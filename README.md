# Gold Auth Gateway — Guia de Deploy no Coolify

Serviço central de Single Sign-On (SSO), Controle de Cargos/Permissões e Auditoria em Tempo Real para todos os aplicativos da **Gold Corretora** (`*.goldcorretora.com.br`).

---

## Passo 1: Subir o container `gold-auth` no Coolify

1. Suba esta pasta (`c:\gabriel-gold\gold-auth`) para um repositório no seu GitHub (ex: `gold-auth`) **ou** crie um recurso **Dockerfile / Git Repository** no Coolify apontando para ela.
2. Na configuração do serviço no Coolify:
   * **Domains:** `https://auth.goldcorretora.com.br`
   * **Port Exposes / Network Port:** `8010`
3. Em **Environment Variables** do `gold-auth` no Coolify, cole:
   ```env
   PORT=8010
   ENV=production
   DATABASE_URL=postgresql://postgres:SUA_SENHA_DO_POSTGRES@SEU_HOST_POSTGRES:5432/postgres
   AUTH_SECRET_KEY=gere-uma-chave-forte-aqui-gold-2026
   COOKIE_DOMAIN=.goldcorretora.com.br
   COOKIE_SECURE=true
   PUBLIC_AUTH_URL=https://auth.goldcorretora.com.br
   DEFAULT_REDIRECT_URL=https://painel.goldcorretora.com.br
   ADMIN_INITIAL_NAME=Gabriel Gold
   ADMIN_INITIAL_EMAIL=admin@goldcorretora.com.br
   ADMIN_INITIAL_PASSWORD=SuaSenhaForteAqui
   ```
   *(Dica: use a mesma `DATABASE_URL` que já está configurada no serviço `gold-db-api`. O `gold-auth` criará automaticamente o schema isolado `schema_auth` sem tocar nas tabelas de leads ou carteira).*
4. Clique em **Deploy**.

---

## Passo 2: Declarar o Middleware `gold-auth` no Traefik

No Coolify, dentro da configuração do serviço **`gold-auth`** (aba **General** → seção **Container Labels**), adicione estas 3 linhas de Labels do Traefik para registrar o middleware globalmente:

```ini
traefik.http.middlewares.gold-auth.forwardauth.address=http://localhost:8010/api/auth/verify
traefik.http.middlewares.gold-auth.forwardauth.trustForwardHeader=true
traefik.http.middlewares.gold-auth.forwardauth.authResponseHeaders=X-Gold-User-Id,X-Gold-User-Name,X-Gold-User-Email,X-Gold-User-Role,X-Gold-User-Permissions
```
> **Nota importante sobre o endereço interno no Coolify:**
> Se o Traefik do Coolify rodar em outro container (padrão `coolify-proxy`), substitua `http://localhost:8010/api/auth/verify` por `https://auth.goldcorretora.com.br/api/auth/verify` (assim o Traefik consulta via URL sem depender do nome aleatório do container interno):
> ```ini
> traefik.http.middlewares.gold-auth.forwardauth.address=https://auth.goldcorretora.com.br/api/auth/verify
> traefik.http.middlewares.gold-auth.forwardauth.trustForwardHeader=true
> traefik.http.middlewares.gold-auth.forwardauth.authResponseHeaders=X-Gold-User-Id,X-Gold-User-Name,X-Gold-User-Email,X-Gold-User-Role,X-Gold-User-Permissions
> ```

---

## Passo 3: Proteger o `painel-vendedor` (ou qualquer outro App) em 15 segundos

Para colocar a catraca SSO na frente do **Painel do Vendedor** (ou qualquer app que você criar no futuro):

1. Abra o aplicativo no Coolify (ex: `painel-vendedor`).
2. Role até **Container Labels** (ou ative *Custom Labels*).
3. Na linha do router HTTP/HTTPS do aplicativo (ex: `traefik.http.routers.https-0-<id>.middlewares`), adicione `gold-auth@docker` (ou se estiver usando o gerador padrão do Coolify, basta adicionar a label do middleware no router do domínio).
4. **No `painel-vendedor`**, adicione a variável de ambiente (opcional, já tem fallback padrão):
   ```env
   VITE_AUTH_URL=https://auth.goldcorretora.com.br
   ```

---

## Como funciona no dia a dia?

* **Painel Admin & Auditoria:** Acesse `https://auth.goldcorretora.com.br/admin`
  * **Aba Atividade ao Vivo:** Mostra em tempo real quem fez login, quem abriu qual lead, quem disparou WhatsApp e quem mudou status de proposta.
  * **Aba Vendedores & Equipe:** Crie usuários, escolha quais aplicativos cada um pode acessar (`painel-vendedor`, `carteira`, etc.) ou bloqueie em 1 clique (derruba todas as sessões ativas do vendedor na hora).
  * **Aba Cargos & Permissões:** Crie quantos cargos novos quiser (ex: `FINANCEIRO`, `POS_VENDA`, `AUDITOR`) e defina as permissões de cada um.
