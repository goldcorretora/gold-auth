import os
import asyncio
import logging
from urllib.parse import quote, unquote
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, Response, HTTPException, Query, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from database import (
    init_db,
    verificar_conexao,
    BancoIndisponivelError,
    autenticar_usuario,
    buscar_usuario_por_email,
    buscar_usuario_por_id,
    definir_senha_temporaria_usuario,
    trocar_propria_senha,
    obter_configuracoes_email,
    salvar_configuracoes_email,
    enviar_email_recuperacao_senha,
    verificar_cooldown_recuperacao_senha,
    criar_token_recuperacao_senha,
    validar_token_recuperacao_senha,
    consumir_token_e_redefinir_senha,
    enviar_email_link_recuperacao_senha,
    criar_sessao,
    validar_sessao_token,
    revogar_sessao,
    revogar_todas_sessoes_usuario,
    listar_usuarios,
    criar_usuario,
    atualizar_usuario,
    excluir_usuario,
    listar_cargos,
    salvar_cargo,
    excluir_cargo,
    registrar_auditoria,
    listar_auditoria,
    expurgar_auditoria_antiga
)
from ui_templates import get_login_html, get_admin_html

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("gold.auth")

COOKIE_NAME = os.getenv("COOKIE_NAME", "gold_sso_token")
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", ".goldcorretora.com.br").strip()
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() == "true"
PUBLIC_AUTH_URL = os.getenv("PUBLIC_AUTH_URL", "https://auth.goldcorretora.com.br").rstrip("/")
_raw_default_redir = os.getenv("DEFAULT_REDIRECT_URL", "https://apps.goldcorretora.com.br").rstrip("/")
if _raw_default_redir in (
    "https://goldcorretora.com.br",
    "http://goldcorretora.com.br",
    "https://vendas.goldcorretora.com.br",
    "https://painel.goldcorretora.com.br",
    "",
):
    DEFAULT_REDIRECT_URL = "https://apps.goldcorretora.com.br"
else:
    DEFAULT_REDIRECT_URL = _raw_default_redir


def _resolve_safe_redirect(rd: Optional[str]) -> Optional[str]:
    if not rd:
        return None
    cleaned = rd.strip()
    if cleaned.startswith("/admin") or "auth.goldcorretora.com.br/admin" in cleaned:
        return cleaned
    if "auth.goldcorretora.com.br" not in cleaned:
        return cleaned
    return None

# Política de retenção de auditoria (padrão de governança: 90 dias)
AUDIT_RETENTION_DAYS = int(os.getenv("AUDIT_RETENTION_DAYS", "90"))

# Cache leve em memória para evitar gravar 50 logs por segundo do mesmo usuário navegando em assets estáticos
_last_access_audit: Dict[str, float] = {}

async def _rotina_expurgo_auditoria_loop():
    """Rotina assíncrona diária que remove logs de auditoria mais antigos que AUDIT_RETENTION_DAYS."""
    while True:
        try:
            expurgar_auditoria_antiga(AUDIT_RETENTION_DAYS)
        except Exception as e:
            logger.warning(f"Erro na rotina de expurgo de auditoria: {e}")
        # Executa uma vez a cada 24 horas (86400 segundos)
        await asyncio.sleep(86400)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        # Executa limpeza imediata de registros expirados no arranque
        expurgar_auditoria_antiga(AUDIT_RETENTION_DAYS)
    except Exception as e:
        logger.error(f"Erro ao inicializar schema_auth ou expurgar auditoria: {e}")

    # Inicia a tarefa de limpeza periódica em background
    expurgo_task = asyncio.create_task(_rotina_expurgo_auditoria_loop())
    yield
    expurgo_task.cancel()
    logger.info("Encerrando Gold Auth Gateway.")

app = FastAPI(
    title="Gold Auth Gateway",
    description="SSO, Traefik ForwardAuth, Controle de Cargos/Permissões e Auditoria Central da Gold Corretora.",
    version="1.1.0",
    lifespan=lifespan
)

cors_env = os.getenv("CORS_ORIGINS", "https://painel.goldcorretora.com.br,https://simulador.goldcorretora.com.br,https://auth.goldcorretora.com.br,http://localhost:5173,http://localhost:8010")
origins = [o.strip() for o in cors_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.goldcorretora\.com\.br|http://localhost:\d+|http://.*\.sslip\.io",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# HELPERS DE SESSÃO E REDE
# ==========================================================
def get_client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "0.0.0.0"

def extract_token(request: Request) -> Optional[str]:
    token = request.cookies.get(COOKIE_NAME)
    if token:
        return token
    auth_header = request.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return None

def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    token = extract_token(request)
    if not token:
        return None
    return validar_sessao_token(token)

def require_admin(request: Request) -> Dict[str, Any]:
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    perms = user.get("permissoes", [])
    cargo = (user.get("cargo") or "").upper()
    if cargo not in ("TI", "ADMIN", "ADMINISTRATIVO") and "*" not in perms and "admin.manage" not in perms:
        raise HTTPException(status_code=403, detail="Acesso restrito à gestão e TI.")
    return user

def require_ti(request: Request) -> Dict[str, Any]:
    admin = require_admin(request)
    if (admin.get("cargo") or "").upper() != "TI":
        raise HTTPException(status_code=403, detail="Acesso restrito à equipe de TI.")
    return admin

def set_sso_cookie(response: Response, token: str, request: Request, dias_validade: int = 7):
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
    domain = COOKIE_DOMAIN if ("goldcorretora.com.br" in host and COOKIE_DOMAIN) else None
    is_https = (request.headers.get("x-forwarded-proto", "http") == "https") or COOKIE_SECURE

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=dias_validade * 24 * 3600,
        httponly=True,
        secure=is_https if domain else False,
        samesite="lax",
        domain=domain,
        path="/"
    )

def clear_sso_cookie(response: Response, request: Request):
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
    domain = COOKIE_DOMAIN if ("goldcorretora.com.br" in host and COOKIE_DOMAIN) else None
    response.delete_cookie(key=COOKIE_NAME, domain=domain, path="/")
    response.delete_cookie(key=COOKIE_NAME, path="/")

def resolve_app_slug_from_host(host: str) -> str:
    h = (host or "").lower().split(":")[0]
    if "painel" in h or "vendedor" in h or "vendas" in h:
        return "painel-vendedor"
    if "api" in h or "db" in h:
        return "gold-db-api"
    if "simulador" in h or "cotador" in h:
        return "cotador-web"
    if "carteira" in h:
        return "carteira"
    if "apps" in h or "hub" in h:
        return "gold-apps"
    if "concilia" in h:
        return "conciliacao"
    if "auth" in h:
        return "gold-auth"
    return h.split(".")[0] if "." in h else (h or "app-gold")

def user_can_access_app(user: Dict[str, Any], app_slug: str) -> bool:
    cargo = (user.get("cargo") or "").upper()
    if cargo in ("ADMIN", "TI", "ADMINISTRATIVO"):
        return True
    apps = user.get("apps_permitidos") or []
    if "*" in apps or app_slug in apps or app_slug in ("gold-auth", "gold-apps", "conciliacao", "gold-db-api"):
        return True
    return False

# ==========================================================
# FAVICON & IDENTIDADE VISUAL
# ==========================================================
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0A121E"/>
  <rect x="0.75" y="0.75" width="62.5" height="62.5" rx="13.25" fill="none" stroke="#C59B27" stroke-width="1.5" stroke-opacity="0.4"/>
  <text x="32" y="47" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="bold" font-size="40" fill="#F5B82E">G</text>
</svg>"""

@app.get("/favicon.svg", include_in_schema=False)
async def get_favicon_svg():
    return Response(
        content=FAVICON_SVG,
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=86400, immutable"}
    )

@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon_ico():
    ico_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    if os.path.exists(ico_path):
        try:
            with open(ico_path, "rb") as f:
                return Response(
                    content=f.read(),
                    media_type="image/x-icon",
                    headers={"Cache-Control": "public, max-age=86400, immutable"}
                )
        except Exception:
            pass
    return Response(
        content=FAVICON_SVG,
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=86400, immutable"}
    )

@app.get("/favicon.png", include_in_schema=False)
async def get_favicon_png():
    png_path = os.path.join(os.path.dirname(__file__), "static", "favicon.png")
    if os.path.exists(png_path):
        try:
            with open(png_path, "rb") as f:
                return Response(
                    content=f.read(),
                    media_type="image/png",
                    headers={"Cache-Control": "public, max-age=86400, immutable"}
                )
        except Exception:
            pass
    return Response(
        content=FAVICON_SVG,
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=86400, immutable"}
    )

# ==========================================================
# ROTAS VISUAIS (LOGIN & PAINEL ADMIN)
# ==========================================================
@app.get("/", include_in_schema=False)
async def root_redirect(
    request: Request,
    rd: Optional[str] = Query(None),
    redirectUri: Optional[str] = Query(None),
):
    clean_rd = _resolve_safe_redirect(rd or redirectUri)
    user = get_current_user(request)
    if not user:
        target = f"/login?rd={quote(clean_rd)}" if clean_rd else "/login"
        return RedirectResponse(url=target, status_code=302)
    if user.get("precisa_trocar_senha"):
        target = f"/login?force_pw_change=1&rd={quote(clean_rd)}" if clean_rd else "/login?force_pw_change=1"
        return RedirectResponse(url=target, status_code=302)
    if clean_rd:
        return RedirectResponse(url=clean_rd, status_code=302)
    return RedirectResponse(url=DEFAULT_REDIRECT_URL, status_code=302)

@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_page(
    request: Request,
    rd: Optional[str] = Query(None),
    redirectUri: Optional[str] = Query(None),
    force_pw_change: Optional[str] = Query(None),
    reset_token: Optional[str] = Query(None)
):
    clean_rd = _resolve_safe_redirect(rd or redirectUri)
    user = get_current_user(request)
    cfg = obter_configuracoes_email(ocultar_senha=True)
    support_email = cfg.get("support_email") or "acesso@goldcorretora.com.br"

    # Se o usuário clicou no link de confirmação de recuperação do e-mail (?reset_token=...),
    # não redireciona mesmo que haja sessão anterior: valida o token e abre direto o modal de Nova Senha!
    reset_user = validar_token_recuperacao_senha(reset_token) if reset_token else None
    reset_token_status = ""
    if reset_token:
        reset_token_status = "valid" if reset_user else "invalid"

    if user and not user.get("precisa_trocar_senha") and not force_pw_change and not reset_token:
        if clean_rd:
            return RedirectResponse(url=clean_rd, status_code=302)
        return RedirectResponse(url=DEFAULT_REDIRECT_URL, status_code=302)

    return HTMLResponse(
        content=get_login_html(
            default_redirect=DEFAULT_REDIRECT_URL,
            support_email=support_email,
            must_change_password=bool(user and user.get("precisa_trocar_senha")),
            logged_user_email=user.get("email") if user else "",
            reset_token=reset_token or "",
            reset_token_status=reset_token_status,
            reset_user_email=reset_user.get("email", "") if reset_user else "",
            reset_user_name=reset_user.get("nome", "") if reset_user else ""
        ),
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def admin_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login?rd=/admin", status_code=302)
    if user.get("precisa_trocar_senha"):
        return RedirectResponse(url="/login?force_pw_change=1&rd=/admin", status_code=302)
    perms = user.get("permissoes") or []
    cargo = (user.get("cargo") or "").upper()
    if cargo not in ("TI", "ADMIN", "ADMINISTRATIVO") and "*" not in perms:
        return RedirectResponse(url=DEFAULT_REDIRECT_URL, status_code=302)
    try:
        cfg = obter_configuracoes_email(ocultar_senha=True)
    except Exception as e:
        logger.warning(f"Aviso em admin_page ao carregar configuracoes: {e}")
        cfg = {}
    is_ti = (cargo == "TI")
    return HTMLResponse(
        content=get_admin_html(
            default_redirect=DEFAULT_REDIRECT_URL,
            support_email=cfg.get("support_email") or "acesso@goldcorretora.com.br",
            is_ti=is_ti
        )
    )

# ==========================================================
# TRAEFIK FORWARDAUTH ENDPOINT (/api/auth/verify)
# ==========================================================
@app.api_route("/api/auth/verify", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
async def traefik_forward_auth(request: Request, target: Optional[str] = Query(None)):
    """
    Endpoint consultado pelo Traefik no Coolify antes de liberar qualquer requisição para os apps protegidos.
    """
    forwarded_method = request.headers.get("x-forwarded-method", request.method).upper()
    forwarded_proto = request.headers.get("x-forwarded-proto", "https").split(",")[0].strip()

    raw_f_host = request.headers.get("x-forwarded-host") or ""
    first_f_host = raw_f_host.split(",")[0].strip() if raw_f_host else ""
    if target:
        forwarded_host = target.strip().replace("https://", "").replace("http://", "").rstrip("/")
    elif first_f_host and "auth.goldcorretora.com.br" not in first_f_host:
        forwarded_host = first_f_host
    else:
        forwarded_host = DEFAULT_REDIRECT_URL.replace("https://", "").replace("http://", "").rstrip("/")

    raw_f_uri = request.headers.get("x-forwarded-uri", "/")
    forwarded_uri = "/" if raw_f_uri.startswith("/api/auth/verify") else raw_f_uri

    # Libera preflight CORS e healthchecks públicos
    if forwarded_method == "OPTIONS" or forwarded_uri.startswith("/healthz") or forwarded_uri.startswith("/api/health"):
        return Response(status_code=200)

    # Libera POST público de captura de leads vindo do simulador (ex: POST /api/leads)
    if forwarded_method == "POST" and forwarded_uri.rstrip("/") == "/api/leads":
        return Response(status_code=200)

    user = get_current_user(request)
    original_url = f"{forwarded_proto}://{forwarded_host}{forwarded_uri}" if forwarded_host else DEFAULT_REDIRECT_URL
    accept_header = request.headers.get("accept", "").lower()
    is_api_call = ("application/json" in accept_header and "text/html" not in accept_header) or forwarded_uri.startswith("/api/")

    if not user:
        if is_api_call:
            return JSONResponse(
                status_code=401,
                content={"detail": "Sessão expirada ou não autenticada. Faça login em auth.goldcorretora.com.br", "login_url": f"{PUBLIC_AUTH_URL}/login"}
            )
        login_target = f"{PUBLIC_AUTH_URL}/login?rd={quote(original_url)}"
        return RedirectResponse(url=login_target, status_code=302)

    # Se o usuário está usando uma senha temporária, obriga a trocar antes de liberar outros apps
    if user.get("precisa_trocar_senha"):
        if is_api_call:
            return JSONResponse(
                status_code=403,
                content={
                    "detail": "É necessário definir uma nova senha pessoal antes de continuar.",
                    "must_change_password": True,
                    "login_url": f"{PUBLIC_AUTH_URL}/login?force_pw_change=1&rd={quote(original_url)}"
                }
            )
        change_target = f"{PUBLIC_AUTH_URL}/login?force_pw_change=1&rd={quote(original_url)}"
        return RedirectResponse(url=change_target, status_code=302)

    app_slug = resolve_app_slug_from_host(forwarded_host)
    if not user_can_access_app(user, app_slug):
        registrar_auditoria(
            acao="ACESSO_NEGADO_APP",
            usuario=user,
            app=app_slug,
            metodo=forwarded_method,
            rota=forwarded_uri,
            detalhes={"motivo": f"Usuário não possui permissão para o app '{app_slug}'"},
            ip=get_client_ip(request)
        )
        if is_api_call:
            return JSONResponse(status_code=403, content={"detail": f"Sem permissão para acessar {app_slug}."})
        return HTMLResponse(
            status_code=403,
            content=f"""
            <!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Acesso Restrito • Gold Corretora</title>
            <style>body{{font-family:system-ui,sans-serif;background:#0F1A2A;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}}
            .box{{background:#162235;border:1px solid rgba(197,155,39,0.3);padding:32px;border-radius:16px;max-width:420px;text-align:center}}
            a{{display:inline-block;margin-top:16px;padding:10px 20px;background:#C59B27;color:#0F1A2A;font-weight:800;text-decoration:none;border-radius:10px}}</style></head>
            <body><div class="box"><h2>Acesso Restrito</h2><p>Olá <b>{user['nome']}</b>, seu perfil (<b>{user['cargo']}</b>) não possui acesso liberado para o módulo <code>{app_slug}</code>.</p>
            <a href="{DEFAULT_REDIRECT_URL}">Voltar ao Hub</a></div></body></html>
            """
        )

    # Registra auditoria inteligente
    is_static_asset = any(forwarded_uri.endswith(ext) for ext in (".js", ".css", ".svg", ".png", ".ico", ".woff2", ".map"))
    if not is_static_asset:
        import time
        now_ts = time.time()
        cache_key = f"{user['id']}:{app_slug}:{forwarded_method}:{forwarded_uri.split('?')[0]}"
        is_mutation = forwarded_method in ("POST", "PATCH", "PUT", "DELETE")
        last_ts = _last_access_audit.get(cache_key, 0)

        if is_mutation or (now_ts - last_ts > 300 and forwarded_uri in ("/", "/index.html")):
            _last_access_audit[cache_key] = now_ts
            acao_nome = f"ACESSO_{app_slug.upper().replace('-', '_')}" if not is_mutation else f"{forwarded_method}_{forwarded_uri.split('?')[0]}"
            registrar_auditoria(
                acao=acao_nome,
                usuario=user,
                app=app_slug,
                metodo=forwarded_method,
                rota=forwarded_uri,
                detalhes={"host": forwarded_host},
                ip=get_client_ip(request)
            )

    headers = {
        "X-Gold-User-Id": str(user["id"]),
        "X-Gold-User-Name": quote(user["nome"]),
        "X-Gold-User-Email": user["email"],
        "X-Gold-User-Role": user["cargo"],
        "X-Gold-User-Permissions": ",".join(user.get("permissoes") or [])
    }
    return Response(status_code=200, headers=headers)

# ==========================================================
# API DE AUTENTICAÇÃO E SESSÃO (/api/auth/*)
# ==========================================================
class LoginIn(BaseModel):
    email: str
    senha: str
    lembrar: bool = True

class ForgotPasswordIn(BaseModel):
    email: str
    observacao: Optional[str] = ""

class ResetPasswordConfirmIn(BaseModel):
    token: str
    nova_senha: str
    confirmar_senha: Optional[str] = None

class ChangePasswordIn(BaseModel):
    nova_senha: str
    confirmar_senha: Optional[str] = None
    senha_atual: Optional[str] = None
    nome: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[str] = None

class AuditEventIn(BaseModel):
    app: str = Field(default="painel-vendedor")
    acao: str
    metodo: str = Field(default="ACTION")
    rota: str = Field(default="/")
    detalhes: Dict[str, Any] = Field(default_factory=dict)

@app.exception_handler(BancoIndisponivelError)
async def banco_indisponivel_handler(request: Request, exc: BancoIndisponivelError):
    logger.error(f"[DB] {request.method} {request.url.path} falhou: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Serviço de autenticação temporariamente indisponível. Tente novamente em instantes."},
    )

@app.get("/api/health")
@app.get("/healthz")
async def health():
    """Healthcheck do Coolify: só responde 200 se o PostgreSQL estiver acessível."""
    try:
        banco = verificar_conexao()
    except Exception as e:
        logger.error(f"[HEALTH] Banco indisponível: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "service": "gold-auth-gateway", "database": "indisponivel"},
        )
    return {
        "status": "healthy",
        "service": "gold-auth-gateway",
        "database": banco
    }

@app.post("/api/auth/login")
async def api_login(payload: LoginIn, request: Request, response: Response):
    ip = get_client_ip(request)
    ua = request.headers.get("user-agent", "")
    user, erro = autenticar_usuario(payload.email, payload.senha)

    if erro or not user:
        registrar_auditoria(
            acao="LOGIN_FALHA",
            usuario={"nome": payload.email, "email": payload.email, "cargo": "DESCONHECIDO"},
            app="gold-auth",
            metodo="POST",
            rota="/api/auth/login",
            detalhes={"motivo": erro or "Falha de credenciais"},
            ip=ip
        )
        raise HTTPException(status_code=401, detail=erro or "Credenciais inválidas.")

    dias = 30 if payload.lembrar else 1
    token = criar_sessao(user["id"], ip=ip, user_agent=ua, dias_validade=dias)
    set_sso_cookie(response, token, request, dias_validade=dias)

    registrar_auditoria(
        acao="LOGIN_SUCESSO",
        usuario=user,
        app="gold-auth",
        metodo="POST",
        rota="/api/auth/login",
        detalhes={
            "user_agent": ua[:120],
            "permanecer_conectado": payload.lembrar,
            "senha_temporaria": bool(user.get("precisa_trocar_senha"))
        },
        ip=ip
    )

    return {
        "ok": True,
        "token": token,
        "user": user,
        "must_change_password": bool(user.get("precisa_trocar_senha"))
    }

@app.post("/api/auth/change-password")
async def api_change_password(payload: ChangePasswordIn, request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão expirada. Faça login novamente.")

    nova = (payload.nova_senha or "").strip()
    if payload.confirmar_senha is not None and nova != payload.confirmar_senha.strip():
        raise HTTPException(status_code=400, detail="A confirmação de senha não confere.")

    era_temporaria = bool(user.get("precisa_trocar_senha"))
    ok, msg = trocar_propria_senha(
        user["id"],
        nova,
        payload.senha_atual,
        nome=payload.nome,
        telefone=payload.telefone,
        data_nascimento=payload.data_nascimento
    )
    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    nome_final = (payload.nome or "").strip() or user.get("nome", "Usuário")
    acao_audit = "PRIMEIRO_ACESSO_CONCLUIDO" if era_temporaria else "SENHA_ALTERADA_PELO_USUARIO"
    resumo_audit = (
        f"{nome_final} concluiu o primeiro acesso, preencheu perfil e definiu nova senha."
        if era_temporaria
        else f"{nome_final} definiu sua nova senha pessoal de acesso."
    )

    registrar_auditoria(
        acao=acao_audit,
        usuario=user,
        app="gold-auth",
        metodo="POST",
        rota="/api/auth/change-password",
        detalhes={
            "resumo": resumo_audit,
            "telefone_preenchido": bool(payload.telefone),
            "data_nascimento_preenchida": bool(payload.data_nascimento)
        },
        ip=get_client_ip(request)
    )
    return {"ok": True, "message": msg}

@app.post("/api/auth/forgot-password")
async def api_forgot_password(payload: ForgotPasswordIn, request: Request):
    email_limpo = payload.email.strip().lower()
    if not email_limpo:
        raise HTTPException(status_code=400, detail="Por favor, digite seu endereço de e-mail.")

    ip = get_client_ip(request)
    cfg = obter_configuracoes_email(ocultar_senha=False)
    support_email = cfg.get("support_email") or "acesso@goldcorretora.com.br"
    alvo = buscar_usuario_por_email(email_limpo)

    # Verifica diretamente no banco se o e-mail existe e está ativo
    if not alvo:
        raise HTTPException(status_code=404, detail="Nenhuma conta encontrada com este endereço de e-mail.")
    if not alvo.get("ativo"):
        raise HTTPException(status_code=403, detail="Esta conta está bloqueada. Entre em contato com a gestão.")

    # Proteção anti-spam: impede envios repetidos em sequência para o mesmo e-mail
    segundos_restantes = verificar_cooldown_recuperacao_senha(alvo["id"], segundos_cooldown=90)
    if segundos_restantes > 0:
        raise HTTPException(
            status_code=429,
            detail=f"Já enviamos um e-mail com as instruções. Verifique sua caixa de entrada ou aguarde {segundos_restantes}s."
        )

    email_enviado = False
    detalhe_envio = ""

    if cfg.get("smtp_configurado"):
        token_rec = criar_token_recuperacao_senha(alvo["id"], ip=ip, minutos_validade=30)
        link_confirmacao = f"{PUBLIC_AUTH_URL}/login?reset_token={quote(token_rec)}"
        ok_smtp, msg_smtp = enviar_email_link_recuperacao_senha(
            destinatario_email=alvo["email"],
            destinatario_nome=alvo["nome"],
            link_recuperacao=link_confirmacao,
            minutos_validade=30
        )
        email_enviado = ok_smtp
        detalhe_envio = msg_smtp

    registrar_auditoria(
        acao="LINK_RECUPERACAO_ENVIADO" if email_enviado else "SOLICITACAO_REDEFINICAO_SENHA",
        usuario={"nome": alvo["nome"], "email": email_limpo, "cargo": alvo["cargo"]},
        app="gold-auth",
        metodo="POST",
        rota="/api/auth/forgot-password",
        detalhes={
            "alvo_email": email_limpo,
            "email_enviado": email_enviado,
            "detalhe_smtp": detalhe_envio,
            "resumo": f"E-mail com instruções de recuperação enviado para {email_limpo}."
        },
        ip=ip
    )

    return {
        "ok": True,
        "email_sent": email_enviado,
        "support_email": support_email,
        "message": "Enviamos um e-mail com as instruções para redefinir sua senha. Verifique sua caixa de entrada."
    }

@app.post("/api/auth/reset-password-confirm")
async def api_reset_password_confirm(payload: ResetPasswordConfirmIn, request: Request, response: Response):
    token_limpo = (payload.token or "").strip()
    nova = (payload.nova_senha or "").strip()
    if not token_limpo:
        raise HTTPException(status_code=400, detail="Token de recuperação ausente.")
    if len(nova) < 4:
        raise HTTPException(status_code=400, detail="A nova senha deve ter pelo menos 4 caracteres.")
    if payload.confirmar_senha is not None and nova != payload.confirmar_senha.strip():
        raise HTTPException(status_code=400, detail="A confirmação de senha não confere.")

    user, erro = consumir_token_e_redefinir_senha(token_limpo, nova)
    if erro or not user:
        raise HTTPException(status_code=400, detail=erro or "Link de recuperação inválido ou expirado.")

    ip = get_client_ip(request)
    ua = request.headers.get("user-agent", "")

    # Já autentica o colaborador automaticamente na nova senha!
    sess_token = criar_sessao(user["id"], ip=ip, user_agent=ua, dias_validade=7)
    set_sso_cookie(response, sess_token, request, dias_validade=7)

    registrar_auditoria(
        acao="SENHA_REDEFINIDA_POR_LINK",
        usuario=user,
        app="gold-auth",
        metodo="POST",
        rota="/api/auth/reset-password-confirm",
        detalhes={
            "resumo": f"{user['nome']} confirmou o link por e-mail e definiu uma nova senha de acesso."
        },
        ip=ip
    )

    return {
        "ok": True,
        "user": user,
        "message": "Sua nova senha foi salva com sucesso! Redirecionando para o portal..."
    }

@app.post("/api/auth/logout")
@app.get("/api/auth/logout")
async def api_logout(request: Request, response: Response, rd: Optional[str] = Query(None)):
    user = get_current_user(request)
    token = extract_token(request)
    if token:
        revogar_sessao(token)
    if user:
        registrar_auditoria(
            acao="LOGOUT",
            usuario=user,
            app="gold-auth",
            metodo=request.method,
            rota="/api/auth/logout",
            ip=get_client_ip(request)
        )

    if request.method == "GET":
        redir = RedirectResponse(url=rd or "/login", status_code=302)
        clear_sso_cookie(redir, request)
        redir.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        redir.headers["Pragma"] = "no-cache"
        return redir

    clear_sso_cookie(response, request)
    return {"ok": True}

@app.get("/api/auth/me")
async def api_me(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    return {
        "authenticated": True,
        "user": user,
        "auth_url": PUBLIC_AUTH_URL
    }

@app.post("/api/auth/audit")
async def api_record_audit(payload: AuditEventIn, request: Request):
    """Permite que o Painel do Vendedor ou a Gold DB API registrem eventos de negócio detalhados."""
    user = get_current_user(request)
    if not user and request.headers.get("x-gold-user-email"):
        user = {
            "id": int(request.headers.get("x-gold-user-id", "0") or 0) or None,
            "nome": unquote(request.headers.get("x-gold-user-name", "Consultor")),
            "email": request.headers.get("x-gold-user-email"),
            "cargo": request.headers.get("x-gold-user-role", "VENDEDOR")
        }
    registrar_auditoria(
        acao=payload.acao,
        usuario=user,
        app=payload.app,
        metodo=payload.metodo,
        rota=payload.rota,
        detalhes=payload.detalhes,
        ip=get_client_ip(request)
    )
    return {"ok": True}

# ==========================================================
# API ADMINISTRATIVA (USUÁRIOS, CARGOS, E-MAIL & AUDITORIA)
# ==========================================================
class UsuarioCreateIn(BaseModel):
    nome: Optional[str] = ""
    email: str
    senha: Optional[str] = None
    cargo: str = "VENDAS"
    apps_permitidos: List[str] = ["painel-vendedor", "gold-db-api", "cotador-web"]
    permissoes_extras: List[str] = []
    precisa_trocar_senha: bool = False
    enviar_por_email: bool = False

class UsuarioUpdateIn(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    cargo: Optional[str] = None
    apps_permitidos: Optional[List[str]] = None
    permissoes_extras: Optional[List[str]] = None
    ativo: Optional[bool] = None
    precisa_trocar_senha: Optional[bool] = None
    em_ferias: Optional[bool] = None
    ferias_inicio: Optional[str] = None
    ferias_retorno: Optional[str] = None

class SendTempPasswordIn(BaseModel):
    senha_personalizada: Optional[str] = None
    enviar_email: bool = True

class CargoIn(BaseModel):
    codigo: str
    nome: str
    descricao: Optional[str] = ""
    permissoes: List[str] = []
    apps_padrao: List[str] = ["painel-vendedor", "gold-db-api", "cotador-web"]

class EmailSettingsIn(BaseModel):
    support_email: str
    smtp_host: Optional[str] = ""
    smtp_port: int = 587
    smtp_user: Optional[str] = ""
    smtp_password: Optional[str] = ""
    smtp_from_name: Optional[str] = "Gold Corretora de Seguros"
    smtp_from_email: Optional[str] = ""
    smtp_use_tls: bool = True
    limpar_senha_smtp: bool = False

class TestEmailIn(BaseModel):
    destinatario: Optional[str] = None

@app.get("/api/admin/users")
async def admin_list_users(request: Request):
    require_admin(request)
    return listar_usuarios()

@app.post("/api/admin/users", status_code=201)
async def admin_create_user(payload: UsuarioCreateIn, request: Request):
    admin = require_admin(request)
    dados = payload.model_dump()
    if not (dados.get("nome") or "").strip():
        prefixo = dados["email"].split("@")[0].replace(".", " ").title()
        dados["nome"] = prefixo or "Novo Colaborador"
    admin_cargo = (admin.get("cargo") or "").upper()
    if admin_cargo != "TI" and (dados.get("cargo") or "").upper() == "TI":
        raise HTTPException(status_code=403, detail="Apenas a equipe de TI pode criar usuários com cargo de TI.")

    senha_informada = (dados.get("senha") or "").strip()
    if "apps_permitidos" in dados and dados["apps_permitidos"]:
        if "*" not in dados["apps_permitidos"] and "gold-db-api" not in dados["apps_permitidos"]:
            dados["apps_permitidos"].append("gold-db-api")

    # Se marcou envio por email e nao digitou senha manual, gera automaticamente temporaria
    if payload.enviar_por_email and not senha_informada:
        from database import gerar_senha_temporaria
        senha_temp = gerar_senha_temporaria()
        dados["senha"] = senha_temp
        dados["precisa_trocar_senha"] = True
    elif not senha_informada:
        raise HTTPException(status_code=400, detail="Defina uma senha ou marque para enviar a senha temporária por e-mail.")
    else:
        senha_temp = senha_informada

    try:
        novo = criar_usuario(dados)
        email_enviado = False
        msg_email = ""
        if payload.enviar_por_email:
            ok_smtp, msg_smtp = enviar_email_recuperacao_senha(
                destinatario_email=novo["email"],
                destinatario_nome=novo["nome"],
                senha_temporaria=senha_temp,
                portal_url=PUBLIC_AUTH_URL
            )
            email_enviado = ok_smtp
            msg_email = msg_smtp

        registrar_auditoria(
            acao="USUARIO_CRIADO",
            usuario=admin,
            app="gold-auth",
            metodo="POST",
            rota="/api/admin/users",
            detalhes={
                "alvo_email": novo["email"],
                "alvo_nome": novo["nome"],
                "cargo": novo["cargo"],
                "precisa_trocar_senha": novo.get("precisa_trocar_senha", False),
                "email_enviado": email_enviado
            },
            ip=get_client_ip(request)
        )
        novo["email_enviado"] = email_enviado
        novo["mensagem_email"] = msg_email
        # Zero-Knowledge: se foi enviado por email, nunca expoe a senha de volta ao admin
        if email_enviado:
            novo["senha_temporaria"] = None
        return novo
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário (verifique se o e-mail já está em uso): {e}")

@app.patch("/api/admin/users/{user_id}")
async def admin_update_user(user_id: int, payload: UsuarioUpdateIn, request: Request):
    admin = require_admin(request)
    updates = payload.model_dump(exclude_unset=True)

    # Garante acesso transparente às APIs internas (gold-db-api) se alterou apps
    if "apps_permitidos" in updates and updates["apps_permitidos"]:
        if "*" not in updates["apps_permitidos"] and "gold-db-api" not in updates["apps_permitidos"]:
            updates["apps_permitidos"].append("gold-db-api")

    # Validação de intervalo de férias
    if updates.get("ferias_inicio") and updates.get("ferias_retorno"):
        if updates["ferias_retorno"] <= updates["ferias_inicio"]:
            raise HTTPException(status_code=400, detail="A data de retorno deve ser posterior à data de início das férias.")

    admin_cargo = (admin.get("cargo") or "").upper()
    if admin_cargo != "TI":
        alvo_user = buscar_usuario_por_id(user_id)
        if alvo_user and (alvo_user.get("cargo") or "").upper() == "TI":
            raise HTTPException(status_code=403, detail="Apenas a equipe de TI pode modificar contas de TI.")
        if "cargo" in updates and updates["cargo"] and updates["cargo"].upper() == "TI":
            raise HTTPException(status_code=403, detail="Apenas a equipe de TI pode conceder o cargo de TI.")

    # Proteção contra auto-bloqueio ou remoção do próprio cargo ADMIN
    if user_id == admin["id"]:
        if "ativo" in updates and not updates["ativo"]:
            raise HTTPException(status_code=400, detail="Você não pode bloquear sua própria conta de administrador.")
        if "cargo" in updates and updates["cargo"] and updates["cargo"].upper() not in ("TI", "ADMIN", "ADMINISTRATIVO"):
            raise HTTPException(status_code=400, detail="Você não pode remover o cargo administrativo da sua própria conta.")

    try:
        atualizado = atualizar_usuario(user_id, updates)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar usuário: {e}")

    if not atualizado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    acao = "USUARIO_ATUALIZADO"
    if "ativo" in updates and len(updates) == 1:
        acao = "USUARIO_ATIVADO" if updates["ativo"] else "USUARIO_BLOQUEADO"
    elif "em_ferias" in updates:
        acao = "USUARIO_FERIAS_MARCADAS" if updates["em_ferias"] else "USUARIO_FERIAS_ENCERRADAS"

    registrar_auditoria(
        acao=acao,
        usuario=admin,
        app="gold-auth",
        metodo="PATCH",
        rota=f"/api/admin/users/{user_id}",
        detalhes={"alvo_email": atualizado["email"], "campos": list(updates.keys())},
        ip=get_client_ip(request)
    )
    return atualizado

@app.delete("/api/admin/users/{user_id}")
async def admin_delete_user(user_id: int, request: Request):
    admin = require_admin(request)
    if user_id == admin["id"]:
        raise HTTPException(status_code=400, detail="Você não pode excluir sua própria conta de administrador.")

    admin_cargo = (admin.get("cargo") or "").upper()
    if admin_cargo != "TI":
        alvo_user = buscar_usuario_por_id(user_id)
        if alvo_user and (alvo_user.get("cargo") or "").upper() == "TI":
            raise HTTPException(status_code=403, detail="Apenas a equipe de TI pode excluir contas de TI.")

    excluido = excluir_usuario(user_id)
    if not excluido:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    registrar_auditoria(
        acao="USUARIO_EXCLUIDO",
        usuario=admin,
        app="gold-auth",
        metodo="DELETE",
        rota=f"/api/admin/users/{user_id}",
        detalhes={"alvo_email": excluido["email"], "alvo_nome": excluido["nome"]},
        ip=get_client_ip(request)
    )
    return {"ok": True, "deleted": excluido}

@app.post("/api/admin/users/{user_id}/send-temp-password")
async def admin_send_temp_password(user_id: int, payload: SendTempPasswordIn, request: Request):
    admin = require_admin(request)
    alvo = buscar_usuario_por_id(user_id)
    if not alvo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    atualizado, senha_temp = definir_senha_temporaria_usuario(user_id, payload.senha_personalizada)
    email_enviado = False
    msg_smtp = "Envio por e-mail não solicitado."

    if payload.enviar_email:
        email_enviado, msg_smtp = enviar_email_recuperacao_senha(
            destinatario_email=alvo["email"],
            destinatario_nome=alvo["nome"],
            senha_temporaria=senha_temp,
            portal_url=PUBLIC_AUTH_URL
        )
        if not email_enviado:
            raise HTTPException(status_code=400, detail=f"Falha ao enviar e-mail: {msg_smtp}")

    cfg = obter_configuracoes_email(ocultar_senha=True)
    registrar_auditoria(
        acao="SENHA_TEMPORARIA_GERADA_ADMIN",
        usuario=admin,
        app="gold-auth",
        metodo="POST",
        rota=f"/api/admin/users/{user_id}/send-temp-password",
        detalhes={
            "alvo_email": alvo["email"],
            "email_enviado": email_enviado,
            "resumo": f"Senha temporária gerada para {alvo['nome']} ({alvo['email']}) • {'Enviada por e-mail (Zero-Knowledge)' if email_enviado else 'Gerada para envio manual'}"
        },
        ip=get_client_ip(request)
    )

    return {
        "ok": True,
        "usuario": atualizado,
        # Zero-Knowledge: se o email foi enviado com sucesso, nunca exibe a senha para o administrador
        "senha_temporaria": None if email_enviado else senha_temp,
        "email_enviado": email_enviado,
        "mensagem_smtp": msg_smtp if email_enviado else "Senha gerada para envio manual.",
        "support_email": cfg.get("support_email") or "acesso@goldcorretora.com.br",
        "portal_url": f"{PUBLIC_AUTH_URL}/login"
    }

@app.post("/api/admin/users/{user_id}/revoke-sessions")
async def admin_revoke_user_sessions(user_id: int, request: Request):
    admin = require_admin(request)
    alvo = buscar_usuario_por_id(user_id)
    revogar_todas_sessoes_usuario(user_id)
    registrar_auditoria(
        acao="SESSOES_REVOGADAS",
        usuario=admin,
        app="gold-auth",
        metodo="POST",
        rota=f"/api/admin/users/{user_id}/revoke-sessions",
        detalhes={"alvo_id": user_id, "alvo_email": alvo["email"] if alvo else str(user_id)},
        ip=get_client_ip(request)
    )
    return {"ok": True}

@app.get("/api/admin/email-settings")
async def admin_get_email_settings(request: Request):
    require_ti(request)
    return obter_configuracoes_email(ocultar_senha=True)

@app.post("/api/admin/email-settings")
async def admin_save_email_settings(payload: EmailSettingsIn, request: Request):
    admin = require_ti(request)
    salvo = salvar_configuracoes_email(payload.model_dump())
    registrar_auditoria(
        acao="CONFIG_EMAIL_ATUALIZADA",
        usuario=admin,
        app="gold-auth",
        metodo="POST",
        rota="/api/admin/email-settings",
        detalhes={
            "support_email": salvo.get("support_email"),
            "smtp_host": salvo.get("smtp_host"),
            "smtp_configurado": salvo.get("smtp_configurado")
        },
        ip=get_client_ip(request)
    )
    return salvo

@app.post("/api/admin/email-settings/test")
async def admin_test_email_settings(payload: TestEmailIn, request: Request):
    admin = require_ti(request)
    destino = (payload.destinatario or admin.get("email") or "").strip()
    if not destino:
        raise HTTPException(status_code=400, detail="Informe um e-mail destinatário para o teste.")

    ok, msg = enviar_email_recuperacao_senha(
        destinatario_email=destino,
        destinatario_nome=admin.get("nome", "Administrador Gold"),
        senha_temporaria="Gold@Teste2026",
        portal_url=PUBLIC_AUTH_URL
    )
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"ok": True, "message": f"E-mail de teste disparado com sucesso para {destino}!"}

@app.get("/api/admin/roles")
async def admin_list_roles(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    return listar_cargos()

@app.post("/api/admin/roles")
async def admin_save_role(payload: CargoIn, request: Request):
    admin = require_admin(request)
    dados = payload.model_dump()
    if "apps_padrao" in dados and dados["apps_padrao"]:
        if "*" not in dados["apps_padrao"] and "gold-db-api" not in dados["apps_padrao"]:
            dados["apps_padrao"].append("gold-db-api")
    role = salvar_cargo(dados)
    registrar_auditoria(
        acao="CARGO_SALVO",
        usuario=admin,
        app="gold-auth",
        metodo="POST",
        rota="/api/admin/roles",
        detalhes={
            "codigo": role["codigo"],
            "nome": role["nome"],
            "permissoes": role["permissoes"],
            "apps_padrao": role.get("apps_padrao", [])
        },
        ip=get_client_ip(request)
    )
    return role

@app.delete("/api/admin/roles/{codigo}")
async def admin_delete_role(codigo: str, request: Request):
    admin = require_admin(request)
    ok = excluir_cargo(codigo)
    if not ok:
        raise HTTPException(status_code=400, detail="Não é possível excluir o cargo de TI ou cargos que ainda possuam usuários vinculados.")
    registrar_auditoria(
        acao="CARGO_EXCLUIDO",
        usuario=admin,
        app="gold-auth",
        metodo="DELETE",
        rota=f"/api/admin/roles/{codigo}",
        detalhes={"codigo": codigo},
        ip=get_client_ip(request)
    )
    return {"ok": True}

@app.get("/api/admin/audit")
async def admin_list_audit(
    request: Request,
    q: Optional[str] = Query(None),
    app: Optional[str] = Query("TODOS"),
    email: Optional[str] = Query("TODOS"),
    limite: int = Query(120, ge=1, le=500)
):
    require_ti(request)
    return listar_auditoria(busca=q, app=app, usuario_email=email, limite=limite)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8010"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
