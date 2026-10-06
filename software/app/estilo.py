"""Estilo visual heredado de AgroVision 360: degradados verde-turquesa, tarjetas redondeadas."""
from html import escape

from i18n import t

CSS = """
<style>
@import url("https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap");
:root {
  --verde: linear-gradient(135deg, #22c55e 0%, #059669 100%);
  --hero: linear-gradient(120deg, #16a34a 0%, #0d9488 100%);
  --naranja: linear-gradient(135deg, #f97316 0%, #ef4444 100%);
  --azul: linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%);
  --morado: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
  --cielo: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
}
.stApp, .stApp p, .stApp label, .stApp input, .stApp button, .stMarkdown, h1, h2, h3 {
  font-family: 'Nunito', system-ui, sans-serif; }
h1, h2, h3 { font-weight: 900 !important; letter-spacing: -0.01em; color: #111827; }
.block-container { padding-top: 1.6rem; max-width: 1280px; }
section[data-testid="stSidebar"] { background: #ffffff; border-right: 4px solid #10b981; }
section[data-testid="stSidebar"] [role="radiogroup"] { width: 100%; }
section[data-testid="stSidebar"] [role="radiogroup"] label {
  padding: .75rem 1rem; border-radius: 14px; margin: 0 0 .35rem 0; width: 100% !important;
  font-weight: 700; transition: background .15s; box-sizing: border-box;
}
section[data-testid="stSidebar"] [role="radiogroup"] label p { font-size: 1.02rem; font-weight: 700; color: #1f2937; }
section[data-testid="stSidebar"] [role="radiogroup"] label > div > div:first-child { display: none !important; }
section[data-testid="stSidebar"] [role="radiogroup"] *:has(> label) { width: 100%; }
section[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: #ecfdf5; }
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background: var(--verde); color: #fff; box-shadow: 0 8px 18px -8px rgba(5,150,105,.7);
}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p { color: #fff; }
section[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
.av-marca { display: flex; align-items: center; gap: .7rem; margin-bottom: 1.2rem; }
.av-logo { width: 44px; height: 44px; border-radius: 14px; background: var(--verde);
  display: grid; place-items: center; color: #fff; }
.av-marca b { display: block; font-size: 1.35rem; font-weight: 900;
  background: var(--hero); -webkit-background-clip: text; background-clip: text; color: transparent; }
.av-marca small { color: #6b7280; font-weight: 600; }
.av-etiqueta { font-size: .72rem; font-weight: 800; color: #059669; letter-spacing: .08em; }
.av-hero { background: var(--hero); border-radius: 26px; padding: 2rem 2.2rem; color: #fff;
  display: flex; justify-content: space-between; align-items: center; gap: 1rem;
  position: relative; overflow: hidden; margin-bottom: 1.2rem; flex-wrap: wrap; }
.av-hero::after { content: ""; position: absolute; width: 260px; height: 260px; border-radius: 50%;
  background: rgba(255,255,255,.08); right: -60px; top: -90px; }
.av-hero .estado { font-size: .78rem; font-weight: 800; letter-spacing: .06em; opacity: .95; }
.av-hero h1 { color: #fff !important; font-size: 2.3rem; margin: .2rem 0; padding: 0; }
.av-hero p { margin: 0; font-weight: 700; opacity: .95; }
.av-reloj { background: rgba(255,255,255,.15); border-radius: 18px; padding: 1rem 1.4rem; z-index: 1; }
.av-reloj small { font-weight: 700; opacity: .9; }
.av-reloj b { display: block; font-size: 2rem; font-weight: 900; }
.av-tarjeta { border-radius: 20px; padding: 1.2rem 1.3rem; color: #fff; min-height: 150px;
  position: relative; overflow: hidden; box-shadow: 0 12px 24px -16px rgba(0,0,0,.45); margin-bottom: 1rem; }
.av-tarjeta::after { content: ""; position: absolute; width: 120px; height: 120px; border-radius: 50%;
  background: rgba(255,255,255,.12); right: -30px; top: -40px; }
.av-tarjeta .icono { width: 44px; height: 44px; border-radius: 12px; background: rgba(255,255,255,.22);
  display: grid; place-items: center; margin-bottom: .8rem; }
.av-tarjeta .titulo { font-weight: 700; font-size: .95rem; opacity: .95; }
.av-tarjeta .valor { font-weight: 900; font-size: 2.1rem; line-height: 1.1; }
.av-tarjeta .valor small { font-size: 1rem; font-weight: 800; opacity: .9; margin-left: .2rem; }
.av-tarjeta .nota { position: absolute; right: 1rem; top: 1rem; background: rgba(255,255,255,.2);
  border-radius: 999px; padding: .15rem .6rem; font-size: .78rem; font-weight: 800; z-index: 1; }
.verde { background: var(--verde); } .naranja { background: var(--naranja); }
.azul { background: var(--azul); } .morado { background: var(--morado); } .cielo { background: var(--cielo); }
.av-panel { background: #fff; border-radius: 22px; padding: 1.3rem 1.4rem;
  box-shadow: 0 10px 30px -22px rgba(0,0,0,.35); margin-bottom: 1rem; }
.av-panel h3 { margin: 0 0 .8rem 0; font-size: 1.25rem; }
.av-alerta { border-left: 4px solid; border-radius: 12px; padding: .7rem .9rem; margin-bottom: .55rem;
  font-weight: 700; color: #1f2937; }
.av-alerta.alto { border-color: #ef4444; background: #fef2f2; }
.av-alerta.medio { border-color: #f97316; background: #fff7ed; }
.av-alerta.info { border-color: #3b82f6; background: #eff6ff; }
.av-alerta.ok { border-color: #22c55e; background: #f0fdf4; }
.av-alerta small { display: block; font-weight: 600; color: #6b7280; }
.av-clima { border-radius: 22px; padding: 1.4rem; color: #fff; background: var(--cielo); margin-bottom: 1rem; }
.av-clima .lugar { font-weight: 800; }
.av-clima .temp { font-size: 2.4rem; font-weight: 900; }
.av-clima .fila { display: grid; grid-template-columns: repeat(3, 1fr); gap: .7rem; margin-top: .9rem; }
.av-clima .fila div { background: rgba(255,255,255,.18); border-radius: 14px; padding: .7rem .8rem; }
.av-clima .fila b { display: block; font-size: 1.35rem; font-weight: 900; }
.av-oferta { background: #fff; border-radius: 18px; padding: 1rem 1.1rem; margin-bottom: 1rem;
  border-top: 5px solid #10b981; box-shadow: 0 10px 24px -20px rgba(0,0,0,.4); }
.av-oferta b { font-size: 1.1rem; font-weight: 900; text-transform: capitalize; }
.av-oferta .precio { color: #059669; font-weight: 900; font-size: 1.4rem; }
.av-oferta small { color: #6b7280; font-weight: 600; display: block; }
div.stButton > button, div.stFormSubmitButton > button {
  background: var(--verde); color: #fff; border: 0; border-radius: 14px; font-weight: 800;
  padding: .55rem 1.3rem; box-shadow: 0 8px 18px -10px rgba(5,150,105,.8);
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover { color: #fff; filter: brightness(1.05); }
[data-testid="stForm"] { background: #fff; border-radius: 22px; border: 1px solid #d1fae5; padding: 1.2rem; }
.stTabs [aria-selected="true"] { color: #059669 !important; }
[data-testid="stMain"] [data-testid="stTextInput"] div:has(> input),
[data-testid="stMain"] [data-testid="stNumberInput"] div:has(> input),
[data-testid="stMain"] [data-testid="stDateInput"] div:has(> input),
[data-testid="stMain"] [data-testid="stSelectbox"] div:has(> input) {
  background: #eef4fb !important; border: 1px solid #dbe5f0 !important; border-radius: 12px !important; }
[data-testid="stMain"] [data-testid="stTextInput"] div:has(> input):focus-within,
[data-testid="stMain"] [data-testid="stNumberInput"] div:has(> input):focus-within { border-color: #10b981 !important; }
</style>
"""

ICONOS = {
    "hoja": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "termometro": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "gotas": '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
    "tendencia": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "plaga": '<path d="m8 2 1.88 1.88"/><path d="M14.12 3.88 16 2"/><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"/><path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6"/><path d="M12 20v-9"/><path d="M6 13H2"/><path d="M22 13h-4"/>',
    "tienda": '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
    "campana": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "sol": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "nube": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
}


def icono(nombre, tam=24):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{tam}" height="{tam}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round">{ICONOS[nombre]}</svg>')


def marca(nombre, subtitulo):
    return (f'<div class="av-marca"><div class="av-logo">{icono("hoja", 24)}</div>'
            f'<div><b>{escape(nombre)}</b><small>{escape(subtitulo)}</small></div></div>')


def hero(titulo, subtitulo, hora, fecha):
    return (f'<div class="av-hero"><div><div class="estado">● {t("SISTEMA ACTIVO · EN LÍNEA")}</div>'
            f'<h1>{escape(titulo)}</h1><p>{escape(subtitulo)}</p></div>'
            f'<div class="av-reloj"><small>{t("Hora actual")}</small><b>{hora}</b><small>{escape(fecha)}</small></div></div>')


def tarjeta(titulo, valor, unidad="", color="verde", icono_nombre="hoja", nota=None):
    nota_html = f'<span class="nota">{escape(str(nota))}</span>' if nota is not None else ""
    return (f'<div class="av-tarjeta {color}">{nota_html}<div class="icono">{icono(icono_nombre)}</div>'
            f'<div class="titulo">{escape(titulo)}</div>'
            f'<div class="valor">{escape(str(valor))}<small>{escape(unidad)}</small></div></div>')


def alerta(texto, detalle="", nivel="info"):
    detalle_html = f"<small>{escape(detalle)}</small>" if detalle else ""
    return f'<div class="av-alerta {nivel}">{escape(texto)}{detalle_html}</div>'


def panel(titulo, contenido_html):
    return f'<div class="av-panel"><h3>{escape(titulo)}</h3>{contenido_html}</div>'


def tarjeta_clima(lugar, temp, humedad, precip, tmin):
    return (f'<div class="av-clima"><div class="lugar">{escape(lugar)}</div>'
            f'<span class="av-sol">{icono("sol", 46)}</span>'
            f'<div class="temp">{temp}°C</div><div class="fila">'
            f'<div><b>{humedad}%</b>{t("Humedad")}</div><div><b>{precip} mm</b>{t("Lluvia hoy")}</div>'
            f'<div><b>{tmin}°C</b>{t("Mínima hoy")}</div></div></div>')


def tarjeta_oferta(oferta):
    lugar = f" · {escape(oferta['lugar'])}" if oferta.get("lugar") else ""
    contacto = escape(oferta["contacto"]) if oferta.get("contacto") else t("Sin contacto")
    return (f'<div class="av-oferta"><b>{escape(oferta["producto"])}</b>'
            f'<div class="precio">S/ {oferta["precio_kg"]:.2f} <small style="display:inline">{t("por kg")}</small></div>'
            f'<small>{oferta["cantidad_kg"]:.0f} {t("kg disponibles")} · {escape(oferta["productor"])}{lugar}</small>'
            f'<small>{contacto} · {t("publicado")} {escape(oferta["fecha"])}</small></div>')


CSS_LOGIN = """
<style>
section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none !important; }
[data-testid="stMain"] .block-container { max-width: 1120px; padding-top: 3rem; }
.av-bienvenida { font-size: 2.1rem !important; margin: .4rem 0 0 0 !important; }
.av-sub { color: #4b5563; font-weight: 600; margin-bottom: .6rem; }
.av-login-panel { background: linear-gradient(150deg, #059669 0%, #0f766e 55%, #0369a1 100%);
  border-radius: 28px; padding: 2.4rem 2rem; color: #fff; text-align: center;
  position: relative; overflow: hidden; min-height: 560px; }
.av-login-panel::before { content: ""; position: absolute; width: 220px; height: 220px; border-radius: 50%;
  background: rgba(255,255,255,.12); right: -70px; top: -70px; }
.av-login-panel::after { content: ""; position: absolute; width: 200px; height: 200px; border-radius: 50%;
  background: rgba(255,255,255,.10); left: -70px; bottom: -80px; }
.av-login-logo { width: 96px; height: 96px; border-radius: 26px; background: rgba(255,255,255,.18);
  display: grid; place-items: center; margin: 0 auto 1.2rem auto; transform: rotate(4deg); }
.av-login-panel h2 { color: #fff !important; font-size: 2.5rem !important; line-height: 1.05; margin: 0 0 .7rem 0; }
.av-login-panel p { font-weight: 700; font-size: 1.05rem; opacity: .95; margin-bottom: 1.4rem; }
.av-login-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .9rem; position: relative; z-index: 1; }
.av-login-grid div { background: rgba(255,255,255,.12); border-radius: 18px; padding: 1rem .6rem; font-weight: 800; }
.av-login-grid span { width: 46px; height: 46px; border-radius: 14px; display: grid; place-items: center;
  margin: 0 auto .6rem auto; }
.av-login-cifras { display: flex; justify-content: space-around; margin-top: 1.6rem; padding-top: 1.2rem;
  border-top: 1px solid rgba(255,255,255,.25); position: relative; z-index: 1; }
.av-login-cifras b { display: block; font-size: 1.9rem; font-weight: 900; }
.av-login-cifras small { font-weight: 700; }
</style>
"""


def panel_login():
    tiles = [("tendencia", "linear-gradient(135deg,#f59e0b,#f97316)", t("Riesgo climático")),
             ("plaga", "linear-gradient(135deg,#a855f7,#ec4899)", t("Alertas de plagas")),
             ("tienda", "linear-gradient(135deg,#3b82f6,#06b6d4)", t("Precios de mercado")),
             ("hoja", "linear-gradient(135deg,#22c55e,#10b981)", t("Venta directa"))]
    grid = "".join(f'<div><span style="background:{fondo}">{icono(ic)}</span>{texto}</div>'
                   for ic, fondo, texto in tiles)
    return (f'<div class="av-login-panel"><div class="av-login-logo">{icono("hoja", 48)}</div>'
            f'<h2>{t("Agricultura Inteligente")}</h2>'
            f'<p>{t("Monitorea el clima, las plagas y el mercado de tu parcela en el altiplano")}</p>'
            f'<div class="av-login-grid">{grid}</div>'
            f'<div class="av-login-cifras"><div><b>4</b><small>{t("Cultivos")}</small></div>'
            f'<div><b>14</b><small>{t("Días de clima")}</small></div>'
            f'<div><b>{t("Gratis")}</b><small>{t("Código abierto")}</small></div></div></div>')


CSS_LANDING = """
<style>
[data-testid="stMain"] .block-container { max-width: 1180px; padding-top: 1.2rem; }
.lp-hero { background: linear-gradient(120deg, #16a34a 0%, #0d9488 60%, #0369a1 100%); border-radius: 32px;
  padding: 3.2rem 3rem; color: #fff; position: relative; overflow: hidden; margin: .6rem 0 1.4rem 0; }
.lp-hero::before { content: ""; position: absolute; width: 380px; height: 380px; border-radius: 50%;
  background: rgba(255,255,255,.08); right: -90px; top: -140px; }
.lp-hero::after { content: ""; position: absolute; width: 240px; height: 240px; border-radius: 50%;
  background: rgba(255,255,255,.07); right: 180px; bottom: -150px; }
.lp-chip { display: inline-block; background: rgba(255,255,255,.18); border-radius: 999px; padding: .3rem .9rem;
  font-size: .8rem; font-weight: 800; letter-spacing: .05em; }
.lp-hero h1 { color: #fff !important; font-size: 3rem !important; line-height: 1.05; margin: 1rem 0 .8rem 0;
  max-width: 720px; position: relative; z-index: 1; }
.lp-hero p { font-size: 1.15rem; font-weight: 700; opacity: .95; max-width: 620px; position: relative; z-index: 1; }
.lp-cifras { display: flex; gap: 2.4rem; margin-top: 1.8rem; position: relative; z-index: 1; flex-wrap: wrap; }
.lp-cifras b { display: block; font-size: 2rem; font-weight: 900; }
.lp-cifras small { font-weight: 700; opacity: .9; }
.lp-titulo { text-align: center; margin: 2.2rem 0 1.2rem 0; }
.lp-titulo small { color: #059669; font-weight: 900; letter-spacing: .08em; }
.lp-titulo h2 { font-size: 2rem !important; margin: .2rem 0 !important; }
.lp-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.lp-card { background: #fff; border-radius: 22px; padding: 1.4rem 1.2rem; box-shadow: 0 14px 30px -24px rgba(0,0,0,.45); }
.lp-card span { width: 50px; height: 50px; border-radius: 15px; display: grid; place-items: center; color: #fff;
  margin-bottom: .9rem; }
.lp-card b { display: block; font-size: 1.1rem; font-weight: 900; margin-bottom: .3rem; }
.lp-card p { color: #4b5563; font-weight: 600; font-size: .93rem; margin: 0; }
.lp-pasos { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.lp-paso { background: #fff; border-radius: 22px; padding: 1.3rem; border-top: 5px solid #10b981; }
.lp-paso i { font-style: normal; font-size: 2rem; font-weight: 900; color: #10b981; }
.lp-paso b { display: block; font-size: 1.05rem; font-weight: 900; margin: .2rem 0; }
.lp-paso p { color: #4b5563; font-weight: 600; margin: 0; font-size: .93rem; }
.lp-equipo { background: #fff; border-radius: 26px; padding: 1.8rem; text-align: center; }
.lp-equipo p { color: #4b5563; font-weight: 600; max-width: 760px; margin: 0 auto 1rem auto; }
.lp-nombres { display: flex; flex-wrap: wrap; gap: .6rem; justify-content: center; }
.lp-nombres span { background: #ecfdf5; color: #065f46; border-radius: 999px; padding: .45rem 1rem; font-weight: 800; }
.lp-pie { margin-top: 2rem; background: #0f172a; color: #cbd5e1; border-radius: 26px; padding: 1.6rem 2rem;
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem; font-weight: 600; }
.lp-pie b { color: #fff; font-weight: 900; }
@media (max-width: 900px) {
  .lp-grid { grid-template-columns: repeat(2, 1fr); } .lp-pasos { grid-template-columns: 1fr; }
  .lp-hero { padding: 2rem 1.4rem; } .lp-hero h1 { font-size: 2.1rem !important; }
}
</style>
"""

EQUIPO = ["Richar Andre Vilca Solorzano", "Flor Melany Yanarico Huanca", "Yeferson Dariun Laura Livise",
          "Leonardo Sebastián Grimaldos Ávila", "Dina Maribel Yana Yucra"]


def landing_hero():
    return (f'<div class="lp-hero"><span class="lp-chip">● {t("PLATAFORMA ABIERTA · ALTIPLANO DE PUNO")}</span>'
            f'<h1>{t("Clima, plagas y mercado en una sola plataforma")}</h1>'
            f'<p>{t("Alertas de helada y de rancha, registro de plagas en campo y precios para decidir cuándo vender. Gratis y de código abierto.")}</p>'
            f'<div class="lp-cifras"><div><b>14</b><small>{t("días de clima")}</small></div>'
            f'<div><b>4</b><small>{t("cultivos andinos")}</small></div><div><b>2</b><small>{t("criterios de rancha")}</small></div>'
            f'<div><b>{t("Gratis")}</b><small>{t("y abierto")}</small></div></div></div>')


def landing_funciones():
    items = [("nube", "linear-gradient(135deg,#3b82f6,#06b6d4)", t("Riesgo climático"),
              t("Heladas por cultivo, rachas secas y grados-día con datos abiertos de Open-Meteo.")),
             ("plaga", "linear-gradient(135deg,#f97316,#ef4444)", t("Alertas de plagas"),
              t("Periodos críticos de rancha y evaluaciones de campo con umbral de acción.")),
             ("tendencia", "linear-gradient(135deg,#a855f7,#ec4899)", t("Precios de mercado"),
              t("Tendencia, estacionalidad, mejor mes de venta y precio de equilibrio.")),
             ("tienda", "linear-gradient(135deg,#22c55e,#059669)", t("Venta directa"),
              t("Publica tu cosecha y conecta con compradores sin intermediarios."))]
    tarjetas = "".join(f'<div class="lp-card"><span style="background:{fondo}">{icono(ic, 26)}</span>'
                       f'<b>{titulo}</b><p>{texto}</p></div>' for ic, fondo, titulo, texto in items)
    return (f'<div class="lp-titulo"><small>{t("SERVICIOS")}</small><h2>{t("Todo lo que necesitas para tu parcela")}</h2></div>'
            f'<div class="lp-grid">{tarjetas}</div>')


def landing_pasos():
    pasos = [("1", t("Crea tu cuenta"), t("Regístrate gratis con tu usuario y contraseña.")),
             ("2", t("Registra tus parcelas"), t("Indica el cultivo y la ubicación de cada parcela.")),
             ("3", t("Recibe alertas"), t("Revisa el clima, las plagas y los precios cada día."))]
    tarjetas = "".join(f'<div class="lp-paso"><i>{n}</i><b>{titulo}</b><p>{texto}</p></div>' for n, titulo, texto in pasos)
    return (f'<div class="lp-titulo"><small>{t("CÓMO FUNCIONA")}</small><h2>{t("Empieza en tres pasos")}</h2></div>'
            f'<div class="lp-pasos">{tarjetas}</div>')


def landing_equipo():
    nombres = "".join(f"<span>{escape(n)}</span>" for n in EQUIPO)
    texto = t("El proyecto empezó en 2025 en los cursos de Ingeniería de Software y Taller de Desarrollo de Software "
              "de la Universidad Nacional del Altiplano, como Green Modern Agrifarm y luego AgroVision 360. "
              "Esta versión la desarrolla el equipo original:")
    return (f'<div class="lp-titulo"><small>{t("ACERCA DE")}</small><h2>{t("Nacido en las aulas de la UNAP")}</h2></div>'
            f'<div class="lp-equipo"><p>{texto}</p><div class="lp-nombres">{nombres}</div></div>')


def landing_pie():
    return (f'<div class="lp-pie"><div><b>AgriFarm AgroVision</b><br>'
            f'{t("Escuela Profesional de Ingeniería Estadística e Informática · UNAP, Puno")}</div>'
            f'<div><b>{t("Contacto")}</b><br>andrevilcasolorzano@gmail.com</div>'
            f'<div><b>{t("Licencia")}</b><br>{t("MIT · código abierto")}</div></div>')


MENU_CSS_BASE = """
<style>
.av-menu-titulo { font-size: 1.5rem; font-weight: 900; color: #111827; margin: .1rem 0 .8rem 0; }
section[data-testid="stSidebar"] [class*="st-key-nav_"] button {
  background: transparent !important; box-shadow: none !important; border: 0 !important;
  justify-content: flex-start !important; padding: .55rem .7rem !important; border-radius: 16px !important;
  font-weight: 700 !important; font-size: 1rem !important; min-height: 52px; }
section[data-testid="stSidebar"] [class*="st-key-nav_"] button > div {
  justify-content: flex-start !important; width: 100%; }
section[data-testid="stSidebar"] [class*="st-key-nav_"] button:hover { filter: none; background: #f8fafc !important; }
section[data-testid="stSidebar"] [class*="st-key-nav_"] button [data-testid="stIconMaterial"] {
  padding: 7px; border-radius: 11px; margin-right: .55rem; font-size: 1.3rem; }
section[data-testid="stSidebar"] .st-key-salir button { background: #f1f5f9 !important; color: #334155 !important;
  box-shadow: none !important; }
.st-key-ver_alertas button { background: linear-gradient(90deg, #f97316, #ef4444) !important; color: #fff !important;
  box-shadow: 0 10px 20px -12px rgba(239,68,68,.9) !important; padding: .75rem !important; font-size: 1.02rem !important; }
.av-cabecera { display: flex; justify-content: space-between; align-items: center; background: #fff;
  border-radius: 20px; padding: .7rem 1rem .7rem 1.3rem; margin-bottom: 1rem;
  box-shadow: 0 10px 26px -24px rgba(0,0,0,.5); flex-wrap: wrap; gap: .6rem; }
.av-ruta { font-weight: 700; color: #6b7280; }
.av-ruta b { color: #059669; font-weight: 900; }
.av-chips { display: flex; gap: .6rem; align-items: center; }
.av-chip { background: #f1f5f9; border-radius: 12px; padding: .45rem .8rem; font-weight: 700; color: #334155; font-size: .9rem; }
.av-usuario { display: flex; gap: .6rem; align-items: center; background: #f8fafc; border-radius: 14px; padding: .35rem .8rem .35rem .4rem; }
.av-avatar { width: 38px; height: 38px; border-radius: 11px; background: linear-gradient(135deg,#10b981,#0d9488);
  color: #fff; display: grid; place-items: center; font-weight: 900; }
.av-usuario b { display: block; font-weight: 900; color: #111827; line-height: 1.1; }
.av-usuario small { color: #6b7280; font-weight: 600; }
.av-panel .av-titulo-alertas { display: flex; justify-content: space-between; align-items: center; color: #f97316; }
.av-panel .av-titulo-alertas h3 { margin: 0; color: #111827 !important; }
.av-clima { position: relative; }
.av-sol { position: absolute; right: 1.3rem; top: 1.1rem; color: #fde047; }
</style>
"""


def css_menu(menu, activa):
    reglas = []
    for nombre, _, color, fondo in menu:
        selector = f'section[data-testid="stSidebar"] .st-key-nav_{nombre} button'
        if nombre == activa:
            reglas.append(f"{selector}, {selector}:hover {{ background: var(--verde) !important; color: #fff !important; "
                          f"box-shadow: 0 10px 22px -10px rgba(5,150,105,.75) !important; }}")
            reglas.append(f"{selector} p::after {{ content: '→'; position: absolute; right: 1rem; }}")
            reglas.append(f"{selector} [data-testid=\"stIconMaterial\"] {{ background: rgba(255,255,255,.22); color: #fff; }}")
        else:
            reglas.append(f"{selector} {{ color: {color} !important; }}")
            reglas.append(f"{selector} [data-testid=\"stIconMaterial\"] {{ background: {fondo}; color: {color}; }}")
    return MENU_CSS_BASE + "<style>" + "\n".join(reglas) + "</style>"


def cabecera(seccion, nombre, ahora, rol, meses, idioma):
    iniciales = "".join(p[0] for p in nombre.split()[:2]).upper()
    return (f'<div class="av-cabecera"><div class="av-ruta">{t("Panel")} / <b>{escape(seccion)}</b></div>'
            f'<div class="av-chips"><span class="av-chip">🌐 {escape(idioma)}</span>'
            f'<span class="av-chip">{ahora.day} {meses[ahora.month - 1]} · {ahora.strftime("%H:%M")}</span>'
            f'<div class="av-usuario"><span class="av-avatar">{escape(iniciales)}</span>'
            f'<div><b>{escape(nombre)}</b><small>{escape(rol)}</small></div></div></div></div>')


def panel_alertas(contenido_html):
    return (f'<div class="av-panel"><div class="av-titulo-alertas"><h3>{t("Alertas recientes")}</h3>'
            f'{icono("campana", 24)}</div><div style="margin-top:.9rem">{contenido_html}</div></div>')
