import os
import json
import hmac
import hashlib
import secrets
import logging
import smtplib
from email.message import EmailMessage
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("gold.auth.db")

class BancoIndisponivelError(RuntimeError):
    """PostgreSQL inacessível ou não configurado. O serviço falha com 503 sem criar SQLite."""


def get_database_url() -> str:
    url = (os.getenv("DATABASE_URL") or "").strip()
    if not url.startswith(("postgresql://", "postgres://")):
        raise BancoIndisponivelError(
            "DATABASE_URL não configurada ou inválida (esperado postgresql://...). "
            "Defina a variável no Coolify apontando para o PostgreSQL."
        )
    return url


def is_postgres_url(url: str) -> bool:
    return url.startswith(("postgresql://", "postgres://"))


def get_connection():
    url = get_database_url()
    try:
        import psycopg
        from psycopg.rows import dict_row
        conn = psycopg.connect(url, row_factory=dict_row, connect_timeout=5)
        return conn, True
    except psycopg.Error as e:
        logger.error(f"[DB] PostgreSQL inacessível: {e}")
        raise BancoIndisponivelError(f"PostgreSQL inacessível: {e}") from e


def verificar_conexao() -> Dict[str, Any]:
    """Usado pelo /api/health: confirma que o PostgreSQL responde e informa o banco e total de usuários."""
    conn, _ = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT current_database() AS banco, (SELECT COUNT(*) FROM schema_auth.usuarios) AS total_usuarios;")
        row = cur.fetchone()
        return {"engine": "postgresql", "database": row["banco"], "total_usuarios": row["total_usuarios"]}
    finally:
        conn.close()

def hash_password(password: str, salt: Optional[str] = None) -> str:
    if not salt:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        210000
    )
    return f"pbkdf2_sha256$210000${salt}${dk.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        parts = stored_hash.split("$")
        if len(parts) != 4:
            return False
        _, iterations, salt, hash_hex = parts
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations)
        )
        return hmac.compare_digest(dk.hex(), hash_hex)
    except Exception:
        return False

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def gerar_senha_temporaria() -> str:
    """Gera uma senha temporária amigável para digitação, mas segura (ex: Gold@4829)."""
    digitos = "".join(secrets.choice("23456789") for _ in range(4))
    sufixo = "".join(secrets.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(2))
    return f"Gold@{digitos}{sufixo}"

_initialized = False

def ensure_db_initialized():
    global _initialized
    if not _initialized:
        init_db()
        _initialized = True

DEFAULT_ROLES = [
    {
        "codigo": "ADMIN",
        "nome": "Administrador Geral",
        "descricao": "Acesso total a todos os sistemas, gestão de equipe, cargos e auditoria.",
        "permissoes": ["*"],
        "apps_padrao": ["*"],
        "is_system": True
    },
    {
        "codigo": "SUPERVISOR",
        "nome": "Supervisor Comercial",
        "descricao": "Visão completa do funil de vendas, carteira de clientes e relatórios.",
        "permissoes": ["leads.view_all", "leads.edit", "leads.assign", "carteira.view", "auditoria.view"],
        "apps_padrao": ["painel-vendedor", "gold-db-api", "cotador-web", "carteira"],
        "is_system": True
    },
    {
        "codigo": "VENDEDOR",
        "nome": "Consultor de Seguros",
        "descricao": "Atendimento de leads em tempo real, propostas e cotações.",
        "permissoes": ["leads.view", "leads.edit", "cotador.use"],
        "apps_padrao": ["painel-vendedor", "gold-db-api", "cotador-web"],
        "is_system": True
    }
]

def init_db():
    conn, is_pg = get_connection()
    cur = conn.cursor()
    logger.info("Inicializando schema_auth com PostgreSQL isolado...")

    if is_pg:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS schema_auth;

            CREATE TABLE IF NOT EXISTS schema_auth.cargos (
                id SERIAL PRIMARY KEY,
                codigo VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT,
                permissoes JSONB DEFAULT '[]'::jsonb,
                apps_padrao JSONB DEFAULT '[]'::jsonb,
                is_system BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS schema_auth.usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                cargo VARCHAR(50) NOT NULL DEFAULT 'VENDEDOR',
                apps_permitidos JSONB DEFAULT '["painel-vendedor", "gold-db-api", "cotador-web"]'::jsonb,
                permissoes_extras JSONB DEFAULT '[]'::jsonb,
                ativo BOOLEAN DEFAULT TRUE,
                precisa_trocar_senha BOOLEAN DEFAULT FALSE,
                ultimo_login TIMESTAMPTZ,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );

            ALTER TABLE schema_auth.usuarios
            ADD COLUMN IF NOT EXISTS precisa_trocar_senha BOOLEAN DEFAULT FALSE;

            CREATE TABLE IF NOT EXISTS schema_auth.sessoes (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES schema_auth.usuarios(id) ON DELETE CASCADE,
                token_hash VARCHAR(128) UNIQUE NOT NULL,
                ip VARCHAR(64),
                user_agent TEXT,
                expires_at TIMESTAMPTZ NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS schema_auth.auditoria (
                id BIGSERIAL PRIMARY KEY,
                usuario_id INTEGER,
                usuario_nome VARCHAR(255),
                usuario_email VARCHAR(255),
                usuario_cargo VARCHAR(50),
                app VARCHAR(100),
                acao VARCHAR(120) NOT NULL,
                metodo VARCHAR(20),
                rota TEXT,
                detalhes JSONB DEFAULT '{}'::jsonb,
                ip VARCHAR(64),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS schema_auth.configuracoes (
                chave VARCHAR(100) PRIMARY KEY,
                valor TEXT,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_auth_sessoes_token ON schema_auth.sessoes(token_hash);
            CREATE INDEX IF NOT EXISTS idx_auth_auditoria_created ON schema_auth.auditoria(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_auth_auditoria_email ON schema_auth.auditoria(usuario_email);
        """)
    else:
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS auth_cargos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                descricao TEXT,
                permissoes TEXT DEFAULT '[]',
                apps_padrao TEXT DEFAULT '[]',
                is_system INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS auth_usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                cargo TEXT NOT NULL DEFAULT 'VENDEDOR',
                apps_permitidos TEXT DEFAULT '["painel-vendedor", "gold-db-api", "cotador-web"]',
                permissoes_extras TEXT DEFAULT '[]',
                ativo INTEGER DEFAULT 1,
                precisa_trocar_senha INTEGER DEFAULT 0,
                ultimo_login TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS auth_sessoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                token_hash TEXT UNIQUE NOT NULL,
                ip TEXT,
                user_agent TEXT,
                expires_at TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS auth_auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                usuario_nome TEXT,
                usuario_email TEXT,
                usuario_cargo TEXT,
                app TEXT,
                acao TEXT NOT NULL,
                metodo TEXT,
                rota TEXT,
                detalhes TEXT DEFAULT '{}',
                ip TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS auth_configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_auth_sessoes_token ON auth_sessoes(token_hash);
            CREATE INDEX IF NOT EXISTS idx_auth_auditoria_created ON auth_auditoria(created_at DESC);
        """)
        try:
            cur.execute("ALTER TABLE auth_usuarios ADD COLUMN precisa_trocar_senha INTEGER DEFAULT 0;")
        except Exception:
            pass

    conn.commit()

    # Seed de cargos iniciais
    tb_cargos = "schema_auth.cargos" if is_pg else "auth_cargos"
    for r in DEFAULT_ROLES:
        if is_pg:
            from psycopg.types.json import Jsonb
            cur.execute(
                f"""
                INSERT INTO {tb_cargos} (codigo, nome, descricao, permissoes, apps_padrao, is_system)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (codigo) DO NOTHING;
                """,
                (r["codigo"], r["nome"], r["descricao"], Jsonb(r["permissoes"]), Jsonb(r["apps_padrao"]), r["is_system"])
            )
        else:
            cur.execute(
                f"""
                INSERT OR IGNORE INTO {tb_cargos} (codigo, nome, descricao, permissoes, apps_padrao, is_system)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (r["codigo"], r["nome"], r["descricao"], json.dumps(r["permissoes"]), json.dumps(r["apps_padrao"]), 1 if r["is_system"] else 0)
            )

    # Seed do usuário Admin Master caso não exista nenhum usuário
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    cur.execute(f"SELECT COUNT(*) as total FROM {tb_users};")
    total_users = cur.fetchone()["total"]

    if total_users == 0:
        admin_name = os.getenv("ADMIN_INITIAL_NAME", "Gabriel Gold").strip()
        admin_email = os.getenv("ADMIN_INITIAL_EMAIL", "admin@goldcorretora.com.br").strip().lower()
        admin_pass = os.getenv("ADMIN_INITIAL_PASSWORD", "Gold@2026")
        pw_hash = hash_password(admin_pass)

        if is_pg:
            from psycopg.types.json import Jsonb
            cur.execute(
                f"""
                INSERT INTO {tb_users} (nome, email, senha_hash, cargo, apps_permitidos, permissoes_extras, ativo, precisa_trocar_senha)
                VALUES (%s, %s, %s, 'ADMIN', %s, %s, TRUE, FALSE);
                """,
                (admin_name, admin_email, pw_hash, Jsonb(["*"]), Jsonb(["*"]))
            )
        else:
            cur.execute(
                f"""
                INSERT INTO {tb_users} (nome, email, senha_hash, cargo, apps_permitidos, permissoes_extras, ativo, precisa_trocar_senha)
                VALUES (?, ?, ?, 'ADMIN', ?, ?, 1, 0);
                """,
                (admin_name, admin_email, pw_hash, json.dumps(["*"]), json.dumps(["*"]))
            )
        logger.info(f"Usuário ADMIN inicial criado: {admin_email}")

    conn.commit()
    conn.close()

def _parse_json_field(val: Any, default: Any):
    if val is None:
        return default
    if isinstance(val, (list, dict)):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except Exception:
            return default
    return default

def _normalize_user(row: Any, is_pg: bool) -> Dict[str, Any]:
    d = dict(row)
    d.pop("senha_hash", None)
    d["apps_permitidos"] = _parse_json_field(d.get("apps_permitidos"), [])
    d["permissoes_extras"] = _parse_json_field(d.get("permissoes_extras"), [])
    d["ativo"] = bool(d.get("ativo", True))
    d["precisa_trocar_senha"] = bool(d.get("precisa_trocar_senha", False))
    return d

def _normalize_role(row: Any) -> Dict[str, Any]:
    d = dict(row)
    d["permissoes"] = _parse_json_field(d.get("permissoes"), [])
    d["apps_padrao"] = _parse_json_field(d.get("apps_padrao"), [])
    d["is_system"] = bool(d.get("is_system", False))
    return d

# ==========================================================
# CONFIGURAÇÕES DE E-MAIL E SUPORTE DA GOLD CORRETORA
# ==========================================================
DEFAULT_EMAIL_SETTINGS = {
    "support_email": os.getenv("SUPPORT_EMAIL", "acesso@goldcorretora.com.br").strip(),
    "smtp_host": os.getenv("SMTP_HOST", "").strip(),
    "smtp_port": int(os.getenv("SMTP_PORT", "587") or 587),
    "smtp_user": os.getenv("SMTP_USER", "").strip(),
    "smtp_password": os.getenv("SMTP_PASSWORD", ""),
    "smtp_from_name": os.getenv("SMTP_FROM_NAME", "Gold Corretora de Seguros").strip(),
    "smtp_from_email": os.getenv("SMTP_FROM_EMAIL", "acesso@goldcorretora.com.br").strip(),
    "smtp_use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true"
}

def obter_configuracoes_email(ocultar_senha: bool = False) -> Dict[str, Any]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_cfg = "schema_auth.configuracoes" if is_pg else "auth_configuracoes"
    cur.execute(f"SELECT chave, valor FROM {tb_cfg};")
    rows = cur.fetchall()
    conn.close()

    stored = {r["chave"]: r["valor"] for r in rows}
    cfg = dict(DEFAULT_EMAIL_SETTINGS)

    for k in ("support_email", "smtp_host", "smtp_user", "smtp_password", "smtp_from_name", "smtp_from_email"):
        if k in stored and stored[k] is not None:
            cfg[k] = stored[k]

    if "smtp_port" in stored and stored["smtp_port"]:
        try:
            cfg["smtp_port"] = int(stored["smtp_port"])
        except Exception:
            pass

    if "smtp_use_tls" in stored and stored["smtp_use_tls"] is not None:
        cfg["smtp_use_tls"] = str(stored["smtp_use_tls"]).lower() in ("true", "1", "yes")

    cfg["smtp_configurado"] = bool(cfg.get("smtp_host") and cfg.get("smtp_user") and cfg.get("smtp_password"))
    if ocultar_senha:
        cfg["tem_senha_salva"] = bool(cfg.get("smtp_password"))
        cfg["smtp_password"] = ""
    return cfg

def salvar_configuracoes_email(novos_dados: Dict[str, Any]) -> Dict[str, Any]:
    ensure_db_initialized()
    atual = obter_configuracoes_email(ocultar_senha=False)
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_cfg = "schema_auth.configuracoes" if is_pg else "auth_configuracoes"

    campos = ["support_email", "smtp_host", "smtp_port", "smtp_user", "smtp_from_name", "smtp_from_email", "smtp_use_tls"]
    if nuevos_pw := novos_dados.get("smtp_password"):
        if nuevos_pw.strip():
            campos.append("smtp_password")
    elif novos_dados.get("limpar_senha_smtp"):
        campos.append("smtp_password")
        novos_dados["smtp_password"] = ""

    for k in campos:
        if k not in novos_dados or novos_dados[k] is None:
            continue
        val_str = str(novos_dados[k]).strip() if k != "smtp_password" else str(novos_dados[k])
        if is_pg:
            cur.execute(
                f"""
                INSERT INTO {tb_cfg} (chave, valor, updated_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (chave) DO UPDATE SET valor = EXCLUDED.valor, updated_at = CURRENT_TIMESTAMP;
                """,
                (k, val_str)
            )
        else:
            cur.execute(
                f"""
                INSERT INTO {tb_cfg} (chave, valor, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor, updated_at = CURRENT_TIMESTAMP;
                """,
                (k, val_str)
            )

    conn.commit()
    conn.close()
    return obter_configuracoes_email(ocultar_senha=True)

def enviar_email_recuperacao_senha(
    destinatario_email: str,
    destinatario_nome: str,
    senha_temporaria: str,
    portal_url: str = "https://auth.goldcorretora.com.br"
) -> Tuple[bool, str]:
    """
    Envia um e-mail institucional da Gold Corretora contendo a senha temporária
    e instruindo o colaborador a trocá-la no primeiro acesso.
    """
    cfg = obter_configuracoes_email(ocultar_senha=False)
    if not cfg.get("smtp_configurado"):
        return False, "Servidor de e-mail (SMTP) da Gold ainda não configurado no painel."

    host = cfg["smtp_host"]
    port = int(cfg.get("smtp_port") or 587)
    user = cfg["smtp_user"]
    password = cfg["smtp_password"]
    from_name = cfg.get("smtp_from_name") or "Gold Corretora de Seguros"
    from_email = cfg.get("smtp_from_email") or user
    reply_to = cfg.get("support_email") or from_email
    use_tls = bool(cfg.get("smtp_use_tls", True))

    msg = EmailMessage()
    msg["Subject"] = "Sua senha temporária de acesso • Gold Corretora"
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = destinatario_email
    if reply_to:
        msg["Reply-To"] = reply_to

    texto_puro = (
        f"Olá, {destinatario_nome}!\n\n"
        f"Uma senha temporária foi gerada para o seu acesso ao Portal Interno da Gold Corretora de Seguros.\n\n"
        f"E-mail de acesso: {destinatario_email}\n"
        f"Senha temporária: {senha_temporaria}\n\n"
        f"Acesse em: {portal_url}/login\n\n"
        f"Importante: Assim que você entrar com esta senha temporária, o sistema solicitará que você defina uma nova senha pessoal de sua preferência.\n\n"
        f"Dúvidas? Entre em contato pelo e-mail {reply_to}.\n"
        f"Gold Corretora de Seguros"
    )
    msg.set_content(texto_puro)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <body style="margin:0;padding:24px;background-color:#F1F5F9;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;color:#0F1A2A;">
      <div style="max-width:520px;margin:0 auto;background:#FFFFFF;border-radius:16px;border:1px solid #E2E8F0;overflow:hidden;">
        <div style="background:#0F1A2A;padding:24px 28px;border-bottom:3px solid #C59B27;">
          <div style="color:#F5B82E;font-size:12px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;">Gold Corretora de Seguros</div>
          <h1 style="color:#FFFFFF;font-size:20px;margin:6px 0 0 0;font-weight:800;">Recuperação de Acesso ao Portal</h1>
        </div>
        <div style="padding:28px;">
          <p style="margin:0 0 16px 0;font-size:15px;line-height:1.6;color:#334155;">
            Olá, <strong>{destinatario_nome}</strong>.
          </p>
          <p style="margin:0 0 20px 0;font-size:14px;line-height:1.6;color:#475569;">
            Recebemos uma solicitação de redefinição de senha para a sua conta na Gold Corretora. Utilize a credencial temporária abaixo para acessar o sistema:
          </p>
          <div style="background:#F8FAFC;border:1px solid #CBD5E1;border-radius:12px;padding:18px 20px;margin-bottom:22px;">
            <div style="font-size:12px;color:#64748B;font-weight:600;margin-bottom:4px;">Seu e-mail de login:</div>
            <div style="font-size:14px;color:#0F1A2A;font-weight:700;font-family:monospace;margin-bottom:14px;">{destinatario_email}</div>
            <div style="font-size:12px;color:#64748B;font-weight:600;margin-bottom:6px;">Sua senha temporária:</div>
            <div style="display:inline-block;background:#0F1A2A;color:#F5B82E;font-family:monospace;font-size:20px;font-weight:800;letter-spacing:0.08em;padding:10px 16px;border-radius:8px;">
              {senha_temporaria}
            </div>
          </div>
          <p style="margin:0 0 24px 0;font-size:13px;line-height:1.5;color:#475569;background:#FEF3C7;border:1px solid #FDE68A;padding:12px 14px;border-radius:10px;">
            <strong>Troca obrigatória no primeiro acesso:</strong> Assim que você entrar com esta senha temporária, o portal pedirá para você escolher uma nova senha definitiva.
          </p>
          <a href="{portal_url}/login" style="display:inline-block;background:#0F1A2A;color:#FFFFFF;text-decoration:none;font-weight:700;font-size:14px;padding:12px 22px;border-radius:10px;">
            Acessar Portal Gold Corretora →
          </a>
        </div>
        <div style="background:#F8FAFC;padding:16px 28px;border-top:1px solid #E2E8F0;font-size:12px;color:#64748B;">
          Precisa de suporte? Responda este e-mail ou escreva para <a href="mailto:{reply_to}" style="color:#0F1A2A;font-weight:700;">{reply_to}</a>.
        </div>
      </div>
    </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    try:
        if port == 465:
            with smtplib.SMTP_SSL(host, port, timeout=10) as server:
                server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port, timeout=10) as server:
                if use_tls:
                    server.starttls()
                server.login(user, password)
                server.send_message(msg)
        return True, f"E-mail enviado com sucesso para {destinatario_email}."
    except Exception as e:
        logger.warning(f"Falha ao enviar e-mail SMTP para {destinatario_email}: {e}")
        return False, f"Falha no envio SMTP: {e}"

# ==========================================================
# AUTENTICAÇÃO E SESSÕES
# ==========================================================
def autenticar_usuario(email: str, senha: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    ph = "%s" if is_pg else "?"

    cur.execute(f"SELECT * FROM {tb_users} WHERE LOWER(email) = {ph};", (email.strip().lower(),))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None, "Credenciais inválidas. Verifique seu e-mail e senha."

    user_dict = dict(row)
    if not bool(user_dict.get("ativo", True)):
        conn.close()
        return None, "Este acesso foi desativado pelo administrador."

    if not verify_password(senha, user_dict.get("senha_hash", "")):
        conn.close()
        return None, "Credenciais inválidas. Verifique seu e-mail e senha."

    # Atualiza ultimo_login
    cur.execute(f"UPDATE {tb_users} SET ultimo_login = CURRENT_TIMESTAMP WHERE id = {ph};", (user_dict["id"],))
    conn.commit()
    conn.close()

    return _normalize_user(user_dict, is_pg), None

def buscar_usuario_por_email(email: str) -> Optional[Dict[str, Any]]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    ph = "%s" if is_pg else "?"
    cur.execute(f"SELECT * FROM {tb_users} WHERE LOWER(email) = {ph};", (email.strip().lower(),))
    row = cur.fetchone()
    conn.close()
    return _normalize_user(row, is_pg) if row else None

def buscar_usuario_por_id(usuario_id: int) -> Optional[Dict[str, Any]]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    ph = "%s" if is_pg else "?"
    cur.execute(f"SELECT * FROM {tb_users} WHERE id = {ph};", (usuario_id,))
    row = cur.fetchone()
    conn.close()
    return _normalize_user(row, is_pg) if row else None

def definir_senha_temporaria_usuario(usuario_id: int, senha_temporaria: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Define uma senha temporária para o usuário, marca precisa_trocar_senha = True
    e revoga sessões anteriores para garantir segurança.
    """
    ensure_db_initialized()
    temp_pw = (senha_temporaria or "").strip() or gerar_senha_temporaria()
    atualizado = atualizar_usuario(
        usuario_id,
        {"senha": temp_pw, "precisa_trocar_senha": True}
    )
    return atualizado, temp_pw

def trocar_propria_senha(usuario_id: int, nova_senha: str, senha_atual: Optional[str] = None) -> Tuple[bool, str]:
    """
    Permite ao usuário logado definir sua nova senha definitiva e limpa precisa_trocar_senha = False.
    Se o usuário não estiver com precisa_trocar_senha=True e informar senha_atual, valida a senha atual.
    """
    ensure_db_initialized()
    if len(nova_senha.strip()) < 4:
        return False, "A nova senha deve ter pelo menos 4 caracteres."

    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    ph = "%s" if is_pg else "?"

    cur.execute(f"SELECT * FROM {tb_users} WHERE id = {ph};", (usuario_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "Usuário não encontrado."

    user_dict = dict(row)
    obrigatorio = bool(user_dict.get("precisa_trocar_senha", False))

    if not obrigatorio and senha_atual:
        if not verify_password(senha_atual, user_dict.get("senha_hash", "")):
            conn.close()
            return False, "A senha atual informada está incorreta."

    if verify_password(nova_senha, user_dict.get("senha_hash", "")):
        conn.close()
        return False, "A nova senha precisa ser diferente da senha temporária atual."

    pw_hash = hash_password(nova_senha)
    false_val = False if is_pg else 0
    cur.execute(
        f"UPDATE {tb_users} SET senha_hash = {ph}, precisa_trocar_senha = {ph}, updated_at = CURRENT_TIMESTAMP WHERE id = {ph};",
        (pw_hash, false_val, usuario_id)
    )
    conn.commit()
    conn.close()
    return True, "Senha atualizada com sucesso!"

def criar_sessao(usuario_id: int, ip: str = "", user_agent: str = "", dias_validade: int = 7) -> str:
    ensure_db_initialized()
    raw_token = secrets.token_urlsafe(48)
    t_hash = hash_token(raw_token)
    expires = datetime.now(timezone.utc) + timedelta(days=dias_validade)

    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_sess = "schema_auth.sessoes" if is_pg else "auth_sessoes"

    if is_pg:
        cur.execute(
            f"INSERT INTO {tb_sess} (usuario_id, token_hash, ip, user_agent, expires_at) VALUES (%s, %s, %s, %s, %s);",
            (usuario_id, t_hash, ip, user_agent, expires)
        )
    else:
        cur.execute(
            f"INSERT INTO {tb_sess} (usuario_id, token_hash, ip, user_agent, expires_at) VALUES (?, ?, ?, ?, ?);",
            (usuario_id, t_hash, ip, user_agent, expires.isoformat())
        )
    conn.commit()
    conn.close()
    return raw_token

def validar_sessao_token(raw_token: str) -> Optional[Dict[str, Any]]:
    if not raw_token:
        return None
    ensure_db_initialized()
    t_hash = hash_token(raw_token)

    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_sess = "schema_auth.sessoes" if is_pg else "auth_sessoes"
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    tb_cargos = "schema_auth.cargos" if is_pg else "auth_cargos"
    ph = "%s" if is_pg else "?"

    cur.execute(
        f"""
        SELECT s.expires_at, u.*, c.nome as cargo_nome, c.permissoes as cargo_permissoes
        FROM {tb_sess} s
        JOIN {tb_users} u ON u.id = s.usuario_id
        LEFT JOIN {tb_cargos} c ON c.codigo = u.cargo
        WHERE s.token_hash = {ph};
        """,
        (t_hash,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    d = dict(row)
    if not bool(d.get("ativo", True)):
        return None

    # Valida expiração
    exp = d.get("expires_at")
    now = datetime.now(timezone.utc)
    if isinstance(exp, str):
        try:
            exp_dt = datetime.fromisoformat(exp.replace("Z", "+00:00"))
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
            if exp_dt < now:
                return None
        except Exception:
            pass
    elif isinstance(exp, datetime):
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp < now:
            return None

    user = _normalize_user(d, is_pg)
    cargo_perms = _parse_json_field(d.get("cargo_permissoes"), [])
    extras = user.get("permissoes_extras", [])
    todas_perms = list(set(cargo_perms + extras))
    user["permissoes"] = todas_perms
    user["cargo_nome"] = d.get("cargo_nome") or user["cargo"]
    return user

def revogar_sessao(raw_token: str):
    if not raw_token:
        return
    ensure_db_initialized()
    t_hash = hash_token(raw_token)
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_sess = "schema_auth.sessoes" if is_pg else "auth_sessoes"
    ph = "%s" if is_pg else "?"
    cur.execute(f"DELETE FROM {tb_sess} WHERE token_hash = {ph};", (t_hash,))
    conn.commit()
    conn.close()

def revogar_todas_sessoes_usuario(usuario_id: int):
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_sess = "schema_auth.sessoes" if is_pg else "auth_sessoes"
    ph = "%s" if is_pg else "?"
    cur.execute(f"DELETE FROM {tb_sess} WHERE usuario_id = {ph};", (usuario_id,))
    conn.commit()
    conn.close()

# ==========================================================
# GESTÃO DE USUÁRIOS E CARGOS
# ==========================================================
def listar_usuarios() -> List[Dict[str, Any]]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    tb_cargos = "schema_auth.cargos" if is_pg else "auth_cargos"
    tb_sess = "schema_auth.sessoes" if is_pg else "auth_sessoes"

    # Remove sessões já expiradas para manter a contagem real e limpa
    if is_pg:
        cur.execute(f"DELETE FROM {tb_sess} WHERE expires_at < CURRENT_TIMESTAMP;")
    else:
        now_iso = datetime.now(timezone.utc).isoformat()
        cur.execute(f"DELETE FROM {tb_sess} WHERE expires_at < ?;", (now_iso,))
    conn.commit()

    cur.execute(
        f"""
        SELECT u.*, c.nome as cargo_nome,
               (SELECT COUNT(*) FROM {tb_sess} s WHERE s.usuario_id = u.id) as sessoes_ativas
        FROM {tb_users} u
        LEFT JOIN {tb_cargos} c ON c.codigo = u.cargo
        ORDER BY u.ativo DESC, u.nome ASC;
        """
    )
    rows = cur.fetchall()
    conn.close()
    res = []
    for r in rows:
        u = _normalize_user(r, is_pg)
        u["cargo_nome"] = r["cargo_nome"] or u["cargo"]
        u["sessoes_ativas"] = r["sessoes_ativas"] or 0
        res.append(u)
    return res

def criar_usuario(dados: Dict[str, Any]) -> Dict[str, Any]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"

    nome = dados["nome"].strip()
    email = dados["email"].strip().lower()
    senha = dados["senha"]
    cargo = dados.get("cargo", "VENDEDOR").strip().upper()
    apps = dados.get("apps_permitidos", ["painel-vendedor", "gold-db-api", "cotador-web"])
    perms = dados.get("permissoes_extras", [])
    precisa_trocar = bool(dados.get("precisa_trocar_senha", False))
    pw_hash = hash_password(senha)

    if is_pg:
        from psycopg.types.json import Jsonb
        cur.execute(
            f"""
            INSERT INTO {tb_users} (nome, email, senha_hash, cargo, apps_permitidos, permissoes_extras, ativo, precisa_trocar_senha)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE, %s)
            RETURNING *;
            """,
            (nome, email, pw_hash, cargo, Jsonb(apps), Jsonb(perms), precisa_trocar)
        )
        row = cur.fetchone()
    else:
        cur.execute(
            f"""
            INSERT INTO {tb_users} (nome, email, senha_hash, cargo, apps_permitidos, permissoes_extras, ativo, precisa_trocar_senha)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?);
            """,
            (nome, email, pw_hash, cargo, json.dumps(apps), json.dumps(perms), 1 if precisa_trocar else 0)
        )
        uid = cur.lastrowid
        cur.execute(f"SELECT * FROM {tb_users} WHERE id = ?;", (uid,))
        row = cur.fetchone()

    conn.commit()
    conn.close()
    return _normalize_user(row, is_pg)

def atualizar_usuario(usuario_id: int, dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    ph = "%s" if is_pg else "?"

    cur.execute(f"SELECT * FROM {tb_users} WHERE id = {ph};", (usuario_id,))
    atual = cur.fetchone()
    if not atual:
        conn.close()
        return None
    atual_dict = dict(atual)

    sets = []
    params = []

    if "nome" in dados and dados["nome"]:
        sets.append(f"nome = {ph}")
        params.append(dados["nome"].strip())

    email_mudou = False
    if "email" in dados and dados["email"]:
        novo_email = dados["email"].strip().lower()
        if novo_email != (atual_dict.get("email") or "").lower():
            email_mudou = True
        sets.append(f"email = {ph}")
        params.append(novo_email)

    cargo_mudou = False
    if "cargo" in dados and dados["cargo"]:
        novo_cargo = dados["cargo"].strip().upper()
        if novo_cargo != (atual_dict.get("cargo") or "").upper():
            cargo_mudou = True
        sets.append(f"cargo = {ph}")
        params.append(novo_cargo)

    if "senha" in dados and dados["senha"]:
        sets.append(f"senha_hash = {ph}")
        params.append(hash_password(dados["senha"]))

    if "precisa_trocar_senha" in dados and dados["precisa_trocar_senha"] is not None:
        sets.append(f"precisa_trocar_senha = {ph}")
        params.append(bool(dados["precisa_trocar_senha"]) if is_pg else (1 if dados["precisa_trocar_senha"] else 0))

    if "apps_permitidos" in dados and dados["apps_permitidos"] is not None:
        sets.append(f"apps_permitidos = {ph}")
        if is_pg:
            from psycopg.types.json import Jsonb
            params.append(Jsonb(dados["apps_permitidos"]))
        else:
            params.append(json.dumps(dados["apps_permitidos"]))

    if "permissoes_extras" in dados and dados["permissoes_extras"] is not None:
        sets.append(f"permissoes_extras = {ph}")
        if is_pg:
            from psycopg.types.json import Jsonb
            params.append(Jsonb(dados["permissoes_extras"]))
        else:
            params.append(json.dumps(dados["permissoes_extras"]))

    if "ativo" in dados and dados["ativo"] is not None:
        sets.append(f"ativo = {ph}")
        params.append(bool(dados["ativo"]) if is_pg else (1 if dados["ativo"] else 0))

    if not sets:
        conn.close()
        return _normalize_user(atual_dict, is_pg)

    sets.append("updated_at = CURRENT_TIMESTAMP")
    params.append(usuario_id)

    try:
        cur.execute(f"UPDATE {tb_users} SET {', '.join(sets)} WHERE id = {ph};", params)
        conn.commit()
    except Exception as e:
        conn.close()
        raise ValueError(f"Não foi possível atualizar o usuário (verifique se o e-mail já está em uso): {e}")

    # Se desativou o usuário, trocou senha, trocou e-mail ou mudou cargo, revoga sessões ativas imediatamente
    if (
        ("ativo" in dados and not dados["ativo"])
        or ("senha" in dados and dados["senha"])
        or email_mudou
        or cargo_mudou
    ):
        tb_sess = "schema_auth.sessoes" if is_pg else "auth_sessoes"
        cur.execute(f"DELETE FROM {tb_sess} WHERE usuario_id = {ph};", (usuario_id,))
        conn.commit()

    cur.execute(f"SELECT * FROM {tb_users} WHERE id = {ph};", (usuario_id,))
    row = cur.fetchone()
    conn.close()
    return _normalize_user(row, is_pg) if row else None

def excluir_usuario(usuario_id: int) -> Optional[Dict[str, Any]]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_users = "schema_auth.usuarios" if is_pg else "auth_usuarios"
    tb_sess = "schema_auth.sessoes" if is_pg else "auth_sessoes"
    ph = "%s" if is_pg else "?"

    cur.execute(f"SELECT * FROM {tb_users} WHERE id = {ph};", (usuario_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None

    user_norm = _normalize_user(row, is_pg)
    cur.execute(f"DELETE FROM {tb_sess} WHERE usuario_id = {ph};", (usuario_id,))
    cur.execute(f"DELETE FROM {tb_users} WHERE id = {ph};", (usuario_id,))
    conn.commit()
    conn.close()
    return user_norm

def listar_cargos() -> List[Dict[str, Any]]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_cargos = "schema_auth.cargos" if is_pg else "auth_cargos"
    cur.execute(f"SELECT * FROM {tb_cargos} ORDER BY is_system DESC, nome ASC;")
    rows = cur.fetchall()
    conn.close()
    return [_normalize_role(r) for r in rows]

def salvar_cargo(dados: Dict[str, Any]) -> Dict[str, Any]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_cargos = "schema_auth.cargos" if is_pg else "auth_cargos"

    codigo = dados["codigo"].strip().upper().replace(" ", "_")
    nome = dados["nome"].strip()
    descricao = (dados.get("descricao") or "").strip()
    permissoes = dados.get("permissoes", [])
    apps_padrao = dados.get("apps_padrao", ["painel-vendedor", "gold-db-api", "cotador-web"])

    if is_pg:
        from psycopg.types.json import Jsonb
        cur.execute(
            f"""
            INSERT INTO {tb_cargos} (codigo, nome, descricao, permissoes, apps_padrao, is_system)
            VALUES (%s, %s, %s, %s, %s, FALSE)
            ON CONFLICT (codigo) DO UPDATE SET
                nome = EXCLUDED.nome,
                descricao = EXCLUDED.descricao,
                permissoes = EXCLUDED.permissoes,
                apps_padrao = EXCLUDED.apps_padrao
            RETURNING *;
            """,
            (codigo, nome, descricao, Jsonb(permissoes), Jsonb(apps_padrao))
        )
        row = cur.fetchone()
    else:
        cur.execute(
            f"""
            INSERT INTO {tb_cargos} (codigo, nome, descricao, permissoes, apps_padrao, is_system)
            VALUES (?, ?, ?, ?, ?, 0)
            ON CONFLICT(codigo) DO UPDATE SET
                nome = excluded.nome,
                descricao = excluded.descricao,
                permissoes = excluded.permissoes,
                apps_padrao = excluded.apps_padrao;
            """,
            (codigo, nome, descricao, json.dumps(permissoes), json.dumps(apps_padrao))
        )
        cur.execute(f"SELECT * FROM {tb_cargos} WHERE codigo = ?;", (codigo,))
        row = cur.fetchone()

    conn.commit()
    conn.close()
    return _normalize_role(row)

def excluir_cargo(codigo: str) -> bool:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_cargos = "schema_auth.cargos" if is_pg else "auth_cargos"
    ph = "%s" if is_pg else "?"
    cur.execute(f"DELETE FROM {tb_cargos} WHERE codigo = {ph} AND is_system = {'FALSE' if is_pg else '0'};", (codigo.upper(),))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# ==========================================================
# AUDITORIA ("QUEM ESTÁ LOGADO FAZENDO O QUÊ")
# ==========================================================
def registrar_auditoria(
    acao: str,
    usuario: Optional[Dict[str, Any]] = None,
    app: str = "gold-auth",
    metodo: str = "GET",
    rota: str = "/",
    detalhes: Optional[Dict[str, Any]] = None,
    ip: str = ""
):
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_aud = "schema_auth.auditoria" if is_pg else "auth_auditoria"

    u_id = usuario.get("id") if usuario else None
    u_nome = usuario.get("nome") if usuario else "Visitante / Sistema"
    u_email = usuario.get("email") if usuario else None
    u_cargo = usuario.get("cargo") if usuario else None
    det = detalhes or {}

    try:
        if is_pg:
            from psycopg.types.json import Jsonb
            cur.execute(
                f"""
                INSERT INTO {tb_aud} (usuario_id, usuario_nome, usuario_email, usuario_cargo, app, acao, metodo, rota, detalhes, ip)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (u_id, u_nome, u_email, u_cargo, app, acao, metodo, rota, Jsonb(det), ip)
            )
        else:
            cur.execute(
                f"""
                INSERT INTO {tb_aud} (usuario_id, usuario_nome, usuario_email, usuario_cargo, app, acao, metodo, rota, detalhes, ip)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (u_id, u_nome, u_email, u_cargo, app, acao, metodo, rota, json.dumps(det, ensure_ascii=False), ip)
            )
        conn.commit()
    except Exception as e:
        logger.warning(f"Erro ao gravar log de auditoria: {e}")
    finally:
        conn.close()

def listar_auditoria(
    busca: Optional[str] = None,
    app: Optional[str] = None,
    usuario_email: Optional[str] = None,
    limite: int = 100
) -> List[Dict[str, Any]]:
    ensure_db_initialized()
    conn, is_pg = get_connection()
    cur = conn.cursor()
    tb_aud = "schema_auth.auditoria" if is_pg else "auth_auditoria"
    ph = "%s" if is_pg else "?"

    where = []
    params = []

    if app and app != "TODOS":
        where.append(f"app = {ph}")
        params.append(app)

    if usuario_email and usuario_email != "TODOS":
        where.append(f"usuario_email = {ph}")
        params.append(usuario_email)

    if busca and busca.strip():
        t = f"%{busca.strip()}%"
        if is_pg:
            where.append("(usuario_nome ILIKE %s OR acao ILIKE %s OR rota ILIKE %s OR usuario_email ILIKE %s)")
        else:
            where.append("(usuario_nome LIKE ? OR acao LIKE ? OR rota LIKE ? OR usuario_email LIKE ?)")
        params.extend([t, t, t, t])

    w_sql = ("WHERE " + " AND ".join(where)) if where else ""
    cur.execute(f"SELECT * FROM {tb_aud} {w_sql} ORDER BY created_at DESC LIMIT {int(limite)};", params)
    rows = cur.fetchall()
    conn.close()

    res = []
    for r in rows:
        d = dict(r)
        d["detalhes"] = _parse_json_field(d.get("detalhes"), {})
        res.append(d)
    return res
