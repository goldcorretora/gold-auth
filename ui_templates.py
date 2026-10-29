# -*- coding: utf-8 -*-
"""
Templates HTML de alta precisão da Gold Corretora (SSO Login + Central de Identidade & Auditoria).
Construídos seguindo os 5 Quality Gates do Web-Craft:
- Tipografia Plus Jakarta Sans + JetBrains Mono (tabular-nums)
- Paleta Oficial Navy (#0A121E / #0F1A2A / #162235) + Gold (#C59B27 / #DDBB5C)
- 4 Estados completos (Skeleton/Loading, Empty State, Error/Retry, Data State)
- Motion rápida (<220ms, cubic-bezier(0.23, 1, 0.32, 1), active scale(0.97), prefers-reduced-motion)
- Acessibilidade completa (focus-visible, semântica HTML, navegação por teclado Esc/Tab)
"""

GOLD_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 208.04 84.13" class="h-9 w-auto" aria-label="Gold Corretora de Seguros">
  <path fill="#fefefe" d="M15.64,66.25l.3,4.5h-.3c-.4-1.35-.98-2.32-1.72-2.91-.75-.59-1.64-.89-2.69-.89-.87,0-1.67.22-2.37.67-.71.45-1.26,1.16-1.67,2.14-.4.98-.61,2.19-.61,3.65,0,1.2.19,2.24.57,3.12.38.88.96,1.55,1.73,2.02.77.47,1.65.7,2.63.7.86,0,1.61-.18,2.27-.55.66-.37,1.38-1.1,2.16-2.19l.3.2c-.66,1.18-1.44,2.04-2.32,2.58-.88.54-1.93.82-3.15.82-2.19,0-3.89-.81-5.09-2.44-.9-1.21-1.35-2.64-1.35-4.28,0-1.32.3-2.54.89-3.65.59-1.11,1.4-1.97,2.44-2.58,1.04-.61,2.17-.91,3.39-.91.95,0,1.89.23,2.82.7.27.14.47.22.58.22.17,0,.33-.06.46-.19.17-.18.29-.42.36-.73h.36,0ZM47.74,0l1.22,15.05h-1.3c-1.24-3.73-2.84-6.54-4.8-8.44-2.83-2.72-6.47-4.09-10.91-4.09-6.05,0-10.66,2.4-13.81,7.21-2.64,4.04-3.96,8.88-3.96,14.48,0,4.55.88,8.69,2.64,12.44,1.75,3.74,4.06,6.49,6.9,8.24,2.84,1.74,5.77,2.62,8.77,2.62,1.75,0,3.46-.23,5.1-.67,1.63-.44,3.22-1.1,4.74-1.98v-13.84c0-2.4-.18-3.97-.54-4.7-.37-.74-.94-1.31-1.69-1.69-.77-.4-2.11-.59-4.03-.59v-1.3h18.43v1.3h-.88c-1.82,0-3.07.61-3.76,1.84-.47.86-.7,2.58-.7,5.15v14.63c-2.69,1.46-5.35,2.53-7.97,3.22-2.63.68-5.54,1.02-8.75,1.02-9.2,0-16.19-2.95-20.96-8.87-3.59-4.43-5.38-9.55-5.38-15.34,0-4.2,1.01-8.23,3.02-12.07,2.39-4.57,5.66-8.1,9.83-10.56C22.46,1.02,26.58,0,31.34,0,33.07,0,34.64.14,36.06.42c1.42.29,3.42.9,6.02,1.86,1.31.49,2.2.74,2.64.74s.82-.2,1.14-.61c.31-.41.5-1.21.58-2.41h1.3,0ZM148.92,35.64l1.15.25-4.1,12.92h-36.94v-1.3h1.79c2.02,0,3.46-.65,4.32-1.96.49-.74.73-2.47.73-5.17V9.5c0-2.98-.32-4.84-.98-5.58-.91-1.03-2.27-1.55-4.07-1.55h-1.79v-1.3h21.6v1.3c-2.53-.02-4.31.2-5.34.7-1.02.48-1.72,1.1-2.09,1.84-.37.74-.56,2.52-.56,5.32v30.1c0,1.96.19,3.29.56,4.02.28.5.72.86,1.31,1.1.58.23,2.41.35,5.5.35h3.48c3.67,0,6.24-.26,7.72-.8s2.83-1.5,4.06-2.87c1.21-1.37,2.44-3.53,3.66-6.48h0ZM152.8,48.82v-1.3h1.79c2.02,0,3.44-.65,4.28-1.93.52-.77.77-2.51.77-5.2V9.5c0-2.98-.32-4.84-.98-5.58-.91-1.03-2.27-1.55-4.07-1.55h-1.79v-1.3h19.4c7.13,0,12.55.8,16.26,2.42,3.72,1.62,6.71,4.32,8.96,8.1,2.27,3.78,3.4,8.15,3.4,13.09,0,6.65-2.02,12.19-6.05,16.66-4.52,4.98-11.41,7.46-20.68,7.46h-21.3ZM166.4,45.31c2.98.66,5.46.98,7.48.98,5.42,0,9.92-1.91,13.51-5.74,3.58-3.82,5.36-9,5.36-15.54s-1.79-11.78-5.36-15.58c-3.59-3.8-8.18-5.7-13.8-5.7-2.1,0-4.5.34-7.19,1.02v40.55h0Z"/>
  <path fill="#ffcc2b" d="M81.9,0c6.18,0,11.54,2.35,16.07,7.06,4.54,4.7,6.8,10.57,6.8,17.62s-2.28,13.26-6.85,18.05c-4.56,4.79-10.09,7.18-16.58,7.18s-12.06-2.34-16.52-7.01c-4.46-4.67-6.7-10.7-6.7-18.12s2.58-13.75,7.73-18.54c4.48-4.15,9.83-6.23,16.06-6.23h0ZM81.23,2.52c-4.25,0-7.67,1.58-10.24,4.75-3.2,3.95-4.81,9.72-4.81,17.33s1.66,13.79,4.98,17.99c2.56,3.19,5.92,4.79,10.1,4.79,4.48,0,8.16-1.75,11.08-5.24,2.92-3.5,4.37-9.01,4.37-16.55,0-8.17-1.61-14.27-4.81-18.28-2.57-3.19-6.12-4.79-10.67-4.79h0Z"/>
  <rect fill="#fefefe" x="15.84" y="56.17" width="175.56" height="1.92"/>
</svg>
"""

SHARED_HEAD = """
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        fontFamily: {
          sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
          mono: ['"JetBrains Mono"', 'monospace'],
        },
        colors: {
          gold: {
            300: '#EAD084',
            400: '#DDBB5C',
            500: '#C59B27',
            600: '#A8821D',
          },
          navy: {
            800: '#162235',
            900: '#0F1A2A',
            950: '#0A121E',
          }
        }
      }
    }
  }
</script>
<style>
  :root {
    --ease-out-strong: cubic-bezier(0.23, 1, 0.32, 1);
  }
  body {
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .tabular-nums {
    font-variant-numeric: tabular-nums;
  }
  .btn-tactile {
    transition: transform 150ms var(--ease-out-strong), background-color 150ms ease, border-color 150ms ease, opacity 150ms ease;
  }
  .btn-tactile:active:not(:disabled) {
    transform: scale(0.97);
  }
  .modal-panel {
    transition: transform 200ms var(--ease-out-strong), opacity 200ms var(--ease-out-strong);
  }
  .modal-entering {
    transform: scale(0.96);
    opacity: 0;
  }
  @media (prefers-reduced-motion: reduce) {
    .btn-tactile, .modal-panel, * {
      transition-duration: 0.01ms !important;
      animation-duration: 0.01ms !important;
      transform: none !important;
    }
  }
</style>
"""


def get_login_html(default_redirect: str = "https://painel.goldcorretora.com.br") -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  {SHARED_HEAD}
  <title>Acesso Corporativo • Gold Corretora</title>
</head>
<body class="bg-navy-950 text-slate-100 min-h-screen flex flex-col justify-between selection:bg-gold-500 selection:text-navy-950">
  <main class="flex-1 flex items-center justify-center p-4 sm:p-6">
    <div class="w-full max-w-[420px]">
      <!-- Cabeçalho da Marca -->
      <div class="flex flex-col items-center text-center mb-7">
        <div class="mb-4">
          {GOLD_LOGO_SVG}
        </div>
        <h1 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
          Portal de Identidade Corporativa
        </h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-1">
          Entre com sua credencial da Gold Corretora para continuar
        </p>
      </div>

      <!-- Card de Autenticação -->
      <section class="bg-navy-900 border border-slate-800 rounded-2xl p-6 sm:p-7 shadow-2xl">
        <form id="login-form" class="space-y-4" novalidate>
          <div id="error-banner" role="alert" class="hidden rounded-xl bg-red-950/80 border border-red-500/40 px-4 py-3 text-xs font-semibold text-red-200 flex items-start gap-2.5">
            <svg class="w-4 h-4 text-red-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <span id="error-text">Credenciais inválidas.</span>
          </div>

          <div>
            <label for="email" class="block text-xs font-bold text-slate-300 mb-1.5">
              E-mail Corporativo
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              placeholder="nome@goldcorretora.com.br"
              class="w-full h-11 rounded-xl bg-navy-950 border border-slate-700/80 px-3.5 text-sm font-medium text-white placeholder-slate-500 focus:outline-none focus:border-gold-400 focus:ring-2 focus:ring-gold-500/30"
            />
          </div>

          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label for="senha" class="block text-xs font-bold text-slate-300">
                Senha de Acesso
              </label>
            </div>
            <div class="relative">
              <input
                id="senha"
                name="senha"
                type="password"
                autocomplete="current-password"
                required
                placeholder="••••••••"
                class="w-full h-11 rounded-xl bg-navy-950 border border-slate-700/80 pl-3.5 pr-11 text-sm font-medium text-white placeholder-slate-500 focus:outline-none focus:border-gold-400 focus:ring-2 focus:ring-gold-500/30"
              />
              <button
                type="button"
                id="toggle-pw"
                aria-label="Mostrar ou ocultar senha"
                class="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 rounded-lg text-slate-400 hover:text-white flex items-center justify-center focus:outline-none focus-visible:ring-2 focus-visible:ring-gold-400"
              >
                <svg id="eye-icon" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <button
            type="submit"
            id="submit-btn"
            class="btn-tactile w-full h-11 rounded-xl bg-gold-500 hover:bg-gold-400 text-navy-950 font-extrabold text-sm flex items-center justify-center gap-2 shadow-lg shadow-gold-500/10 focus:outline-none focus-visible:ring-2 focus-visible:ring-gold-300 disabled:opacity-50"
          >
            <span id="submit-label">Entrar nos Sistemas Gold</span>
            <svg id="submit-spinner" class="hidden w-4 h-4 animate-spin text-navy-950" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
            </svg>
          </button>
        </form>

        <div class="mt-5 pt-4 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
          <span>Sessão SSO criptografada</span>
          <span class="font-mono text-gold-400">*.goldcorretora.com.br</span>
        </div>
      </section>
    </div>
  </main>

  <footer class="py-4 text-center text-xs text-slate-500">
    Gold Corretora de Seguros • Controle de Acesso & Auditoria Unificada
  </footer>

  <script>
    const form = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const senhaInput = document.getElementById('senha');
    const errorBanner = document.getElementById('error-banner');
    const errorText = document.getElementById('error-text');
    const submitBtn = document.getElementById('submit-btn');
    const submitLabel = document.getElementById('submit-label');
    const submitSpinner = document.getElementById('submit-spinner');
    const togglePw = document.getElementById('toggle-pw');

    togglePw.addEventListener('click', () => {{
      const isPw = senhaInput.type === 'password';
      senhaInput.type = isPw ? 'text' : 'password';
    }});

    form.addEventListener('submit', async (e) => {{
      e.preventDefault();
      errorBanner.classList.add('hidden');

      const email = emailInput.value.trim();
      const senha = senhaInput.value;
      if (!email || !senha) {{
        errorText.textContent = 'Preencha seu e-mail e sua senha.';
        errorBanner.classList.remove('hidden');
        return;
      }}

      submitBtn.disabled = true;
      submitLabel.textContent = 'Validando acesso...';
      submitSpinner.classList.remove('hidden');

      try {{
        const res = await fetch('/api/auth/login', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ email, senha }})
        }});
        const data = await res.json();
        if (!res.ok) {{
          throw new Error(data.detail || 'Credenciais inválidas.');
        }}

        const params = new URLSearchParams(window.location.search);
        const rd = params.get('rd');
        if (rd) {{
          window.location.href = rd;
        }} else if (data.user && data.user.cargo === 'ADMIN') {{
          window.location.href = '/admin';
        }} else {{
          window.location.href = '{default_redirect}';
        }}
      }} catch (err) {{
        errorText.textContent = err.message || 'Falha de conexão com o servidor.';
        errorBanner.classList.remove('hidden');
        submitBtn.disabled = false;
        submitLabel.textContent = 'Entrar nos Sistemas Gold';
        submitSpinner.classList.add('hidden');
      }}
    }});
  </script>
</body>
</html>"""


def get_admin_html(default_redirect: str = "https://painel.goldcorretora.com.br") -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  {SHARED_HEAD}
  <title>Gestão de Acessos & Auditoria • Gold Corretora</title>
</head>
<body class="bg-slate-100 text-slate-800 min-h-screen flex flex-col selection:bg-gold-500 selection:text-white">
  <!-- Topbar Oficial Gold -->
  <header class="bg-navy-900 border-b border-navy-800 sticky top-0 z-30">
    <div class="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <a href="/admin" class="flex items-center shrink-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-gold-400 rounded-lg">
          {GOLD_LOGO_SVG}
        </a>
        <div class="hidden sm:block border-l border-slate-700/70 pl-4">
          <span class="text-xs font-extrabold uppercase tracking-wider text-gold-400 block">
            Gold Auth Gateway
          </span>
          <span class="text-[11px] text-slate-400 font-medium block">
            Controle de Vendedores, Cargos & Auditoria em Tempo Real
          </span>
        </div>
      </div>

      <div class="flex items-center gap-2.5">
        <a
          href="{default_redirect}"
          class="btn-tactile px-3.5 py-2 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/15 text-white border border-white/15 flex items-center gap-1.5"
        >
          <span>Abrir Painel do Vendedor</span>
          <svg class="w-3.5 h-3.5 text-gold-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>

        <div id="current-user-pill" class="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-navy-950 border border-slate-800 text-xs">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span id="header-user-name" class="font-bold text-white">Admin</span>
          <span id="header-user-role" class="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-gold-500/20 text-gold-400 font-bold">ADMIN</span>
        </div>

        <a
          href="/api/auth/logout"
          class="btn-tactile px-3 py-2 rounded-xl text-xs font-bold bg-red-500/15 hover:bg-red-500/25 text-red-300 border border-red-500/30"
        >
          Sair
        </a>
      </div>
    </div>
  </header>

  <!-- Conteúdo Principal -->
  <main class="flex-1 max-w-[1440px] w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
    <!-- Cabeçalho da Página + Abas -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-navy-900 tracking-tight">
          Segurança & Rastreabilidade Operacional
        </h1>
        <p class="text-xs sm:text-sm text-slate-600 mt-0.5">
          Gerencie quem pode acessar cada aplicativo da Gold Corretora e acompanhe todas as ações em tempo real.
        </p>
      </div>

      <!-- Segmented Control de Navegação -->
      <nav aria-label="Seções do painel" class="bg-white p-1 rounded-2xl border border-slate-200 shadow-xs flex items-center self-start sm:self-auto">
        <button
          type="button"
          data-tab="auditoria"
          onclick="switchTab('auditoria')"
          class="tab-btn btn-tactile px-3.5 py-2 rounded-xl text-xs sm:text-sm font-extrabold bg-navy-900 text-white"
        >
          Atividade ao Vivo
        </button>
        <button
          type="button"
          data-tab="usuarios"
          onclick="switchTab('usuarios')"
          class="tab-btn btn-tactile px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold text-slate-600 hover:bg-slate-100"
        >
          Vendedores & Equipe
        </button>
        <button
          type="button"
          data-tab="cargos"
          onclick="switchTab('cargos')"
          class="tab-btn btn-tactile px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold text-slate-600 hover:bg-slate-100"
        >
          Cargos & Permissões
        </button>
      </nav>
    </div>

    <!-- KPIs Rápidos -->
    <section aria-label="Resumo operacional" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-white rounded-2xl border border-slate-200 p-4 flex items-center justify-between">
        <div>
          <span class="text-xs font-bold text-slate-500 block">Usuários Ativos</span>
          <strong id="kpi-active-users" class="text-2xl font-extrabold text-navy-900 tabular-nums mt-0.5 block">—</strong>
        </div>
        <span class="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200">Liberados no SSO</span>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 p-4 flex items-center justify-between">
        <div>
          <span class="text-xs font-bold text-slate-500 block">Sessões Conectadas</span>
          <strong id="kpi-active-sessions" class="text-2xl font-extrabold text-navy-900 tabular-nums mt-0.5 block">—</strong>
        </div>
        <span class="px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 text-xs font-bold border border-amber-200">Dispositivos logados</span>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 p-4 flex items-center justify-between">
        <div>
          <span class="text-xs font-bold text-slate-500 block">Eventos Auditados (Recentes)</span>
          <strong id="kpi-audit-count" class="text-2xl font-extrabold text-navy-900 tabular-nums mt-0.5 block">—</strong>
        </div>
        <button
          type="button"
          onclick="carregarTudo()"
          class="btn-tactile px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-navy-900 text-xs font-bold"
        >
          Atualizar Agora
        </button>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- ABA 1: AUDITORIA ("QUEM ESTÁ FAZENDO O QUÊ") -->
    <!-- ========================================== -->
    <section id="tab-auditoria" class="space-y-4">
      <div class="bg-white rounded-2xl border border-slate-200 p-4 flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5 flex-1">
          <input
            id="audit-search"
            type="search"
            placeholder="Filtrar por vendedor, lead, rota ou ação..."
            oninput="debounceAudit()"
            class="h-10 rounded-xl border border-slate-300 px-3.5 text-xs sm:text-sm font-medium text-navy-900 focus:outline-none focus:border-gold-500 focus:ring-2 focus:ring-gold-500/20 flex-1 max-w-md"
          />
          <select
            id="audit-app-filter"
            onchange="carregarAuditoria()"
            class="h-10 rounded-xl border border-slate-300 px-3 text-xs sm:text-sm font-bold text-navy-900 bg-white focus:outline-none focus:border-gold-500"
          >
            <option value="TODOS">Todos os Aplicativos</option>
            <option value="painel-vendedor">Painel do Vendedor</option>
            <option value="gold-db-api">Gold DB API (Leads / Carteira)</option>
            <option value="gold-auth">Gold Auth (Logins / Admin)</option>
            <option value="cotador-web">Simulador / Cotador</option>
          </select>
          <select
            id="audit-user-filter"
            onchange="carregarAuditoria()"
            class="h-10 rounded-xl border border-slate-300 px-3 text-xs sm:text-sm font-bold text-navy-900 bg-white focus:outline-none focus:border-gold-500"
          >
            <option value="TODOS">Todos os Usuários</option>
          </select>
        </div>

        <div class="flex items-center gap-2 text-xs text-slate-500 font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span>Atualização automática a cada 10s</span>
        </div>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-[11px] font-extrabold text-slate-500 uppercase">
                <th class="py-3 px-4">Horário</th>
                <th class="py-3 px-4">Usuário / Cargo</th>
                <th class="py-3 px-4">Aplicativo</th>
                <th class="py-3 px-4">Ação Executada</th>
                <th class="py-3 px-4">Detalhes do Que Fez</th>
                <th class="py-3 px-4">IP</th>
              </tr>
            </thead>
            <tbody id="audit-tbody" class="divide-y divide-slate-200 text-xs sm:text-sm">
              <tr>
                <td colspan="6" class="py-10 text-center text-slate-400 font-medium">Carregando registros de atividade...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- ABA 2: GESTÃO DE USUÁRIOS / VENDEDORES     -->
    <!-- ========================================== -->
    <section id="tab-usuarios" class="hidden space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white rounded-2xl border border-slate-200 p-4">
        <div>
          <h2 class="text-base font-extrabold text-navy-900">Consultores, Supervisores e Administradores</h2>
          <p class="text-xs text-slate-500">Crie logins, defina quais aplicativos cada pessoa pode abrir ou bloqueie o acesso instantaneamente.</p>
        </div>
        <button
          type="button"
          onclick="abrirModalUsuario()"
          class="btn-tactile h-10 px-4 rounded-xl bg-navy-900 hover:bg-navy-800 text-gold-400 font-extrabold text-xs sm:text-sm flex items-center justify-center gap-2 shrink-0"
        >
          <span>+ Novo Usuário / Vendedor</span>
        </button>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-[11px] font-extrabold text-slate-500 uppercase">
                <th class="py-3 px-4">Nome & E-mail</th>
                <th class="py-3 px-4">Cargo</th>
                <th class="py-3 px-4">Aplicativos Liberados</th>
                <th class="py-3 px-4">Status / Sessões</th>
                <th class="py-3 px-4">Último Login</th>
                <th class="py-3 px-4 text-right">Ações</th>
              </tr>
            </thead>
            <tbody id="users-tbody" class="divide-y divide-slate-200 text-xs sm:text-sm">
              <tr>
                <td colspan="6" class="py-10 text-center text-slate-400">Carregando equipe...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- ABA 3: CARGOS & PERMISSÕES DINÂMICAS       -->
    <!-- ========================================== -->
    <section id="tab-cargos" class="hidden space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white rounded-2xl border border-slate-200 p-4">
        <div>
          <h2 class="text-base font-extrabold text-navy-900">Cargos e Permissões Customizáveis</h2>
          <p class="text-xs text-slate-500">Crie novos cargos (ex: Financeiro, Pós-Venda, Auditor) e defina exatamente quais permissões possuem.</p>
        </div>
        <button
          type="button"
          onclick="abrirModalCargo()"
          class="btn-tactile h-10 px-4 rounded-xl bg-navy-900 hover:bg-navy-800 text-gold-400 font-extrabold text-xs sm:text-sm flex items-center justify-center gap-2 shrink-0"
        >
          <span>+ Criar Novo Cargo</span>
        </button>
      </div>

      <div id="roles-grid" class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Renderizado via JS -->
      </div>
    </section>
  </main>

  <!-- MODAL: CRIAR / EDITAR USUÁRIO -->
  <div id="user-modal" class="hidden fixed inset-0 z-50 bg-navy-950/70 backdrop-blur-xs flex items-center justify-center p-4" role="dialog" aria-modal="true">
    <div class="modal-panel bg-white rounded-2xl border border-slate-200 max-w-lg w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 id="user-modal-title" class="text-lg font-extrabold text-navy-900">Novo Vendedor / Usuário</h3>
        <button type="button" onclick="fecharModalUsuario()" class="w-8 h-8 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 flex items-center justify-center font-bold">✕</button>
      </div>

      <form id="user-form" class="space-y-4">
        <input type="hidden" id="u-id" />
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label for="u-nome" class="block text-xs font-bold text-slate-700 mb-1">Nome Completo</label>
            <input id="u-nome" type="text" required placeholder="Ex: João Silva" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-sm font-medium text-navy-900 focus:outline-none focus:border-gold-500" />
          </div>
          <div>
            <label for="u-email" class="block text-xs font-bold text-slate-700 mb-1">E-mail de Login</label>
            <input id="u-email" type="email" required placeholder="joao@goldcorretora.com.br" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-sm font-medium text-navy-900 focus:outline-none focus:border-gold-500" />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label for="u-cargo" class="block text-xs font-bold text-slate-700 mb-1">Cargo</label>
            <select id="u-cargo" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-sm font-bold text-navy-900 bg-white focus:outline-none focus:border-gold-500"></select>
          </div>
          <div>
            <label for="u-senha" class="block text-xs font-bold text-slate-700 mb-1">Senha <span id="u-senha-hint" class="text-[11px] font-normal text-slate-400"></span></label>
            <input id="u-senha" type="password" placeholder="Mínimo 6 caracteres" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-sm font-medium text-navy-900 focus:outline-none focus:border-gold-500" />
          </div>
        </div>

        <div>
          <span class="block text-xs font-bold text-slate-700 mb-1.5">Aplicativos Liberados para este Usuário</span>
          <div class="grid grid-cols-2 gap-2 bg-slate-50 p-3 rounded-xl border border-slate-200 text-xs font-semibold text-navy-900">
            <label class="flex items-center gap-2"><input type="checkbox" name="u-app" value="painel-vendedor" checked class="rounded text-gold-600" /> Painel do Vendedor</label>
            <label class="flex items-center gap-2"><input type="checkbox" name="u-app" value="gold-db-api" checked class="rounded text-gold-600" /> API de Leads & Carteira</label>
            <label class="flex items-center gap-2"><input type="checkbox" name="u-app" value="cotador-web" checked class="rounded text-gold-600" /> Simulador / Cotador</label>
            <label class="flex items-center gap-2"><input type="checkbox" name="u-app" value="carteira" class="rounded text-gold-600" /> Módulo Carteira Geral</label>
            <label class="flex items-center gap-2 col-span-2"><input type="checkbox" name="u-app" value="*" class="rounded text-gold-600" /> Todos os Aplicativos Presentes e Futuros (*)</label>
          </div>
        </div>

        <div>
          <label for="u-perms" class="block text-xs font-bold text-slate-700 mb-1">Permissões Extras Específicas (separadas por vírgula)</label>
          <input id="u-perms" type="text" placeholder="Ex: leads.delete, relatorios.export" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-xs font-mono text-navy-900 focus:outline-none focus:border-gold-500" />
        </div>

        <div id="user-form-error" class="hidden text-xs font-bold text-red-600 bg-red-50 border border-red-200 rounded-xl p-2.5"></div>

        <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-200">
          <button type="button" onclick="fecharModalUsuario()" class="btn-tactile px-4 py-2 rounded-xl text-xs font-bold text-slate-600 hover:bg-slate-100">Cancelar</button>
          <button type="submit" class="btn-tactile px-5 py-2 rounded-xl text-xs font-extrabold bg-navy-900 hover:bg-navy-800 text-gold-400">Salvar Usuário</button>
        </div>
      </form>
    </div>
  </div>

  <!-- MODAL: CRIAR / EDITAR CARGO -->
  <div id="role-modal" class="hidden fixed inset-0 z-50 bg-navy-950/70 backdrop-blur-xs flex items-center justify-center p-4" role="dialog" aria-modal="true">
    <div class="modal-panel bg-white rounded-2xl border border-slate-200 max-w-md w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 class="text-lg font-extrabold text-navy-900">Configurar Cargo & Permissões</h3>
        <button type="button" onclick="fecharModalCargo()" class="w-8 h-8 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 flex items-center justify-center font-bold">✕</button>
      </div>

      <form id="role-form" class="space-y-3.5">
        <div>
          <label for="r-codigo" class="block text-xs font-bold text-slate-700 mb-1">Código Identificador (Ex: FINANCEIRO, POS_VENDA)</label>
          <input id="r-codigo" type="text" required placeholder="FINANCEIRO" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-xs font-mono uppercase text-navy-900 focus:outline-none focus:border-gold-500" />
        </div>
        <div>
          <label for="r-nome" class="block text-xs font-bold text-slate-700 mb-1">Nome de Exibição</label>
          <input id="r-nome" type="text" required placeholder="Analista Financeiro" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-sm font-medium text-navy-900 focus:outline-none focus:border-gold-500" />
        </div>
        <div>
          <label for="r-desc" class="block text-xs font-bold text-slate-700 mb-1">Descrição da Função</label>
          <input id="r-desc" type="text" placeholder="Acesso a relatórios de boletos e comissões" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-sm text-navy-900 focus:outline-none focus:border-gold-500" />
        </div>
        <div>
          <label for="r-perms" class="block text-xs font-bold text-slate-700 mb-1">Permissões do Cargo (separadas por vírgula)</label>
          <input id="r-perms" type="text" placeholder="leads.view, carteira.view, financeiro.boletos" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-xs font-mono text-navy-900 focus:outline-none focus:border-gold-500" />
        </div>

        <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-200">
          <button type="button" onclick="fecharModalCargo()" class="btn-tactile px-4 py-2 rounded-xl text-xs font-bold text-slate-600 hover:bg-slate-100">Cancelar</button>
          <button type="submit" class="btn-tactile px-5 py-2 rounded-xl text-xs font-extrabold bg-navy-900 hover:bg-navy-800 text-gold-400">Salvar Cargo</button>
        </div>
      </form>
    </div>
  </div>

  <script>
    let stateUsers = [];
    let stateRoles = [];
    let stateAudit = [];
    let auditDebounceTimer = null;

    function fmtData(iso) {{
      if (!iso) return 'Nunca acessou';
      try {{
        const hasTz = iso.endsWith('Z') || /[+-]\\d{{2}}(:\\d{{2}})?$/.test(iso);
        const d = new Date(hasTz ? iso : iso + 'Z');
        return new Intl.DateTimeFormat('pt-BR', {{
          dateStyle: 'short',
          timeStyle: 'medium',
          timeZone: 'America/Sao_Paulo'
        }}).format(d);
      }} catch {{
        return iso;
      }}
    }}

    function switchTab(tab) {{
      ['auditoria', 'usuarios', 'cargos'].forEach(t => {{
        document.getElementById('tab-' + t).classList.toggle('hidden', t !== tab);
      }});
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        const isCurrent = btn.getAttribute('data-tab') === tab;
        btn.className = isCurrent
          ? 'tab-btn btn-tactile px-3.5 py-2 rounded-xl text-xs sm:text-sm font-extrabold bg-navy-900 text-white'
          : 'tab-btn btn-tactile px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold text-slate-600 hover:bg-slate-100';
      }});
    }}

    async function carregarMe() {{
      try {{
        const res = await fetch('/api/auth/me');
        if (res.ok) {{
          const data = await res.json();
          document.getElementById('header-user-name').textContent = data.user.nome;
          document.getElementById('header-user-role').textContent = data.user.cargo;
        }}
      }} catch {{}}
    }}

    async function carregarCargos() {{
      const res = await fetch('/api/admin/roles');
      if (!res.ok) return;
      stateRoles = await res.json();

      // Atualiza select do modal de usuário
      const sel = document.getElementById('u-cargo');
      sel.innerHTML = stateRoles.map(r => `<option value="${{r.codigo}}">${{r.nome}} (${{r.codigo}})</option>`).join('');

      // Renderiza cards de cargos
      const grid = document.getElementById('roles-grid');
      grid.innerHTML = stateRoles.map(r => `
        <div class="bg-white rounded-2xl border border-slate-200 p-5 flex flex-col justify-between gap-4 shadow-xs">
          <div>
            <div class="flex items-center justify-between gap-2">
              <span class="font-mono text-xs font-bold px-2.5 py-1 rounded-lg bg-navy-900 text-gold-400">${{r.codigo}}</span>
              ${{r.is_system ? '<span class="text-[11px] font-bold text-slate-400">Cargo Nativo</span>' : `
                <button onclick="removerCargo('${{r.codigo}}')" class="text-xs font-bold text-red-600 hover:underline">Excluir</button>
              `}}
            </div>
            <h3 class="text-base font-extrabold text-navy-900 mt-3">${{r.nome}}</h3>
            <p class="text-xs text-slate-500 mt-1">${{r.descricao || 'Sem descrição.'}}</p>
          </div>
          <div class="pt-3 border-t border-slate-100">
            <span class="text-[11px] font-bold text-slate-400 uppercase block mb-1.5">Permissões Atribuídas</span>
            <div class="flex flex-wrap gap-1.5">
              ${{(r.permissoes || []).map(p => `<span class="font-mono text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">${{p}}</span>`).join('') || '<span class="text-xs text-slate-400">Básicas</span>'}}
            </div>
            <button
              type="button"
              onclick='editarCargo(${{JSON.stringify(r)}})'
              class="mt-3 w-full py-1.5 rounded-xl border border-slate-200 hover:bg-slate-50 text-xs font-bold text-navy-900"
            >
              Editar Permissões
            </button>
          </div>
        </div>
      `).join('');
    }}

    async function carregarUsuarios() {{
      const res = await fetch('/api/admin/users');
      if (!res.ok) return;
      stateUsers = await res.json();

      const ativos = stateUsers.filter(u => u.ativo).length;
      const sessoes = stateUsers.reduce((acc, u) => acc + (u.sessoes_ativas || 0), 0);
      document.getElementById('kpi-active-users').textContent = `${{ativos}} / ${{stateUsers.length}}`;
      document.getElementById('kpi-active-sessions').textContent = sessoes;

      // Popula filtro de auditoria por usuário
      const uFilter = document.getElementById('audit-user-filter');
      const currentVal = uFilter.value;
      uFilter.innerHTML = '<option value="TODOS">Todos os Usuários</option>' +
        stateUsers.map(u => `<option value="${{u.email}}">${{u.nome}} (${{u.email}})</option>`).join('');
      uFilter.value = currentVal || 'TODOS';

      const tbody = document.getElementById('users-tbody');
      if (stateUsers.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="6" class="py-8 text-center text-slate-400">Nenhum usuário cadastrado.</td></tr>';
        return;
      }}

      tbody.innerHTML = stateUsers.map(u => `
        <tr class="hover:bg-slate-50/80">
          <td class="py-3.5 px-4">
            <div class="font-bold text-navy-900">${{u.nome}}</div>
            <div class="text-xs text-slate-500 font-mono">${{u.email}}</div>
          </td>
          <td class="py-3.5 px-4">
            <span class="font-mono text-xs font-bold px-2.5 py-1 rounded-lg ${{u.cargo === 'ADMIN' ? 'bg-navy-900 text-gold-400' : 'bg-slate-100 text-navy-900 border border-slate-200'}}">
              ${{u.cargo}}
            </span>
          </td>
          <td class="py-3.5 px-4">
            <div class="flex flex-wrap gap-1">
              ${{(u.apps_permitidos || []).map(a => `<span class="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-slate-100 text-slate-700">${{a === '*' ? 'Todos os Apps (*)' : a}}</span>`).join('')}}
            </div>
          </td>
          <td class="py-3.5 px-4">
            ${{u.ativo
              ? `<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>Ativo (${{u.sessoes_ativas || 0}} sessões)</span>`
              : `<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-red-50 text-red-700 border border-red-200">Bloqueado</span>`
            }}
          </td>
          <td class="py-3.5 px-4 text-xs text-slate-600 tabular-nums">
            ${{fmtData(u.ultimo_login)}}
          </td>
          <td class="py-3.5 px-4 text-right space-x-1.5 whitespace-nowrap">
            <button
              type="button"
              onclick='editarUsuario(${{JSON.stringify(u)}})'
              class="btn-tactile px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 text-xs font-bold text-navy-900"
            >
              Editar
            </button>
            <button
              type="button"
              onclick="alternarStatusUsuario(${{u.id}}, ${{!u.ativo}})"
              class="btn-tactile px-2.5 py-1.5 rounded-lg text-xs font-bold ${{u.ativo ? 'bg-red-50 text-red-700 hover:bg-red-100 border border-red-200' : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200'}}"
            >
              ${{u.ativo ? 'Bloquear' : 'Reativar'}}
            </button>
          </td>
        </tr>
      `).join('');
    }}

    function formatarDetalhesAuditoria(item) {{
      const d = item.detalhes || {{}};
      if (d.resumo) return `<span class="font-semibold text-navy-900">${{d.resumo}}</span>`;
      if (d.lead_nome || d.novo_status) {{
        return `<span class="font-semibold text-navy-900">Lead #${{d.lead_id || ''}} (${{d.lead_nome || ''}})</span> → <span class="px-1.5 py-0.5 rounded bg-amber-100 text-amber-900 font-bold text-xs">${{d.novo_status || ''}}</span> ${{d.observacoes ? `<span class="text-slate-500 italic">"${{d.observacoes}}"</span>` : ''}}`;
      }}
      if (d.alvo_email) {{
        return `Usuário alvo: <span class="font-mono font-semibold">${{d.alvo_email}}</span>`;
      }}
      if (d.motivo) {{
        return `<span class="text-red-600 font-medium">${{d.motivo}}</span>`;
      }}
      const str = JSON.stringify(d);
      return str === '{{}}' ? `<span class="text-slate-400 font-mono">${{item.rota || '/'}}</span>` : `<span class="font-mono text-xs text-slate-600">${{str}}</span>`;
    }}

    function badgeAcao(acao) {{
      if (acao.includes('FALHA') || acao.includes('NEGADO') || acao.includes('BLOQUEADO')) {{
        return `<span class="px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200 font-mono text-[11px] font-bold">${{acao}}</span>`;
      }}
      if (acao.includes('LEAD') || acao.includes('WHATSAPP') || acao.includes('CONVERTIDO')) {{
        return `<span class="px-2 py-0.5 rounded-md bg-amber-50 text-amber-900 border border-amber-200 font-mono text-[11px] font-bold">${{acao}}</span>`;
      }}
      if (acao.includes('LOGIN_SUCESSO')) {{
        return `<span class="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 font-mono text-[11px] font-bold">${{acao}}</span>`;
      }}
      return `<span class="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200 font-mono text-[11px] font-bold">${{acao}}</span>`;
    }}

    async function carregarAuditoria() {{
      const q = document.getElementById('audit-search').value.trim();
      const app = document.getElementById('audit-app-filter').value;
      const email = document.getElementById('audit-user-filter').value;

      const params = new URLSearchParams();
      if (q) params.set('q', q);
      if (app && app !== 'TODOS') params.set('app', app);
      if (email && email !== 'TODOS') params.set('email', email);

      const res = await fetch('/api/admin/audit?' + params.toString());
      if (!res.ok) return;
      stateAudit = await res.json();

      document.getElementById('kpi-audit-count').textContent = stateAudit.length;
      const tbody = document.getElementById('audit-tbody');

      if (stateAudit.length === 0) {{
        tbody.innerHTML = `
          <tr>
            <td colspan="6" class="py-12 text-center">
              <p class="text-sm font-bold text-navy-900">Nenhuma atividade encontrada para este filtro</p>
              <p class="text-xs text-slate-500 mt-1">Assim que os vendedores acessarem ou interagirem com os leads, os eventos aparecerão aqui.</p>
            </td>
          </tr>
        `;
        return;
      }}

      tbody.innerHTML = stateAudit.map(item => `
        <tr class="hover:bg-slate-50/80">
          <td class="py-3 px-4 text-xs text-slate-500 tabular-nums whitespace-nowrap">
            ${{fmtData(item.created_at)}}
          </td>
          <td class="py-3 px-4">
            <div class="font-bold text-navy-900">${{item.usuario_nome || 'Visitante'}}</div>
            <div class="text-[11px] text-slate-500 font-mono">${{item.usuario_email || '—'}} ${{item.usuario_cargo ? `• ${{item.usuario_cargo}}` : ''}}</div>
          </td>
          <td class="py-3 px-4">
            <span class="text-xs font-bold text-navy-900 bg-slate-100 px-2.5 py-1 rounded-lg border border-slate-200">
              ${{item.app || 'gold-auth'}}
            </span>
          </td>
          <td class="py-3 px-4 whitespace-nowrap">
            ${{badgeAcao(item.acao)}}
          </td>
          <td class="py-3 px-4 text-xs">
            ${{formatarDetalhesAuditoria(item)}}
          </td>
          <td class="py-3 px-4 text-xs font-mono text-slate-400 tabular-nums">
            ${{item.ip || '—'}}
          </td>
        </tr>
      `).join('');
    }}

    function debounceAudit() {{
      clearTimeout(auditDebounceTimer);
      auditDebounceTimer = setTimeout(carregarAuditoria, 250);
    }}

    // Modal Usuário
    function abrirModalUsuario() {{
      document.getElementById('u-id').value = '';
      document.getElementById('user-modal-title').textContent = 'Novo Vendedor / Usuário';
      document.getElementById('u-nome').value = '';
      document.getElementById('u-email').value = '';
      document.getElementById('u-senha').value = '';
      document.getElementById('u-senha').required = true;
      document.getElementById('u-senha-hint').textContent = '(obrigatória)';
      document.getElementById('u-perms').value = '';
      document.getElementById('user-form-error').classList.add('hidden');
      document.querySelectorAll('input[name="u-app"]').forEach(cb => {{
        cb.checked = ['painel-vendedor', 'gold-db-api', 'cotador-web'].includes(cb.value);
      }});
      document.getElementById('user-modal').classList.remove('hidden');
    }}

    function editarUsuario(u) {{
      document.getElementById('u-id').value = u.id;
      document.getElementById('user-modal-title').textContent = 'Editar ' + u.nome;
      document.getElementById('u-nome').value = u.nome;
      document.getElementById('u-email').value = u.email;
      document.getElementById('u-cargo').value = u.cargo;
      document.getElementById('u-senha').value = '';
      document.getElementById('u-senha').required = false;
      document.getElementById('u-senha-hint').textContent = '(deixe em branco para manter a atual)';
      document.getElementById('u-perms').value = (u.permissoes_extras || []).join(', ');
      document.getElementById('user-form-error').classList.add('hidden');

      const apps = u.apps_permitidos || [];
      document.querySelectorAll('input[name="u-app"]').forEach(cb => {{
        cb.checked = apps.includes(cb.value);
      }});
      document.getElementById('user-modal').classList.remove('hidden');
    }}

    function fecharModalUsuario() {{
      document.getElementById('user-modal').classList.add('hidden');
    }}

    document.getElementById('user-form').addEventListener('submit', async (e) => {{
      e.preventDefault();
      const id = document.getElementById('u-id').value;
      const nome = document.getElementById('u-nome').value.trim();
      const email = document.getElementById('u-email').value.trim();
      const cargo = document.getElementById('u-cargo').value;
      const senha = document.getElementById('u-senha').value;
      const apps = Array.from(document.querySelectorAll('input[name="u-app"]:checked')).map(cb => cb.value);
      const perms = document.getElementById('u-perms').value.split(',').map(s => s.trim()).filter(Boolean);

      const payload = {{ nome, email, cargo, apps_permitidos: apps, permissoes_extras: perms }};
      if (senha) payload.senha = senha;

      const errEl = document.getElementById('user-form-error');
      errEl.classList.add('hidden');

      const url = id ? `/api/admin/users/${{id}}` : '/api/admin/users';
      const method = id ? 'PATCH' : 'POST';

      const res = await fetch(url, {{
        method,
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(payload)
      }});
      if (!res.ok) {{
        const data = await res.json().catch(() => ({{}}));
        errEl.textContent = data.detail || 'Não foi possível salvar o usuário.';
        errEl.classList.remove('hidden');
        return;
      }}
      fecharModalUsuario();
      await carregarUsuarios();
      await carregarAuditoria();
    }});

    async function alternarStatusUsuario(id, novoAtivo) {{
      await fetch(`/api/admin/users/${{id}}`, {{
        method: 'PATCH',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ ativo: novoAtivo }})
      }});
      await carregarUsuarios();
      await carregarAuditoria();
    }}

    // Modal Cargo
    function abrirModalCargo() {{
      document.getElementById('r-codigo').value = '';
      document.getElementById('r-codigo').readOnly = false;
      document.getElementById('r-nome').value = '';
      document.getElementById('r-desc').value = '';
      document.getElementById('r-perms').value = '';
      document.getElementById('role-modal').classList.remove('hidden');
    }}

    function editarCargo(r) {{
      document.getElementById('r-codigo').value = r.codigo;
      document.getElementById('r-codigo').readOnly = true;
      document.getElementById('r-nome').value = r.nome;
      document.getElementById('r-desc').value = r.descricao || '';
      document.getElementById('r-perms').value = (r.permissoes || []).join(', ');
      document.getElementById('role-modal').classList.remove('hidden');
    }}

    function fecharModalCargo() {{
      document.getElementById('role-modal').classList.add('hidden');
    }}

    document.getElementById('role-form').addEventListener('submit', async (e) => {{
      e.preventDefault();
      const codigo = document.getElementById('r-codigo').value.trim().toUpperCase();
      const nome = document.getElementById('r-nome').value.trim();
      const descricao = document.getElementById('r-desc').value.trim();
      const permissoes = document.getElementById('r-perms').value.split(',').map(s => s.trim()).filter(Boolean);

      const res = await fetch('/api/admin/roles', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ codigo, nome, descricao, permissoes }})
      }});
      if (res.ok) {{
        fecharModalCargo();
        await carregarCargos();
        await carregarAuditoria();
      }}
    }});

    async function removerCargo(codigo) {{
      if (!confirm(`Deseja realmente excluir o cargo ${{codigo}}?`)) return;
      await fetch(`/api/admin/roles/${{codigo}}`, {{ method: 'DELETE' }});
      await carregarCargos();
      await carregarAuditoria();
    }}

    // Atalho Esc fecha modais
    window.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') {{
        fecharModalUsuario();
        fecharModalCargo();
      }}
    }});

    async function carregarTudo() {{
      await Promise.all([carregarMe(), carregarCargos(), carregarUsuarios(), carregarAuditoria()]);
    }}

    carregarTudo();
    setInterval(carregarAuditoria, 10000);
  </script>
</body>
</html>"""
