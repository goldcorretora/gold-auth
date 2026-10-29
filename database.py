import os
import json
import hmac
import hashlib
import secrets
import logging
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("gold.auth.db")

def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cotador_gold")

def is_postgres_url(url: str) -> bool:
    return url.startswith("postgresql://") or url.startswith("postgres://")

def get_connection():
    url = get_database_url()
    if is_postgres_url(url):
        try:
            import psycopg
            from psycopg.rows import dict_row
            conn = psycopg.connect(url, row_factory=dict_row, connect_timeout=3)
            return conn, True
        except Exception as e:
            logger.warning(f"PostgreSQL inacessível ({e}). Usando SQLite local resiliente...")
            return get_sqlite_connection(), False
    else:
        return get_sqlite_connection(), False

def get_sqlite_connection():
    import sqlite3
    db_path = os.getenv("SQLITE_PATH", "gold_auth_local.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

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
    logger.info(f"Inicializando schema_auth (Modo: {'PostgreSQL' if is_pg else 'SQLite'})...")

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
                ultimo_login TIMESTAMPTZ,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );

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

            CREATE INDEX IF NOT EXISTS idx_auth_sessoes_token ON auth_sessoes(token_hash);
            CREATE INDEX IF NOT EXISTS idx_auth_auditoria_created ON auth_auditoria(created_at DESC);
        """)

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
                INSERT INTO {tb_users} (nome, email, senha_hash, cargo, apps_permitidos, permissoes_extras, ativo)
                VALUES (%s, %s, %s, 'ADMIN', %s, %s, TRUE);
                """,
                (admin_name, admin_email, pw_hash, Jsonb(["*"]), Jsonb(["*"]))
            )
        else:
            cur.execute(
                f"""
                INSERT INTO {tb_users} (nome, email, senha_hash, cargo, apps_permitidos, permissoes_extras, ativo)
                VALUES (?, ?, ?, 'ADMIN', ?, ?, 1);
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
    return d

def _normalize_role(row: Any) -> Dict[str, Any]:
    d = dict(row)
    d["permissoes"] = _parse_json_field(d.get("permissoes"), [])
    d["apps_padrao"] = _parse_json_field(d.get("apps_padrao"), [])
    d["is_system"] = bool(d.get("is_system", False))
    return d

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
    pw_hash = hash_password(senha)

    if is_pg:
        from psycopg.types.json import Jsonb
        cur.execute(
            f"""
            INSERT INTO {tb_users} (nome, email, senha_hash, cargo, apps_permitidos, permissoes_extras, ativo)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
            RETURNING *;
            """,
            (nome, email, pw_hash, cargo, Jsonb(apps), Jsonb(perms))
        )
        row = cur.fetchone()
    else:
        cur.execute(
            f"""
            INSERT INTO {tb_users} (nome, email, senha_hash, cargo, apps_permitidos, permissoes_extras, ativo)
            VALUES (?, ?, ?, ?, ?, ?, 1);
            """,
            (nome, email, pw_hash, cargo, json.dumps(apps), json.dumps(perms))
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

    sets = []
    params = []

    if "nome" in dados and dados["nome"]:
        sets.append(f"nome = {ph}")
        params.append(dados["nome"].strip())

    if "email" in dados and dados["email"]:
        sets.append(f"email = {ph}")
        params.append(dados["email"].strip().lower())

    if "cargo" in dados and dados["cargo"]:
        sets.append(f"cargo = {ph}")
        params.append(dados["cargo"].strip().upper())

    if "senha" in dados and dados["senha"]:
        sets.append(f"senha_hash = {ph}")
        params.append(hash_password(dados["senha"]))

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
        return None

    sets.append("updated_at = CURRENT_TIMESTAMP")
    params.append(usuario_id)

    cur.execute(f"UPDATE {tb_users} SET {', '.join(sets)} WHERE id = {ph};", params)
    conn.commit()

    # Se desativou o usuário ou trocou senha, revoga sessões ativas imediatamente
    if ("ativo" in dados and not dados["ativo"]) or ("senha" in dados and dados["senha"]):
        tb_sess = "schema_auth.sessoes" if is_pg else "auth_sessoes"
        cur.execute(f"DELETE FROM {tb_sess} WHERE usuario_id = {ph};", (usuario_id,))
        conn.commit()

    cur.execute(f"SELECT * FROM {tb_users} WHERE id = {ph};", (usuario_id,))
    row = cur.fetchone()
    conn.close()
    return _normalize_user(row, is_pg) if row else None

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
    apps_padrao = dados.get("apps_padrao", ["painel-vendedor"])

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
