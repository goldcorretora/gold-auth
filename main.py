import os
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
    autenticar_usuario,
    criar_sessao,
    validar_sessao_token,
    revogar_sessao,
    revogar_todas_sessoes_usuario,
    listar_usuarios,
    criar_usuario,
    atualizar_usuario,
    listar_cargos,
    salvar_cargo,
    excluir_cargo,
    registrar_auditoria,
    listar_auditoria
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
DEFAULT_REDIRECT_URL = os.getenv("DEFAULT_REDIRECT_URL", "https://painel.goldcorretora.com.br").rstrip("/")

# Cache leve em memória para evitar gravar 50 logs por segundo do mesmo usuário navegando em assets estáticos
_last_access_audit: Dict[str, float] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except Exception as e:
        logger.error(f"Erro ao inicializar schema_auth: {e}")
    yield
    logger.info("Encerrando Gold Auth Gateway.")

app = FastAPI(
    title="Gold Auth Gateway",
    description="SSO, Traefik ForwardAuth, Controle de Cargos/Permissões e Auditoria Central da Gold Corretora.",
    version="1.0.0",
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
    if user.get("cargo") != "ADMIN" and "*" not in perms and "admin.manage" not in perms:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores.")
    return user

def set_sso_cookie(response: Response, token: str, request: Request):
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
    domain = COOKIE_DOMAIN if ("goldcorretora.com.br" in host and COOKIE_DOMAIN) else None
    is_https = (request.headers.get("x-forwarded-proto", "http") == "https") or COOKIE_SECURE

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=7 * 24 * 3600,
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
    if "painel" in h or "vendedor" in h:
        return "painel-vendedor"
    if "api" in h or "db" in h:
        return "gold-db-api"
    if "simulador" in h or "cotador" in h:
        return "cotador-web"
    if "carteira" in h:
        return "carteira"
    if "auth" in h:
        return "gold-auth"
    return h.split(".")[0] if "." in h else (h or "app-gold")

def user_can_access_app(user: Dict[str, Any], app_slug: str) -> bool:
    if user.get("cargo") == "ADMIN":
        return True
    apps = user.get("apps_permitidos") or []
    if "*" in apps or app_slug in apps or app_slug == "gold-auth":
        return True
    return False

# ==========================================================
# ROTAS VISUAIS (LOGIN & PAINEL ADMIN)
# ==========================================================
@app.get("/", include_in_schema=False)
async def root_redirect(request: Request, rd: Optional[str] = Query(None)):
    user = get_current_user(request)
    if not user:
        target = f"/login?rd={quote(rd)}" if rd else "/login"
        return RedirectResponse(url=target, status_code=302)
    if rd:
        return RedirectResponse(url=rd, status_code=302)
    if user.get("cargo") == "ADMIN" or "auditoria.view" in (user.get("permissoes") or []):
        return RedirectResponse(url="/admin", status_code=302)
    return RedirectResponse(url=DEFAULT_REDIRECT_URL, status_code=302)

@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_page(request: Request, rd: Optional[str] = Query(None)):
    user = get_current_user(request)
    if user:
        if rd:
            return RedirectResponse(url=rd, status_code=302)
        if user.get("cargo") == "ADMIN":
            return RedirectResponse(url="/admin", status_code=302)
        return RedirectResponse(url=DEFAULT_REDIRECT_URL, status_code=302)
    return HTMLResponse(content=get_login_html(default_redirect=DEFAULT_REDIRECT_URL))

@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def admin_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login?rd=/admin", status_code=302)
    perms = user.get("permissoes") or []
    if user.get("cargo") != "ADMIN" and "*" not in perms and "auditoria.view" not in perms:
        return RedirectResponse(url=DEFAULT_REDIRECT_URL, status_code=302)
    return HTMLResponse(content=get_admin_html(default_redirect=DEFAULT_REDIRECT_URL))

# ==========================================================
# TRAEFIK FORWARDAUTH ENDPOINT (/api/auth/verify)
# ==========================================================
@app.api_route("/api/auth/verify", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
async def traefik_forward_auth(request: Request):
    """
    Endpoint consultado pelo Traefik no Coolify antes de liberar qualquer requisição para os apps protegidos.
    - Se for requisição OPTIONS (CORS preflight), retorna 200 OK para o navegador prosseguir.
    - Se autenticado e autorizado, retorna 200 OK com cabeçalhos X-Gold-User-* para o app destino.
    - Se não autenticado:
        * Se for chamada de API/JSON (Accept: application/json ou /api/*), retorna 401 JSON.
        * Se for acesso via navegador, redireciona (302) para https://auth.goldcorretora.com.br/login?rd=<URL_ORIGINAL>
    """
    forwarded_method = request.headers.get("x-forwarded-method", request.method).upper()
    forwarded_proto = request.headers.get("x-forwarded-proto", "https")
    forwarded_host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
    forwarded_uri = request.headers.get("x-forwarded-uri", "/")

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
            <a href="{PUBLIC_AUTH_URL}/login">Voltar</a></div></body></html>
            """
        )

    # Registra auditoria inteligente (todas as mutações POST/PATCH/PUT/DELETE ou primeiro acesso a página a cada 5 min)
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

    # Injeta headers seguros para o backend/app destino (URL-encoded para evitar erro de acentuação em HTTP headers)
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

class AuditEventIn(BaseModel):
    app: str = Field(default="painel-vendedor")
    acao: str
    metodo: str = Field(default="ACTION")
    rota: str = Field(default="/")
    detalhes: Dict[str, Any] = Field(default_factory=dict)

@app.get("/api/health")
@app.get("/healthz")
async def health():
    return {"status": "healthy", "service": "gold-auth-gateway"}

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

    token = criar_sessao(user["id"], ip=ip, user_agent=ua)
    set_sso_cookie(response, token, request)

    registrar_auditoria(
        acao="LOGIN_SUCESSO",
        usuario=user,
        app="gold-auth",
        metodo="POST",
        rota="/api/auth/login",
        detalhes={"user_agent": ua[:120]},
        ip=ip
    )

    return {
        "ok": True,
        "token": token,
        "user": user
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
    # Também aceita identificação via headers internos se vier da gold-db-api
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
# API ADMINISTRATIVA (USUÁRIOS, CARGOS & AUDITORIA)
# ==========================================================
class UsuarioCreateIn(BaseModel):
    nome: str
    email: str
    senha: str
    cargo: str = "VENDEDOR"
    apps_permitidos: List[str] = ["painel-vendedor", "gold-db-api", "cotador-web"]
    permissoes_extras: List[str] = []

class UsuarioUpdateIn(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    cargo: Optional[str] = None
    apps_permitidos: Optional[List[str]] = None
    permissoes_extras: Optional[List[str]] = None
    ativo: Optional[bool] = None

class CargoIn(BaseModel):
    codigo: str
    nome: str
    descricao: Optional[str] = ""
    permissoes: List[str] = []
    apps_padrao: List[str] = ["painel-vendedor"]

@app.get("/api/admin/users")
async def admin_list_users(request: Request):
    require_admin(request)
    return listar_usuarios()

@app.post("/api/admin/users", status_code=201)
async def admin_create_user(payload: UsuarioCreateIn, request: Request):
    admin = require_admin(request)
    try:
        novo = criar_usuario(payload.model_dump())
        registrar_auditoria(
            acao="USUARIO_CRIADO",
            usuario=admin,
            app="gold-auth",
            metodo="POST",
            rota="/api/admin/users",
            detalhes={"alvo_email": novo["email"], "alvo_nome": novo["nome"], "cargo": novo["cargo"]},
            ip=get_client_ip(request)
        )
        return novo
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário (verifique se o e-mail já existe): {e}")

@app.patch("/api/admin/users/{user_id}")
async def admin_update_user(user_id: int, payload: UsuarioUpdateIn, request: Request):
    admin = require_admin(request)
    updates = payload.model_dump(exclude_unset=True)
    atualizado = atualizar_usuario(user_id, updates)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    acao = "USUARIO_ATUALIZADO"
    if "ativo" in updates:
        acao = "USUARIO_ATIVADO" if updates["ativo"] else "USUARIO_BLOQUEADO"

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

@app.post("/api/admin/users/{user_id}/revoke-sessions")
async def admin_revoke_user_sessions(user_id: int, request: Request):
    admin = require_admin(request)
    revogar_todas_sessoes_usuario(user_id)
    registrar_auditoria(
        acao="SESSOES_REVOGADAS",
        usuario=admin,
        app="gold-auth",
        metodo="POST",
        rota=f"/api/admin/users/{user_id}/revoke-sessions",
        detalhes={"alvo_id": user_id},
        ip=get_client_ip(request)
    )
    return {"ok": True}

@app.get("/api/admin/roles")
async def admin_list_roles(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    return listar_cargos()

@app.post("/api/admin/roles")
async def admin_save_role(payload: CargoIn, request: Request):
    admin = require_admin(request)
    role = salvar_cargo(payload.model_dump())
    registrar_auditoria(
        acao="CARGO_SALVO",
        usuario=admin,
        app="gold-auth",
        metodo="POST",
        rota="/api/admin/roles",
        detalhes={"codigo": role["codigo"], "nome": role["nome"], "permissoes": role["permissoes"]},
        ip=get_client_ip(request)
    )
    return role

@app.delete("/api/admin/roles/{codigo}")
async def admin_delete_role(codigo: str, request: Request):
    admin = require_admin(request)
    ok = excluir_cargo(codigo)
    if not ok:
        raise HTTPException(status_code=400, detail="Não foi possível excluir este cargo (cargos de sistema são protegidos).")
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
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado.")
    perms = user.get("permissoes") or []
    if user.get("cargo") != "ADMIN" and "*" not in perms and "auditoria.view" not in perms:
        raise HTTPException(status_code=403, detail="Sem permissão para visualizar auditoria.")
    return listar_auditoria(busca=q, app=app, usuario_email=email, limite=limite)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8010"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
