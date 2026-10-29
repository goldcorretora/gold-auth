# -*- coding: utf-8 -*-
"""
Templates HTML da Gold Corretora (SSO Login Split-Screen + Central de Identidade & Auditoria).
Refinados sob os 5 Quality Gates do Web-Craft:
1. Logotipo Oficial Completo (sem qualquer corte na subtítulo 'corretora de seguros' e ornamentos laterais).
2. Arquitetura Split-Screen Institucional (Painel Institucional Azul-Marinho à esquerda + Superfície Clara/Arejada com Card Branco de Alto Contraste à direita, eliminando o 'Void Screen' e a estética de terminal).
3. Fluxo completo de UX: 'Lembrar meu usuário / Permanecer conectado' (persistência em localStorage + sessão de 30 dias), modal funcional 'Esqueceu sua senha?' com registro de chamado + atalho direto ao Suporte TI, e rodapé de suporte visível.
4. Contraste WCAG AA (>7:1 nos textos primários e >4.8:1 nos textos secundários e rodapé), anéis de foco nítidos com reforço visual, botão do ícone de senha com alto contraste e área de toque de 40x40px.
5. Microcópia humana, acolhedora e institucional (zero jargão técnico de DNS/wildcard).
"""

def _build_gold_logo_svg(text_fill: str = "#FFFFFF", gold_fill: str = "#F5B82E", css_class: str = "h-11 w-auto") -> str:
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 208.04 84.13" class="{css_class}" role="img" aria-label="Gold Corretora de Seguros">
  <g>
    <path fill="{text_fill}" d="M15.64,66.25l.3,4.5h-.3c-.4-1.35-.98-2.32-1.72-2.91-.75-.59-1.64-.89-2.69-.89-.87,0-1.67.22-2.37.67-.71.45-1.26,1.16-1.67,2.14-.4.98-.61,2.19-.61,3.65,0,1.2.19,2.24.57,3.12.38.88.96,1.55,1.73,2.02.77.47,1.65.7,2.63.7.86,0,1.61-.18,2.27-.55.66-.37,1.38-1.1,2.16-2.19l.3.2c-.66,1.18-1.44,2.04-2.32,2.58-.88.54-1.93.82-3.15.82-2.19,0-3.89-.81-5.09-2.44-.9-1.21-1.35-2.64-1.35-4.28,0-1.32.3-2.54.89-3.65.59-1.11,1.4-1.97,2.44-2.58,1.04-.61,2.17-.91,3.39-.91.95,0,1.89.23,2.82.7.27.14.47.22.58.22.17,0,.33-.06.46-.19.17-.18.29-.42.36-.73h.36,0ZM23.47,70.59c1.36,0,2.44.51,3.26,1.54.7.88,1.05,1.89,1.05,3.03,0,.8-.19,1.61-.58,2.43-.38.82-.91,1.44-1.59,1.86-.68.42-1.43.62-2.25.62-1.35,0-2.42-.54-3.22-1.61-.67-.91-1.01-1.92-1.01-3.05,0-.82.2-1.64.61-2.45.41-.81.94-1.41,1.61-1.8.66-.39,1.37-.58,2.11-.58h0ZM23.17,71.23c-.34,0-.69.1-1.04.31-.35.21-.63.56-.84,1.08-.22.51-.32,1.17-.32,1.98,0,1.3.26,2.42.78,3.36.52.94,1.2,1.41,2.05,1.41.63,0,1.15-.26,1.56-.78.41-.52.62-1.41.62-2.68,0-1.59-.34-2.83-1.03-3.74-.46-.62-1.05-.94-1.77-.94h0ZM33.2,70.59v2.02c.74-1.35,1.51-2.02,2.29-2.02.35,0,.65.11.88.33.23.22.35.47.35.76,0,.26-.08.47-.25.65-.17.18-.37.26-.6.26s-.48-.11-.76-.34c-.28-.23-.49-.34-.63-.34-.12,0-.24.07-.38.2-.29.27-.59.71-.9,1.32v4.28c0,.5.06.88.19,1.13.08.18.23.32.45.44.22.12.52.17.93.17v.36h-4.58v-.36c.45,0,.79-.07,1.01-.21.16-.11.28-.27.34-.5.03-.11.05-.43.05-.95v-3.46c0-1.04-.02-1.66-.06-1.86-.04-.2-.12-.34-.23-.43-.11-.09-.26-.14-.42-.14-.2,0-.43.05-.68.15l-.1-.36,2.71-1.1h.41ZM41.36,70.59v2.02c.74-1.35,1.51-2.02,2.29-2.02.35,0,.65.11.88.33.23.22.35.47.35.76,0,.26-.08.47-.25.65-.17.18-.37.26-.6.26s-.48-.11-.76-.34c-.28-.23-.49-.34-.63-.34-.12,0-.24.07-.38.2-.29.27-.59.71-.9,1.32v4.28c0,.5.06.88.19,1.13.08.18.23.32.45.44.22.12.52.17.93.17v.36h-4.58v-.36c.45,0,.79-.07,1.01-.21.16-.11.28-.27.34-.5.03-.11.05-.43.05-.95v-3.46c0-1.04-.02-1.66-.06-1.86-.04-.2-.12-.34-.23-.43-.11-.09-.26-.14-.42-.14-.2,0-.43.05-.68.15l-.1-.36,2.71-1.1h.41ZM48.38,74.23c0,1.32.32,2.36.97,3.11.65.75,1.42,1.13,2.3,1.13.58,0,1.09-.16,1.53-.48.43-.32.8-.87,1.09-1.66l.3.2c-.14.9-.53,1.72-1.19,2.45-.66.73-1.48,1.1-2.47,1.1-1.07,0-1.99-.42-2.76-1.25-.76-.84-1.15-1.96-1.15-3.37,0-1.53.39-2.72,1.18-3.57.78-.86,1.77-1.28,2.95-1.28,1,0,1.82.33,2.47.99.64.66.97,1.54.97,2.65h-6.18ZM48.38,73.67h4.14c-.03-.57-.1-.98-.2-1.21-.16-.36-.41-.65-.73-.86-.32-.21-.66-.31-1.01-.31-.54,0-1.02.21-1.45.63-.43.42-.67,1-.75,1.75h0ZM59.88,67.91v2.94h2.09v.66l-2.09.02v5.8c0,.58.08.97.25,1.17.16.2.38.3.64.3.22,0,.42-.07.63-.2.2-.13.36-.33.47-.6h.38c-.23.64-.55,1.13-.97,1.45-.42.32-.85.49-1.29.49-.3,0-.59-.08-.88-.25-.29-.17-.5-.41-.63-.72-.14-.31-.21-.79-.21-1.43v-6.04h-1.42v-.31c.36-.14.73-.38,1.1-.72.38-.34.71-.74,1.01-1.21.15-.25.36-.7.63-1.36h.3ZM68.72,70.59c1.36,0,2.44.51,3.26,1.54.7.88,1.05,1.89,1.05,3.03,0,.8-.19,1.61-.58,2.43-.38.82-.91,1.44-1.59,1.86-.68.42-1.43.62-2.25.62-1.35,0-2.42-.54-3.22-1.61-.67-.91-1.01-1.92-1.01-3.05,0-.82.2-1.64.61-2.45.41-.81.94-1.41,1.61-1.8.66-.39,1.37-.58,2.11-.58h0ZM68.42,71.23c-.34,0-.69.1-1.04.31-.35.21-.63.56-.84,1.08-.22.51-.32,1.17-.32,1.98,0,1.3.26,2.42.78,3.36.52.94,1.2,1.41,2.05,1.41.63,0,1.15-.26,1.56-.78.41-.52.62-1.41.62-2.68,0-1.59-.34-2.83-1.03-3.74-.46-.62-1.05-.94-1.77-.94h0ZM78.45,70.59v2.02c.74-1.35,1.51-2.02,2.29-2.02.35,0,.65.11.88.33.23.22.35.47.35.76,0,.26-.08.47-.25.65-.17.18-.37.26-.6.26s-.48-.11-.76-.34c-.28-.23-.49-.34-.63-.34-.12,0-.24.07-.38.2-.29.27-.59.71-.9,1.32v4.28c0,.5.06.88.19,1.13.08.18.23.32.45.44.22.12.52.17.93.17v.36h-4.58v-.36c.45,0,.79-.07,1.01-.21.16-.11.28-.27.34-.5.03-.11.05-.43.05-.95v-3.46c0-1.04-.02-1.66-.06-1.86-.04-.2-.12-.34-.23-.43-.11-.09-.26-.14-.42-.14-.2,0-.43.05-.68.15l-.1-.36,2.71-1.1h.41ZM89.03,78.51c-.92.71-1.49,1.12-1.73,1.23-.35.16-.72.25-1.12.25-.62,0-1.13-.21-1.53-.64s-.6-.98-.6-1.67c0-.44.1-.82.29-1.13.27-.44.73-.86,1.39-1.25.66-.39,1.76-.87,3.3-1.43v-.35c0-.89-.14-1.5-.42-1.83-.28-.33-.69-.5-1.23-.5-.41,0-.73.11-.97.33-.25.22-.37.47-.37.76l.02.57c0,.3-.08.53-.23.7-.15.16-.36.24-.6.24s-.44-.08-.6-.25c-.15-.17-.23-.4-.23-.7,0-.56.29-1.08.86-1.55.57-.47,1.38-.7,2.42-.7.8,0,1.45.13,1.96.4.38.2.67.52.85.95.12.28.18.85.18,1.71v3.03c0,.85.02,1.37.05,1.56.03.19.09.32.16.39.08.06.16.1.26.1.11,0,.2-.02.28-.07.14-.09.4-.32.79-.71v.55c-.73.98-1.43,1.47-2.1,1.47-.32,0-.58-.11-.77-.33-.19-.22-.29-.6-.29-1.13h0ZM89.03,77.88v-3.4c-.99.39-1.63.67-1.92.83-.52.29-.89.58-1.11.9-.22.31-.33.65-.33,1.02,0,.47.14.86.42,1.17.28.31.61.46.97.46.5,0,1.15-.33,1.96-.98h0ZM107.17,78.78c-.44.46-.86.79-1.28.99-.42.2-.87.3-1.35.3-.98,0-1.83-.41-2.56-1.22-.73-.82-1.09-1.87-1.09-3.15s.4-2.45,1.21-3.52c.81-1.06,1.85-1.59,3.12-1.59.79,0,1.44.25,1.95.76v-1.66c0-1.02-.02-1.64-.07-1.87-.05-.23-.13-.39-.23-.48-.11-.08-.24-.13-.39-.13-.17,0-.39.05-.68.16l-.13-.36,2.68-1.1h.44v10.34c0,1.04.02,1.68.07,1.91.05.23.13.39.24.48.11.09.23.14.38.14.18,0,.41-.06.71-.17l.11.36-2.67,1.1h-.45v-1.29h0ZM107.17,78.1v-4.58c-.04-.45-.16-.85-.35-1.22-.19-.37-.45-.64-.78-.83-.32-.18-.64-.28-.94-.28-.57,0-1.09.26-1.54.77-.59.68-.89,1.66-.89,2.96s.29,2.32.86,3.02c.57.7,1.21,1.05,1.92,1.05.6,0,1.17-.3,1.72-.9h0ZM113.85,74.23c0,1.32.32,2.36.97,3.11.65.75,1.42,1.13,2.3,1.13.58,0,1.09-.16,1.53-.48.43-.32.8-.87,1.09-1.66l.3.2c-.14.9-.53,1.72-1.19,2.45-.66.73-1.48,1.1-2.47,1.1-1.07,0-1.99-.42-2.76-1.25-.76-.84-1.15-1.96-1.15-3.37,0-1.53.39-2.72,1.18-3.57.78-.86,1.77-1.28,2.95-1.28,1,0,1.82.33,2.47.99.64.66.97,1.54.97,2.65h-6.18,0ZM113.85,73.67h4.14c-.03-.57-.1-.98-.2-1.21-.16-.36-.41-.65-.73-.86-.32-.21-.66-.31-1.01-.31-.54,0-1.02.21-1.45.63-.43.42-.67,1-.75,1.75h0ZM137.79,66.25v4.58h-.36c-.12-.88-.33-1.58-.63-2.1-.3-.52-.74-.93-1.3-1.24-.56-.31-1.14-.46-1.74-.46-.68,0-1.24.21-1.68.62-.44.41-.67.89-.67,1.41,0,.4.14.77.42,1.11.41.49,1.37,1.14,2.89,1.95,1.24.67,2.09,1.18,2.54,1.53.45.36.8.77,1.05,1.26.24.48.37.99.37,1.52,0,1-.39,1.87-1.17,2.59-.78.73-1.78,1.09-3.01,1.09-.39,0-.75-.03-1.09-.09-.2-.03-.62-.15-1.26-.36-.63-.21-1.04-.31-1.21-.31s-.29.05-.39.15c-.09.1-.16.3-.21.61h-.36v-4.54h.36c.17.95.4,1.66.68,2.13.29.47.73.87,1.32,1.18.59.31,1.24.47,1.94.47.81,0,1.46-.22,1.93-.65.47-.43.71-.94.71-1.53,0-.33-.09-.66-.27-.99-.18-.33-.46-.64-.83-.93-.25-.2-.95-.61-2.09-1.24-1.14-.63-1.95-1.14-2.43-1.51-.48-.38-.85-.8-1.09-1.25-.25-.46-.37-.96-.37-1.51,0-.95.37-1.77,1.1-2.46.73-.69,1.66-1.03,2.79-1.03.71,0,1.45.17,2.24.52.37.16.62.24.77.24.17,0,.31-.05.42-.15.11-.1.19-.3.26-.61h.36ZM143.35,74.23c0,1.32.32,2.36.97,3.11.65.75,1.42,1.13,2.3,1.13.58,0,1.09-.16,1.53-.48.43-.32.8-.87,1.09-1.66l.3.2c-.14.9-.53,1.72-1.19,2.45-.66.73-1.48,1.1-2.47,1.1-1.07,0-1.99-.42-2.76-1.25-.76-.84-1.15-1.96-1.15-3.37,0-1.53.39-2.72,1.18-3.57.78-.86,1.77-1.28,2.95-1.28,1,0,1.82.33,2.47.99.64.66.97,1.54.97,2.65h-6.18,0ZM143.35,73.67h4.14c-.03-.57-.1-.98-.2-1.21-.16-.36-.41-.65-.73-.86-.32-.21-.66-.31-1.01-.31-.54,0-1.02.21-1.45.63-.43.42-.67,1-.75,1.75h0ZM154.62,76.53c-.54-.27-.96-.64-1.26-1.12-.29-.48-.44-1-.44-1.58,0-.88.33-1.64,1-2.28.66-.64,1.52-.96,2.56-.96.85,0,1.59.21,2.21.62h1.89c.28,0,.44,0,.49.02.05.02.08.04.1.08.04.06.06.16.06.31,0,.17-.02.29-.05.35-.02.03-.05.06-.1.08-.05.02-.21.03-.49.03h-1.16c.36.47.55,1.07.55,1.8,0,.83-.32,1.54-.95,2.14-.64.59-1.49.89-2.56.89-.44,0-.89-.07-1.35-.2-.28.25-.48.47-.58.65-.1.19-.15.34-.15.47,0,.11.05.22.16.32.11.11.32.18.63.23.18.03.64.05,1.37.07,1.34.03,2.21.08,2.61.15.61.08,1.09.31,1.45.67.36.37.54.81.54,1.35,0,.73-.34,1.43-1.03,2.07-1.02.95-2.34,1.43-3.97,1.43-1.26,0-2.32-.28-3.18-.85-.49-.33-.73-.67-.73-1.02,0-.16.04-.31.11-.47.11-.24.34-.58.68-1.01.05-.06.38-.41,1-1.06-.34-.2-.58-.38-.72-.54s-.21-.34-.21-.55c0-.23.09-.5.28-.81.18-.31.61-.74,1.28-1.31h0ZM156.32,71.07c-.48,0-.88.19-1.21.57-.32.38-.49.97-.49,1.76,0,1.03.22,1.82.66,2.38.34.43.76.64,1.28.64s.9-.18,1.22-.55.48-.95.48-1.74c0-1.03-.22-1.84-.67-2.42-.33-.43-.76-.64-1.28-.64h0ZM154.53,79.81c-.31.33-.54.64-.69.93-.16.29-.23.55-.23.79,0,.31.19.58.57.82.65.4,1.59.6,2.81.6s2.03-.21,2.59-.62c.56-.41.83-.85.83-1.32,0-.34-.17-.58-.5-.72-.34-.14-1.01-.23-2.01-.25-1.46-.04-2.59-.11-3.37-.22h0ZM171.59,70.85v5.44c0,1.02.02,1.64.07,1.87.05.23.13.39.23.48.11.09.23.14.38.14.2,0,.43-.06.68-.17l.14.36-2.68,1.1h-.44v-1.88c-.77.83-1.35,1.34-1.76,1.56-.4.21-.83.32-1.28.32-.5,0-.93-.14-1.3-.43-.37-.29-.62-.66-.77-1.12-.14-.46-.21-1.1-.21-1.93v-3.99c0-.42-.05-.72-.14-.88-.09-.16-.23-.29-.41-.38-.18-.09-.51-.13-.98-.12v-.36h3.14v6c0,.84.14,1.38.43,1.64.29.26.64.39,1.05.39.28,0,.6-.09.95-.26.35-.18.78-.51,1.26-1.01v-5.07c0-.52-.09-.87-.28-1.05-.19-.18-.57-.28-1.16-.29v-.36h3.06ZM177.87,70.59v2.02c.74-1.35,1.51-2.02,2.29-2.02.35,0,.65.11.88.33.23.22.35.47.35.76,0,.26-.08.47-.25.65-.17.18-.37.26-.6.26s-.48-.11-.76-.34c-.28-.23-.49-.34-.63-.34-.12,0-.24.07-.38.2-.29.27-.59.71-.9,1.32v4.28c0,.5.06.88.19,1.13.08.18.23.32.45.44.22.12.52.17.93.17v.36h-4.58v-.36c.45,0,.79-.07,1.01-.21.16-.11.28-.27.34-.5.03-.11.05-.43.05-.95v-3.46c0-1.04-.02-1.66-.06-1.86-.04-.2-.12-.34-.23-.43-.11-.09-.26-.14-.42-.14-.2,0-.43.05-.68.15l-.1-.36,2.71-1.1h.41ZM187.8,70.59c1.36,0,2.44.51,3.26,1.54.7.88,1.05,1.89,1.05,3.03,0,.8-.19,1.61-.58,2.43-.38.82-.91,1.44-1.59,1.86-.68.42-1.43.62-2.25.62-1.35,0-2.42-.54-3.22-1.61-.67-.91-1.01-1.92-1.01-3.05,0-.82.2-1.64.61-2.45.41-.81.94-1.41,1.61-1.8.66-.39,1.37-.58,2.11-.58h0ZM187.49,71.23c-.34,0-.69.1-1.04.31-.35.21-.63.56-.84,1.08-.22.51-.32,1.17-.32,1.98,0,1.3.26,2.42.78,3.36.52.94,1.2,1.41,2.05,1.41.63,0,1.15-.26,1.56-.78.41-.52.62-1.41.62-2.68,0-1.59-.34-2.83-1.03-3.74-.46-.62-1.05-.94-1.77-.94h0ZM200.67,70.59v3.04h-.32c-.25-.95-.56-1.6-.95-1.94-.38-.34-.88-.52-1.47-.52-.45,0-.82.12-1.1.36-.28.24-.42.51-.42.8,0,.36.1.68.31.94.2.27.61.55,1.23.85l1.43.69c1.32.65,1.98,1.5,1.98,2.55,0,.81-.31,1.47-.92,1.97-.61.5-1.3.75-2.06.75-.55,0-1.17-.1-1.87-.29-.22-.06-.39-.09-.53-.09-.15,0-.27.08-.35.24h-.32v-3.2h.32c.18.91.53,1.6,1.05,2.07.51.46,1.09.69,1.73.69.45,0,.81-.13,1.1-.39.28-.26.43-.58.43-.95,0-.45-.16-.82-.48-1.13s-.95-.69-1.89-1.16c-.94-.47-1.56-.89-1.85-1.27-.29-.37-.44-.84-.44-1.41,0-.74.25-1.35.76-1.85.5-.5,1.15-.74,1.95-.74.35,0,.78.08,1.28.23.33.1.55.15.66.15s.19-.02.25-.07c.06-.05.13-.15.2-.31h.32,0ZM47.74,0l1.22,15.05h-1.3c-1.24-3.73-2.84-6.54-4.8-8.44-2.83-2.72-6.47-4.09-10.91-4.09-6.05,0-10.66,2.4-13.81,7.21-2.64,4.04-3.96,8.88-3.96,14.48,0,4.55.88,8.69,2.64,12.44,1.75,3.74,4.06,6.49,6.9,8.24,2.84,1.74,5.77,2.62,8.77,2.62,1.75,0,3.46-.23,5.1-.67,1.63-.44,3.22-1.1,4.74-1.98v-13.84c0-2.4-.18-3.97-.54-4.7-.37-.74-.94-1.31-1.69-1.69-.77-.4-2.11-.59-4.03-.59v-1.3h18.43v1.3h-.88c-1.82,0-3.07.61-3.76,1.84-.47.86-.7,2.58-.7,5.15v14.63c-2.69,1.46-5.35,2.53-7.97,3.22-2.63.68-5.54,1.02-8.75,1.02-9.2,0-16.19-2.95-20.96-8.87-3.59-4.43-5.38-9.55-5.38-15.34,0-4.2,1.01-8.23,3.02-12.07,2.39-4.57,5.66-8.1,9.83-10.56C22.46,1.02,26.58,0,31.34,0,33.07,0,34.64.14,36.06.42c1.42.29,3.42.9,6.02,1.86,1.31.49,2.2.74,2.64.74s.82-.2,1.14-.61c.31-.41.5-1.21.58-2.41h1.3,0ZM148.92,35.64l1.15.25-4.1,12.92h-36.94v-1.3h1.79c2.02,0,3.46-.65,4.32-1.96.49-.74.73-2.47.73-5.17V9.5c0-2.98-.32-4.84-.98-5.58-.91-1.03-2.27-1.55-4.07-1.55h-1.79v-1.3h21.6v1.3c-2.53-.02-4.31.2-5.34.7-1.02.48-1.72,1.1-2.09,1.84-.37.74-.56,2.52-.56,5.32v30.1c0,1.96.19,3.29.56,4.02.28.5.72.86,1.31,1.1.58.23,2.41.35,5.5.35h3.48c3.67,0,6.24-.26,7.72-.8s2.83-1.5,4.06-2.87c1.21-1.37,2.44-3.53,3.66-6.48h0ZM152.8,48.82v-1.3h1.79c2.02,0,3.44-.65,4.28-1.93.52-.77.77-2.51.77-5.2V9.5c0-2.98-.32-4.84-.98-5.58-.91-1.03-2.27-1.55-4.07-1.55h-1.79v-1.3h19.4c7.13,0,12.55.8,16.26,2.42,3.72,1.62,6.71,4.32,8.96,8.1,2.27,3.78,3.4,8.15,3.4,13.09,0,6.65-2.02,12.19-6.05,16.66-4.52,4.98-11.41,7.46-20.68,7.46h-21.3ZM166.4,45.31c2.98.66,5.46.98,7.48.98,5.42,0,9.92-1.91,13.51-5.74,3.58-3.82,5.36-9,5.36-15.54s-1.79-11.78-5.36-15.58c-3.59-3.8-8.18-5.7-13.8-5.7-2.1,0-4.5.34-7.19,1.02v40.55h0Z"></path>
    <path fill="{gold_fill}" d="M81.9,0c6.18,0,11.54,2.35,16.07,7.06,4.54,4.7,6.8,10.57,6.8,17.62s-2.28,13.26-6.85,18.05c-4.56,4.79-10.09,7.18-16.58,7.18s-12.06-2.34-16.52-7.01c-4.46-4.67-6.7-10.7-6.7-18.12s2.58-13.75,7.73-18.54c4.48-4.15,9.83-6.23,16.06-6.23h0ZM81.23,2.52c-4.25,0-7.67,1.58-10.24,4.75-3.2,3.95-4.81,9.72-4.81,17.33s1.66,13.79,4.98,17.99c2.56,3.19,5.92,4.79,10.1,4.79,4.48,0,8.16-1.75,11.08-5.24,2.92-3.5,4.37-9.01,4.37-16.55,0-8.17-1.61-14.27-4.81-18.28-2.57-3.19-6.12-4.79-10.67-4.79h0Z"></path>
  </g>
  <rect fill="{text_fill}" x="15.84" y="56.17" width="175.56" height="1.92"></rect>
  <circle fill="{text_fill}" cx="193.08" cy="57.02" r="1.8"></circle>
  <circle fill="{text_fill}" cx="4.92" cy="57.01" r="2.28"></circle>
  <circle fill="{text_fill}" cx="9.96" cy="57.01" r="3"></circle>
  <circle fill="{text_fill}" cx="1.48" cy="57.09" r="1.48"></circle>
  <circle fill="{text_fill}" cx="14.28" cy="57.25" r="1.8"></circle>
  <circle fill="{text_fill}" cx="197.82" cy="56.92" r="3"></circle>
  <circle fill="{text_fill}" cx="203" cy="57.02" r="2.28"></circle>
  <circle fill="{text_fill}" cx="206.55" cy="56.83" r="1.48"></circle>
</svg>
"""

GOLD_LOGO_LIGHT = _build_gold_logo_svg(text_fill="#FFFFFF", gold_fill="#F5B82E", css_class="h-10 sm:h-12 w-auto")
GOLD_LOGO_NAVY = _build_gold_logo_svg(text_fill="#0F1A2A", gold_fill="#C59B27", css_class="h-11 w-auto")
GOLD_LOGO_HEADER = _build_gold_logo_svg(text_fill="#FFFFFF", gold_fill="#F5B82E", css_class="h-9 w-auto")

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
            50: '#FBF7EB',
            100: '#F5EBD0',
            300: '#EAD084',
            400: '#DDBB5C',
            500: '#C59B27',
            600: '#A67F18',
            700: '#876511',
          },
          navy: {
            700: '#1E2F47',
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
    transition: transform 150ms var(--ease-out-strong), box-shadow 150ms ease, background-color 150ms ease, border-color 150ms ease, opacity 150ms ease;
  }
  .btn-tactile:active:not(:disabled) {
    transform: scale(0.98);
  }
  .btn-gold-primary {
    background: linear-gradient(180deg, #162235 0%, #0F1A2A 100%);
    color: #FFFFFF;
    border: 1px solid #0A121E;
    box-shadow: 0 10px 24px -6px rgba(15, 26, 42, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.14);
  }
  .btn-gold-primary:hover:not(:disabled) {
    background: linear-gradient(180deg, #1E2F47 0%, #162235 100%);
    box-shadow: 0 14px 28px -6px rgba(15, 26, 42, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }
  .input-corporate {
    transition: border-color 150ms ease, box-shadow 150ms ease, background-color 150ms ease;
  }
  .input-corporate::placeholder {
    color: #94A3B8;
    font-weight: 400;
  }
  .input-corporate:focus {
    outline: none;
    background-color: #FFFFFF;
    border-color: #0F1A2A;
    box-shadow: 0 0 0 3px rgba(197, 155, 39, 0.28);
  }
  .field-group:focus-within label {
    color: #0F1A2A;
  }
  .field-group:focus-within .focus-badge {
    opacity: 1;
    transform: translateX(0);
  }
  .modal-panel {
    transition: transform 200ms var(--ease-out-strong), opacity 200ms var(--ease-out-strong);
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


def get_login_html(default_redirect: str = "https://vendas.goldcorretora.com.br") -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  {SHARED_HEAD}
  <title>Portal Interno • Gold Corretora de Seguros</title>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col lg:flex-row selection:bg-gold-500 selection:text-white">

  <!-- ===================================================================== -->
  <!-- COLUNA ESQUERDA: PAINEL INSTITUCIONAL GOLD CORRETORA (DESKTOP SPLIT)  -->
  <!-- ===================================================================== -->
  <aside class="hidden lg:flex lg:w-[46%] xl:w-[48%] bg-navy-900 text-white p-12 xl:p-16 flex-col justify-between relative overflow-hidden border-r border-navy-800">
    <!-- Iluminação ambiente sutil institucional -->
    <div class="pointer-events-none absolute -top-32 -left-32 w-[480px] h-[480px] rounded-full bg-gold-500/10 blur-3xl"></div>
    <div class="pointer-events-none absolute bottom-0 right-0 w-[420px] h-[420px] rounded-full bg-gold-400/5 blur-3xl"></div>

    <!-- Topo: Logo Oficial Completo + Selo Institucional -->
    <div class="relative z-10 flex items-center justify-between">
      <a href="https://goldcorretora.com.br" class="inline-block focus:outline-none focus-visible:ring-2 focus-visible:ring-gold-400 rounded-lg">
        {GOLD_LOGO_LIGHT}
      </a>
      <span class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/15 text-xs font-semibold text-gold-300">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        Ambiente Interno Protegido
      </span>
    </div>

    <!-- Centro: Mensagem Institucional Humanizada -->
    <div class="relative z-10 my-auto py-10 max-w-lg space-y-6">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-lg bg-gold-500/15 border border-gold-400/30 text-gold-300 text-xs font-bold tracking-wide">
        Tradição em Proteção Familiar e Patrimonial
      </div>

      <h2 class="text-3xl xl:text-4xl font-extrabold text-white tracking-tight leading-[1.18]">
        Cuidando do futuro de quem confia na Gold Corretora.
      </h2>

      <p class="text-base text-slate-200 leading-relaxed font-normal">
        Bem-vindo à nossa central integrada de atendimento, cotações e gestão de carteira. Um único acesso para você acompanhar seus clientes com agilidade e segurança.
      </p>

      <!-- Pilares Operacionais -->
      <div class="pt-4 grid grid-cols-2 gap-4 border-t border-white/10">
        <div class="bg-white/5 border border-white/10 rounded-2xl p-4">
          <div class="text-xs font-bold text-gold-300 mb-1">Central Comercial</div>
          <p class="text-xs text-slate-200 leading-relaxed">Atendimento imediato de simulações de Seguro de Vida e propostas.</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-2xl p-4">
          <div class="text-xs font-bold text-gold-300 mb-1">Gestão de Carteira</div>
          <p class="text-xs text-slate-200 leading-relaxed">Consulta unificada de apólices vigentes, segurados e assistência.</p>
        </div>
      </div>
    </div>

    <!-- Rodapé Institucional Esquerdo (Alto Contraste WCAG AA) -->
    <div class="relative z-10 pt-6 border-t border-white/15 flex items-center justify-between text-xs text-slate-200">
      <span class="font-medium">© Gold Corretora de Seguros</span>
      <span class="text-slate-300">Goiânia • GO</span>
    </div>
  </aside>

  <!-- ===================================================================== -->
  <!-- COLUNA DIREITA: ÁREA DE LOGIN CLARA, AREJADA E DE ALTO CONTRASTE      -->
  <!-- ===================================================================== -->
  <main class="flex-1 flex flex-col justify-between p-5 sm:p-8 lg:p-12 xl:p-16 bg-slate-50">
    <!-- Barra Superior Mobile / Atalho Institucional -->
    <div class="flex items-center justify-between max-w-md w-full mx-auto lg:max-w-none">
      <div class="lg:hidden">
        {GOLD_LOGO_NAVY}
      </div>
      <div class="hidden lg:block"></div>
      <a
        href="https://goldcorretora.com.br"
        target="_blank"
        rel="noopener noreferrer"
        class="text-xs font-bold text-slate-600 hover:text-navy-900 flex items-center gap-1.5 px-3 py-1.5 rounded-xl hover:bg-slate-200/60 transition focus:outline-none focus-visible:ring-2 focus-visible:ring-navy-900"
      >
        <span>Site institucional</span>
        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
      </a>
    </div>

    <!-- Container Central do Formulário -->
    <div class="w-full max-w-[440px] mx-auto my-8">
      <!-- Card Branco Elevado com Contraste Nítido sobre o Fundo Slate-50 -->
      <section class="bg-white rounded-3xl border border-slate-200/90 shadow-[0_20px_50px_-12px_rgba(15,26,42,0.10)] p-7 sm:p-9">
        <!-- Cabeçalho do Card -->
        <div class="mb-7">
          <div class="hidden lg:block mb-5">
            {GOLD_LOGO_NAVY}
          </div>
          <h1 class="text-2xl sm:text-[26px] font-extrabold text-navy-900 tracking-tight leading-snug">
            Acesse o portal interno
          </h1>
          <p class="text-sm text-slate-600 mt-1.5 font-medium">
            Informe seu e-mail e senha para entrar nos sistemas da Gold Corretora.
          </p>
        </div>

        <!-- Banner de Erro / Alerta -->
        <div
          id="error-banner"
          role="alert"
          class="hidden mb-5 rounded-2xl bg-red-50 border border-red-200 px-4 py-3.5 text-xs font-bold text-red-800 flex items-start gap-2.5"
        >
          <svg class="w-4 h-4 text-red-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
          <span id="error-text">Verifique seu e-mail e sua senha.</span>
        </div>

        <!-- Formulário de Login -->
        <form id="login-form" class="space-y-5" novalidate>
          <!-- Campo de E-mail -->
          <div class="field-group">
            <div class="flex items-center justify-between mb-2">
              <label for="email" class="block text-xs font-extrabold text-slate-700 transition-colors">
                Seu e-mail de acesso
              </label>
              <span class="focus-badge opacity-0 -translate-x-1 transition-all text-[11px] font-bold text-gold-700 bg-gold-50 px-2 py-0.5 rounded-md border border-gold-300">
                Editando
              </span>
            </div>
            <input
              id="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              placeholder="Ex.: voce@goldcorretora.com.br"
              class="input-corporate w-full h-12 rounded-xl bg-slate-50/70 border border-slate-300 px-4 text-sm font-semibold text-navy-900"
            />
          </div>

          <!-- Campo de Senha + Link Esqueceu sua senha? -->
          <div class="field-group">
            <div class="flex items-center justify-between mb-2">
              <label for="senha" class="block text-xs font-extrabold text-slate-700 transition-colors">
                Sua senha
              </label>
              <button
                type="button"
                onclick="abrirModalRecuperacao()"
                class="text-xs font-bold text-gold-700 hover:text-navy-900 underline decoration-gold-400 underline-offset-4 focus:outline-none focus-visible:ring-2 focus-visible:ring-navy-900 rounded px-1"
              >
                Esqueceu sua senha?
              </button>
            </div>
            <div class="relative">
              <input
                id="senha"
                name="senha"
                type="password"
                autocomplete="current-password"
                required
                placeholder="Digite sua senha"
                class="input-corporate w-full h-12 rounded-xl bg-slate-50/70 border border-slate-300 pl-4 pr-12 text-sm font-semibold text-navy-900"
              />
              <button
                type="button"
                id="toggle-pw"
                aria-label="Mostrar ou ocultar senha"
                title="Mostrar ou ocultar senha"
                class=" absolute right-1.5 top-1/2 -translate-y-1/2 w-9 h-9 rounded-lg text-slate-600 hover:text-navy-900 hover:bg-slate-200/70 flex items-center justify-center transition focus:outline-none focus-visible:ring-2 focus-visible:ring-navy-900"
              >
                <svg id="eye-open" class="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg id="eye-closed" class="hidden w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Opção Lembrar Meu Usuário / Permanecer Conectado -->
          <div class="flex items-center justify-between pt-0.5">
            <label for="lembrar" class="inline-flex items-center gap-2.5 cursor-pointer select-none">
              <input
                id="lembrar"
                name="lembrar"
                type="checkbox"
                checked
                class="w-4 h-4 rounded border-slate-300 text-navy-900 focus:ring-2 focus:ring-gold-500"
              />
              <span class="text-xs font-semibold text-slate-700">
                Lembrar meu e-mail e permanecer conectado
              </span>
            </label>
          </div>

          <!-- Botão Principal -->
          <div class="pt-1">
            <button
              type="submit"
              id="submit-btn"
              class="btn-tactile btn-gold-primary w-full h-12 rounded-xl font-extrabold text-sm flex items-center justify-center gap-2.5 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-navy-900 disabled:opacity-50"
            >
              <span id="submit-label">Entrar no Portal Gold</span>
              <svg id="submit-arrow" class="w-4 h-4 text-gold-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
              <svg id="submit-spinner" class="hidden w-4 h-4 animate-spin text-gold-400" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
            </button>
          </div>
        </form>

        <!-- Bloco de Suporte ao Colaborador / Corretor -->
        <div class="mt-7 pt-5 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs text-slate-600">
          <span class="font-medium">Precisa de ajuda com seu acesso?</span>
          <button
            type="button"
            onclick="abrirModalRecuperacao()"
            class="font-extrabold text-navy-900 hover:text-gold-700 inline-flex items-center gap-1 underline decoration-slate-300 underline-offset-4 focus:outline-none focus-visible:ring-2 focus-visible:ring-navy-900 rounded"
          >
            <span>Falar com o Suporte Gold</span>
          </button>
        </div>
      </section>
    </div>

    <!-- Rodapé Direito com Contraste WCAG AA Validado (>5.5:1) -->
    <footer class="max-w-md w-full mx-auto lg:max-w-none text-center lg:flex lg:items-center lg:justify-between text-xs text-slate-600 font-medium pt-4 border-t border-slate-200/80">
      <span>Gold Corretora de Seguros • Portal de Colaboradores e Consultores</span>
      <span class="block lg:inline mt-1 lg:mt-0 text-slate-600">Conexão segura verificada</span>
    </footer>
  </main>

  <!-- ===================================================================== -->
  <!-- MODAL: RECUPERAÇÃO DE SENHA & SUPORTE INTERNO                         -->
  <!-- ===================================================================== -->
  <div
    id="forgot-modal"
    class="hidden fixed inset-0 z-50 bg-navy-950/60 backdrop-blur-xs flex items-center justify-center p-4"
    role="dialog"
    aria-modal="true"
    aria-labelledby="forgot-title"
  >
    <div class="modal-panel bg-white rounded-3xl border border-slate-200 max-w-md w-full p-6 sm:p-7 shadow-2xl space-y-4">
      <div class="flex items-start justify-between gap-3">
        <div>
          <h2 id="forgot-title" class="text-lg font-extrabold text-navy-900">
            Recuperar ou liberar acesso
          </h2>
          <p class="text-xs text-slate-600 mt-1 leading-relaxed">
            Informe seu e-mail abaixo. A administração da Gold Corretora receberá seu pedido imediatamente para gerar uma nova senha.
          </p>
        </div>
        <button
          type="button"
          onclick="fecharModalRecuperacao()"
          aria-label="Fechar janela"
          class="w-8 h-8 rounded-lg text-slate-500 hover:text-navy-900 hover:bg-slate-100 flex items-center justify-center font-bold focus:outline-none focus-visible:ring-2 focus-visible:ring-navy-900"
        >
          ✕
        </button>
      </div>

      <form id="forgot-form" class="space-y-4">
        <div>
          <label for="forgot-email" class="block text-xs font-extrabold text-slate-700 mb-1.5">
            Seu e-mail de cadastro
          </label>
          <input
            id="forgot-email"
            type="email"
            required
            placeholder="Ex.: voce@goldcorretora.com.br"
            class="input-corporate w-full h-11 rounded-xl bg-slate-50 border border-slate-300 px-3.5 text-sm font-semibold text-navy-900"
          />
        </div>

        <div>
          <label for="forgot-obs" class="block text-xs font-extrabold text-slate-700 mb-1.5">
            Como podemos ajudar? <span class="font-normal text-slate-500">(opcional)</span>
          </label>
          <input
            id="forgot-obs"
            type="text"
            placeholder="Ex.: Esqueci minha senha / Preciso liberar acesso ao painel"
            class="input-corporate w-full h-11 rounded-xl bg-slate-50 border border-slate-300 px-3.5 text-xs font-medium text-navy-900"
          />
        </div>

        <div id="forgot-feedback" class="hidden rounded-xl p-3 text-xs font-bold"></div>

        <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-200">
          <button
            type="button"
            onclick="fecharModalRecuperacao()"
            class="btn-tactile px-4 py-2.5 rounded-xl text-xs font-bold text-slate-700 hover:bg-slate-100"
          >
            Fechar
          </button>
          <button
            type="submit"
            id="forgot-submit"
            class="btn-tactile btn-gold-primary px-5 py-2.5 rounded-xl text-xs font-extrabold"
          >
            Solicitar Nova Senha
          </button>
        </div>
      </form>

      <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
        <span>Urgência no plantão comercial?</span>
        <a
          href="mailto:gold.gabrielrodrigues@gmail.com?subject=Suporte%20Acesso%20Portal%20Gold"
          class="font-bold text-navy-900 hover:underline"
        >
          Enviar e-mail direto à TI
        </a>
      </div>
    </div>
  </div>

  <script>
    const form = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const senhaInput = document.getElementById('senha');
    const lembrarInput = document.getElementById('lembrar');
    const errorBanner = document.getElementById('error-banner');
    const errorText = document.getElementById('error-text');
    const submitBtn = document.getElementById('submit-btn');
    const submitLabel = document.getElementById('submit-label');
    const submitArrow = document.getElementById('submit-arrow');
    const submitSpinner = document.getElementById('submit-spinner');
    const togglePw = document.getElementById('toggle-pw');
    const eyeOpen = document.getElementById('eye-open');
    const eyeClosed = document.getElementById('eye-closed');

    // Carrega e-mail salvo caso o usuário tenha marcado 'Lembrar meu e-mail'
    try {{
      const savedEmail = localStorage.getItem('gold_saved_email');
      if (savedEmail) {{
        emailInput.value = savedEmail;
      }}
    }} catch {{}}

    togglePw.addEventListener('click', () => {{
      const isPw = senhaInput.type === 'password';
      senhaInput.type = isPw ? 'text' : 'password';
      eyeOpen.classList.toggle('hidden', isPw);
      eyeClosed.classList.toggle('hidden', !isPw);
    }});

    function abrirModalRecuperacao() {{
      const modal = document.getElementById('forgot-modal');
      const fEmail = document.getElementById('forgot-email');
      const feedback = document.getElementById('forgot-feedback');
      feedback.classList.add('hidden');
      if (emailInput.value.trim()) {{
        fEmail.value = emailInput.value.trim();
      }}
      modal.classList.remove('hidden');
      setTimeout(() => fEmail.focus(), 50);
    }}

    function fecharModalRecuperacao() {{
      document.getElementById('forgot-modal').classList.add('hidden');
    }}

    window.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') fecharModalRecuperacao();
    }});

    document.getElementById('forgot-form').addEventListener('submit', async (e) => {{
      e.preventDefault();
      const email = document.getElementById('forgot-email').value.trim();
      const observacao = document.getElementById('forgot-obs').value.trim();
      const feedback = document.getElementById('forgot-feedback');
      const btn = document.getElementById('forgot-submit');

      btn.disabled = true;
      btn.textContent = 'Enviando...';

      try {{
        const res = await fetch('/api/auth/forgot-password', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ email, observacao }})
        }});
        const data = await res.json();
        feedback.className = 'rounded-xl p-3 text-xs font-bold bg-emerald-50 text-emerald-800 border border-emerald-200';
        feedback.textContent = data.message || 'Solicitação registrada com sucesso!';
        feedback.classList.remove('hidden');
      }} catch {{
        feedback.className = 'rounded-xl p-3 text-xs font-bold bg-red-50 text-red-800 border border-red-200';
        feedback.textContent = 'Não foi possível enviar agora. Acione o suporte diretamente.';
        feedback.classList.remove('hidden');
      }} finally {{
        btn.disabled = false;
        btn.textContent = 'Solicitar Nova Senha';
      }}
    }});

    form.addEventListener('submit', async (e) => {{
      e.preventDefault();
      errorBanner.classList.add('hidden');

      const email = emailInput.value.trim();
      const senha = senhaInput.value;
      const lembrar = lembrarInput.checked;

      if (!email || !senha) {{
        errorText.textContent = 'Por favor, preencha seu e-mail e sua senha.';
        errorBanner.classList.remove('hidden');
        return;
      }}

      try {{
        if (lembrar) {{
          localStorage.setItem('gold_saved_email', email);
        }} else {{
          localStorage.removeItem('gold_saved_email');
        }}
      }} catch {{}}

      submitBtn.disabled = true;
      submitLabel.textContent = 'Autenticando...';
      submitArrow.classList.add('hidden');
      submitSpinner.classList.remove('hidden');

      try {{
        const res = await fetch('/api/auth/login', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ email, senha, lembrar }})
        }});
        const data = await res.json();
        if (!res.ok) {{
          throw new Error(data.detail || 'E-mail ou senha incorretos.');
        }}

        const params = new URLSearchParams(window.location.search);
        const rd = params.get('rd');
        if (rd && !rd.includes('auth.goldcorretora.com.br')) {{
          window.location.href = rd;
        }} else if ('{default_redirect}' && '{default_redirect}' !== 'https://goldcorretora.com.br') {{
          window.location.href = '{default_redirect}';
        }} else {{
          window.location.href = 'https://vendas.goldcorretora.com.br';
        }}
      }} catch (err) {{
        errorText.textContent = err.message || 'Não foi possível conectar ao servidor.';
        errorBanner.classList.remove('hidden');
        submitBtn.disabled = false;
        submitLabel.textContent = 'Entrar no Portal Gold';
        submitArrow.classList.remove('hidden');
        submitSpinner.classList.add('hidden');
      }}
    }});
  </script>
</body>
</html>"""


def get_admin_html(default_redirect: str = "https://vendas.goldcorretora.com.br") -> str:
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
          {GOLD_LOGO_HEADER}
        </a>
        <div class="hidden sm:block border-l border-slate-700/70 pl-4">
          <span class="text-xs font-extrabold uppercase tracking-wider text-gold-400 block">
            Portal de Acessos Gold
          </span>
          <span class="text-[11px] text-slate-300 font-medium block">
            Controle de Vendedores, Cargos & Auditoria em Tempo Real
          </span>
        </div>
      </div>

      <div class="flex items-center gap-2.5">
        <a
          href="{default_redirect}"
          class="btn-tactile px-3.5 py-2 rounded-xl text-xs font-bold bg-white/10 hover:bg-white/15 text-white border border-white/15 flex items-center gap-1.5"
        >
          <span>Abrir Painel de Vendas</span>
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
          class="btn-tactile px-3 py-2 rounded-xl text-xs font-bold bg-red-500/15 hover:bg-red-500/25 text-red-200 border border-red-500/30"
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
          Gestão da Equipe & Auditoria Operacional
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
          <span class="text-xs font-bold text-slate-600 block">Usuários Ativos</span>
          <strong id="kpi-active-users" class="text-2xl font-extrabold text-navy-900 tabular-nums mt-0.5 block">—</strong>
        </div>
        <span class="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-bold border border-emerald-200">Acesso Liberado</span>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 p-4 flex items-center justify-between">
        <div>
          <span class="text-xs font-bold text-slate-600 block">Sessões Conectadas</span>
          <strong id="kpi-active-sessions" class="text-2xl font-extrabold text-navy-900 tabular-nums mt-0.5 block">—</strong>
        </div>
        <span class="px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 text-xs font-bold border border-amber-200">Dispositivos logados</span>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 p-4 flex items-center justify-between">
        <div>
          <span class="text-xs font-bold text-slate-600 block">Eventos Auditados (Recentes)</span>
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
            <option value="painel-vendedor">Painel de Vendas</option>
            <option value="gold-db-api">API de Leads & Carteira</option>
            <option value="gold-auth">Portal de Acesso (Logins / Senhas)</option>
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

        <div class="flex items-center gap-2 text-xs text-slate-600 font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span>Atualização automática a cada 10s</span>
        </div>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-[11px] font-extrabold text-slate-600 uppercase">
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
                <td colspan="6" class="py-10 text-center text-slate-500 font-medium">Carregando registros de atividade...</td>
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
          <p class="text-xs text-slate-600">Crie logins, redefina senhas, defina quais aplicativos cada pessoa pode abrir ou bloqueie o acesso instantaneamente.</p>
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
              <tr class="bg-slate-50 border-b border-slate-200 text-[11px] font-extrabold text-slate-600 uppercase">
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
                <td colspan="6" class="py-10 text-center text-slate-500">Carregando equipe...</td>
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
          <p class="text-xs text-slate-600">Crie novos cargos (ex: Financeiro, Pós-Venda, Auditor) e defina exatamente quais permissões possuem.</p>
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
        <button type="button" onclick="fecharModalUsuario()" class="w-8 h-8 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 flex items-center justify-center font-bold">✕</button>
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
            <label for="u-senha" class="block text-xs font-bold text-slate-700 mb-1">Senha <span id="u-senha-hint" class="text-[11px] font-normal text-slate-500"></span></label>
            <input id="u-senha" type="password" placeholder="Mínimo 4 caracteres" class="w-full h-10 rounded-xl border border-slate-300 px-3 text-sm font-medium text-navy-900 focus:outline-none focus:border-gold-500" />
          </div>
        </div>

        <div>
          <span class="block text-xs font-bold text-slate-700 mb-1.5">Aplicativos Liberados para este Usuário</span>
          <div class="grid grid-cols-2 gap-2 bg-slate-50 p-3 rounded-xl border border-slate-200 text-xs font-semibold text-navy-900">
            <label class="flex items-center gap-2"><input type="checkbox" name="u-app" value="painel-vendedor" checked class="rounded text-gold-600" /> Painel de Vendas</label>
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
        <button type="button" onclick="fecharModalCargo()" class="w-8 h-8 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 flex items-center justify-center font-bold">✕</button>
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

      const sel = document.getElementById('u-cargo');
      sel.innerHTML = stateRoles.map(r => `<option value="${{r.codigo}}">${{r.nome}} (${{r.codigo}})</option>`).join('');

      const grid = document.getElementById('roles-grid');
      grid.innerHTML = stateRoles.map(r => `
        <div class="bg-white rounded-2xl border border-slate-200 p-5 flex flex-col justify-between gap-4 shadow-xs">
          <div>
            <div class="flex items-center justify-between gap-2">
              <span class="font-mono text-xs font-bold px-2.5 py-1 rounded-lg bg-navy-900 text-gold-400">${{r.codigo}}</span>
              ${{r.is_system ? '<span class="text-[11px] font-bold text-slate-500">Cargo Nativo</span>' : `
                <button onclick="removerCargo('${{r.codigo}}')" class="text-xs font-bold text-red-600 hover:underline">Excluir</button>
              `}}
            </div>
            <h3 class="text-base font-extrabold text-navy-900 mt-3">${{r.nome}}</h3>
            <p class="text-xs text-slate-600 mt-1">${{r.descricao || 'Sem descrição.'}}</p>
          </div>
          <div class="pt-3 border-t border-slate-100">
            <span class="text-[11px] font-bold text-slate-500 uppercase block mb-1.5">Permissões Atribuídas</span>
            <div class="flex flex-wrap gap-1.5">
              ${{(r.permissoes || []).map(p => `<span class="font-mono text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">${{p}}</span>`).join('') || '<span class="text-xs text-slate-500">Básicas</span>'}}
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

      const uFilter = document.getElementById('audit-user-filter');
      const currentVal = uFilter.value;
      uFilter.innerHTML = '<option value="TODOS">Todos os Usuários</option>' +
        stateUsers.map(u => `<option value="${{u.email}}">${{u.nome}} (${{u.email}})</option>`).join('');
      uFilter.value = currentVal || 'TODOS';

      const tbody = document.getElementById('users-tbody');
      if (stateUsers.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="6" class="py-8 text-center text-slate-500">Nenhum usuário cadastrado.</td></tr>';
        return;
      }}

      tbody.innerHTML = stateUsers.map(u => `
        <tr class="hover:bg-slate-50/80">
          <td class="py-3.5 px-4">
            <div class="font-bold text-navy-900">${{u.nome}}</div>
            <div class="text-xs text-slate-600 font-mono">${{u.email}}</div>
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
              Editar / Senha
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
        return `<span class="font-semibold text-navy-900">Lead #${{d.lead_id || ''}} (${{d.lead_nome || ''}})</span> → <span class="px-1.5 py-0.5 rounded bg-amber-100 text-amber-900 font-bold text-xs">${{d.novo_status || ''}}</span> ${{d.observacoes ? `<span class="text-slate-600 italic">"${{d.observacoes}}"</span>` : ''}}`;
      }}
      if (d.alvo_email) {{
        return `Usuário alvo: <span class="font-mono font-semibold">${{d.alvo_email}}</span>`;
      }}
      if (d.motivo) {{
        return `<span class="text-red-600 font-medium">${{d.motivo}}</span>`;
      }}
      const str = JSON.stringify(d);
      return str === '{{}}' ? `<span class="text-slate-500 font-mono">${{item.rota || '/'}}</span>` : `<span class="font-mono text-xs text-slate-600">${{str}}</span>`;
    }}

    function badgeAcao(acao) {{
      if (acao.includes('FALHA') || acao.includes('NEGADO') || acao.includes('BLOQUEADO')) {{
        return `<span class="px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200 font-mono text-[11px] font-bold">${{acao}}</span>`;
      }}
      if (acao.includes('REDEFINICAO_SENHA')) {{
        return `<span class="px-2 py-0.5 rounded-md bg-purple-50 text-purple-800 border border-purple-200 font-mono text-[11px] font-bold">${{acao}}</span>`;
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
              <p class="text-xs text-slate-600 mt-1">Assim que os vendedores acessarem ou interagirem com os leads, os eventos aparecerão aqui.</p>
            </td>
          </tr>
        `;
        return;
      }}

      tbody.innerHTML = stateAudit.map(item => `
        <tr class="hover:bg-slate-50/80">
          <td class="py-3 px-4 text-xs text-slate-600 tabular-nums whitespace-nowrap">
            ${{fmtData(item.created_at)}}
          </td>
          <td class="py-3 px-4">
            <div class="font-bold text-navy-900">${{item.usuario_nome || 'Visitante'}}</div>
            <div class="text-[11px] text-slate-600 font-mono">${{item.usuario_email || '—'}} ${{item.usuario_cargo ? `• ${{item.usuario_cargo}}` : ''}}</div>
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
          <td class="py-3 px-4 text-xs font-mono text-slate-500 tabular-nums">
            ${{item.ip || '—'}}
          </td>
        </tr>
      `).join('');
    }}

    function debounceAudit() {{
      clearTimeout(auditDebounceTimer);
      auditDebounceTimer = setTimeout(carregarAuditoria, 250);
    }}

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
