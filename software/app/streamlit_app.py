"""Panel web. Ejecutar desde software: streamlit run app/streamlit_app.py"""
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "app"))
import estilo  # noqa: E402
import i18n  # noqa: E402
from i18n import t  # noqa: E402
from agrovision import auth, clima, db, mercado, plagas  # noqa: E402
from agrovision.config import CULTIVOS, ZONA_HORARIA, parametros_cultivo  # noqa: E402

NOMBRE_APP = "AgriFarm AgroVision"
st.set_page_config(page_title=NOMBRE_APP, page_icon="🌱", layout="wide")
i18n.idioma = st.session_state.get("idioma", "es")
MESES, DIAS = i18n.MESES[i18n.idioma], i18n.DIAS[i18n.idioma]
st.markdown(estilo.CSS, unsafe_allow_html=True)


def html(fragmento):
    st.markdown(fragmento, unsafe_allow_html=True)


def selector_idioma(clave):
    opciones = list(i18n.NOMBRES)
    elegido = st.selectbox(t("Idioma"), opciones, index=opciones.index(i18n.idioma),
                           format_func=i18n.NOMBRES.get, key=clave, label_visibility="collapsed")
    if elegido != i18n.idioma:
        st.session_state["idioma"] = elegido
        st.rerun()


@st.cache_resource
def conexion():
    return db.conectar()


@st.cache_data(ttl=1800, show_spinner="Consultando el clima…")
def clima_cacheado(lat, lon):
    return clima.obtener_clima(lat, lon)


def clima_seguro(parcela):
    try:
        return clima_cacheado(parcela["latitud"], parcela["longitud"])
    except OSError as error:
        st.error(f"No se pudo consultar Open-Meteo: {error}")
        return None


def alertas_parcela(parcela, datos):
    """Lista de (texto, detalle, nivel) para una parcela."""
    resultado = []
    if datos:
        hoy = date.today().isoformat()
        umbral = parametros_cultivo(parcela["cultivo"])["helada_critica"]
        for h in clima.riesgo_helada(datos["diario"], umbral):
            if h["fecha"] >= hoy:
                nivel = "alto" if h["nivel"] == "alto" else "medio"
                resultado.append((t(f"Riesgo {h['nivel']} de helada"), f"{h['fecha']}{t(' · mínima ')}{h['tmin']} °C", nivel))
        if parcela["cultivo"] == "papa":
            for fecha in plagas.periodos_criticos_rancha(datos["horario"], "hutton"):
                resultado.append((t("Periodo crítico de rancha (Hutton)"), fecha, "alto"))
    for a in plagas.alertas_monitoreo(con, parcela["id"]):
        if a["supera_umbral"]:
            resultado.append((f"{a['plaga'].capitalize()} {t('sobre el umbral')}",
                              f"{a['incidencia']} % ({t('umbral ')}{a['umbral']} %) · {t(a['tendencia'])}", "medio"))
    return resultado


con = conexion()


def ir_a(vista):
    st.session_state["vista"] = vista
    st.rerun()


def pantalla_landing():
    html(estilo.CSS_LOGIN + estilo.CSS_LANDING)
    marca, _, idioma_col, b1, b2 = st.columns([2.6, 0.9, 1, 1.1, 1.4], vertical_alignment="center")
    with idioma_col:
        selector_idioma("idioma_landing")
    with marca:
        html(estilo.marca(NOMBRE_APP, t("Sistema inteligente")))
    if b1.button(t("Iniciar sesión"), key="nav_login", width="stretch"):
        ir_a("login")
    if b2.button(t("Crear cuenta"), key="nav_registro", width="stretch"):
        ir_a("login")
    html(estilo.landing_hero())
    _, centro, _ = st.columns([1, 1, 1])
    if centro.button(t("Empieza gratis →"), key="cta", width="stretch"):
        ir_a("login")
    html(estilo.landing_funciones())
    html(estilo.landing_pasos())
    html(estilo.landing_equipo())
    html(estilo.landing_pie())


def pantalla_login():
    html(estilo.CSS_LOGIN)
    izquierda, derecha = st.columns([1, 1.05], gap="large")
    with izquierda:
        volver_col, idioma_col = st.columns([2, 1])
        with idioma_col:
            selector_idioma("idioma_login")
        if volver_col.button(t("← Volver al inicio"), key="volver"):
            ir_a("inicio")
        html(estilo.marca(NOMBRE_APP, t("Sistema inteligente")))
        entrar, registrar = st.tabs([t("Iniciar sesión"), t("Crear cuenta")])
        with entrar:
            html(f'<h2 class="av-bienvenida">{t("¡Bienvenido de vuelta!")}</h2>'
                 f'<p class="av-sub">{t("Inicia sesión para continuar con tu parcela")}</p>')
            with st.form("login"):
                usuario = st.text_input(t("Usuario"))
                password = st.text_input(t("Contraseña"), type="password")
                if st.form_submit_button(t("Iniciar sesión →"), width="stretch"):
                    datos = auth.verificar(con, usuario, password)
                    if datos:
                        st.session_state["usuario"] = datos
                        st.session_state["recien_entro"] = True
                        st.rerun()
                    st.error(t("Usuario o contraseña incorrectos."))
        with registrar:
            with st.form("registro", clear_on_submit=True):
                nombre = st.text_input("Nombre completo")
                nuevo = st.text_input(t("Usuario"), help=t("3 a 32 caracteres: letras, números, punto o guion"))
                clave = st.text_input(t("Contraseña"), type="password", help=t("Mínimo 8 caracteres"))
                repetir = st.text_input("Repite la contraseña", type="password")
                if st.form_submit_button(t("Crear cuenta"), width="stretch"):
                    if clave != repetir:
                        st.error(t("Las contraseñas no coinciden."))
                    else:
                        try:
                            auth.crear_usuario(con, nuevo, clave, nombre)
                            st.success(t("Cuenta creada. Ya puedes iniciar sesión."))
                        except ValueError as error:
                            st.error(str(error))
    with derecha:
        html(estilo.panel_login())


usuario_actual = st.session_state.get("usuario")
if usuario_actual is None:
    if st.session_state.get("vista", "inicio") == "inicio":
        pantalla_landing()
    else:
        pantalla_login()
    st.stop()

parcelas = db.listar_parcelas(con, usuario_actual["id"])

MENU = [  # (página, icono Material, color del texto, fondo del icono) como en AgroVision 360
    ("Inicio", ":material/home:", "#059669", "#ecfdf5"),
    ("Clima", ":material/cloud:", "#2563eb", "#eff6ff"),
    ("Plagas", ":material/bug_report:", "#dc2626", "#fef2f2"),
    ("Mercado", ":material/trending_up:", "#ea580c", "#fff7ed"),
    ("Ofertas", ":material/shopping_cart:", "#4f46e5", "#eef2ff"),
    ("Parcelas", ":material/grass:", "#16a34a", "#f0fdf4"),
]
pagina = st.session_state.get("pagina", "Inicio")
html(estilo.css_menu(MENU, pagina))

if st.session_state.pop("recien_entro", False):
    st.toast(f"{t('¡Bienvenido a ')}{NOMBRE_APP}!", icon="✅")

with st.sidebar:
    html(estilo.marca(NOMBRE_APP, t("Sistema inteligente")))
    selector_idioma("idioma_panel")
    html(f'<div class="av-etiqueta">● {t("NAVEGACIÓN")}</div><div class="av-menu-titulo">{t("Menú Principal")}</div>')
    for nombre, icono_menu, _, _ in MENU:
        if st.button(t(nombre), key=f"nav_{nombre}", icon=icono_menu, width="stretch"):
            st.session_state["pagina"] = nombre
            st.rerun()
    st.divider()
    parcela = None
    if parcelas:
        opciones = {f"{p['nombre']} · {p['cultivo']}": p for p in parcelas}
        parcela = opciones[st.selectbox(t("Parcela activa"), list(opciones))]
    else:
        st.caption(t("Aún no hay parcelas. Regístralas en «Parcelas»."))
    st.divider()
    if st.button(t("Cerrar sesión"), key="salir", icon=":material/logout:", width="stretch"):
        st.session_state.pop("usuario", None)
        st.session_state.pop("pagina", None)
        ir_a("inicio")

html(estilo.cabecera(t(pagina), usuario_actual["nombre"], datetime.now(ZoneInfo(ZONA_HORARIA)),
                     t(usuario_actual.get("rol", "productor")), MESES, i18n.idioma.upper()))


def pedir_parcela():
    if parcela is None:
        html(estilo.alerta(t("Primero registra una parcela"), t("Ve a la sección «Parcelas» del menú."), "info"))
        st.stop()


# ---------------------------------------------------------------- Inicio
if pagina == "Inicio":
    ahora = datetime.now(ZoneInfo(ZONA_HORARIA))
    if i18n.idioma == "es":
        fecha = f"{DIAS[ahora.weekday()]}, {ahora.day} de {MESES[ahora.month - 1]}"
    else:
        fecha = f"{DIAS[ahora.weekday()]}, {ahora.day} {MESES[ahora.month - 1]}"
    html(estilo.hero(f"{t('Hola, ')}{usuario_actual['nombre'].split()[0]} 👋", t("Tu panel de monitoreo climático, de plagas y de mercado"),
                     ahora.strftime("%H:%M"), fecha))
    datos = clima_seguro(parcela) if parcela else None
    alertas = alertas_parcela(parcela, datos) if parcela else []
    actual, dia = clima.condicion_actual(datos, ahora.strftime("%Y-%m-%dT%H")) if datos else (None, None)
    ofertas = mercado.listar_ofertas(con)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        html(estilo.tarjeta(t("Parcelas registradas"), len(parcelas), "", "verde", "hoja"))
    with c2:
        html(estilo.tarjeta(t("Mínima de hoy"), dia["tmin"] if dia else "–", "°C", "naranja", "termometro"))
    with c3:
        html(estilo.tarjeta(t("Humedad relativa"), actual["hr"] if actual else "–", "%", "azul", "gotas"))
    with c4:
        html(estilo.tarjeta(t("Ofertas activas"), len(ofertas), "", "morado", "tienda"))

    izquierda, derecha = st.columns([1.15, 1])
    with izquierda:
        if parcela and actual and dia:
            html(estilo.tarjeta_clima(f"{parcela['nombre']} · {parcela['latitud']:.2f}, {parcela['longitud']:.2f}",
                                      actual["temp"], actual["hr"], dia["precip"], dia["tmin"]))
        elif parcela:
            html(estilo.alerta(t("Sin datos de clima por ahora"), t("Revisa la conexión a internet."), "info"))
        else:
            html(estilo.alerta(t("Registra tu primera parcela"), t("Ve a «Parcelas» en el menú."), "info"))
    with derecha:
        cuerpo = "".join(estilo.alerta(t, d, n) for t, d, n in alertas[:4]) or \
            estilo.alerta(t("Todo en orden"), t("No hay alertas activas."), "ok")
        html(estilo.panel_alertas(cuerpo))
        if st.button(t("Ver todas las alertas →"), key="ver_alertas", width="stretch"):
            st.session_state["pagina"] = "Plagas"
            st.rerun()

# ---------------------------------------------------------------- Clima
elif pagina == "Clima":
    pedir_parcela()
    st.header(t("Clima y riesgo agroclimático"))
    st.caption(f"{parcela['nombre']} · {parcela['cultivo']}{t(' · últimos 7 días y pronóstico de 7 (Open-Meteo)')}")
    datos = clima_seguro(parcela)
    if datos:
        resumen = clima.resumen_climatico(datos, parcela["cultivo"])
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            html(estilo.tarjeta(t("Lluvia acumulada"), resumen["precip_total"], "mm", "azul", "gotas"))
        with c2:
            html(estilo.tarjeta(t("Racha seca máxima"), resumen["racha_seca_max"], t("días"), "naranja", "nube"))
        with c3:
            html(estilo.tarjeta(t("Grados-día"), resumen["grados_dia"], "", "verde", "tendencia"))
        with c4:
            html(estilo.tarjeta(t("Días con helada"), len(resumen["heladas"]), "", "morado", "termometro"))
        diario = pd.DataFrame(datos["diario"]).set_index("fecha")
        st.subheader(t("Temperaturas diarias"))
        st.line_chart(diario[["tmax", "tmin"]].rename(columns={"tmax": t("Máxima"), "tmin": t("Mínima")}),
                      color=["#f97316", "#3b82f6"], y_label="°C")
        st.subheader(t("Precipitación diaria"))
        st.bar_chart(diario[["precip"]].rename(columns={"precip": "mm"}), color="#059669")
        if resumen["heladas"]:
            html(estilo.panel(t("Días con riesgo de helada"), "".join(
                estilo.alerta(f"{t('Riesgo ')}{t(h['nivel'])}", f"{h['fecha']}{t(' · mínima ')}{h['tmin']} °C",
                              "alto" if h["nivel"] == "alto" else "medio") for h in resumen["heladas"])))

# ---------------------------------------------------------------- Plagas
elif pagina == "Plagas":
    pedir_parcela()
    st.header(t("Monitoreo de plagas"))
    if parcela["cultivo"] == "papa":
        datos = clima_seguro(parcela)
        if datos:
            c1, c2 = st.columns(2)
            for col, criterio, color in ((c1, "hutton", "naranja"), (c2, "smith", "morado")):
                periodos = plagas.periodos_criticos_rancha(datos["horario"], criterio)
                dias_fav = plagas.dias_favorables_rancha(datos["horario"], criterio)
                with col:
                    html(estilo.tarjeta(f"{t('Rancha · criterio ')}{criterio.title()}", len(periodos), t("periodos"),
                                        color, "plaga", nota=f"{len(dias_fav)}{t(' días favorables')}"))
            st.caption(t("Criterios definidos para el Reino Unido; su calibración al altiplano es parte del estudio."))
    with st.form("monitoreo", clear_on_submit=True):
        st.subheader(t("Registrar evaluación de campo"))
        c1, c2 = st.columns(2)
        nombre_plaga = c1.text_input("Plaga o enfermedad", placeholder=t("rancha, gorgojo de los andes…"))
        fecha = c2.date_input("Fecha", value=date.today())
        evaluadas = c1.number_input("Plantas evaluadas", min_value=1, value=50)
        afectadas = c2.number_input("Plantas afectadas", min_value=0, value=0)
        notas = st.text_input("Notas (opcional)")
        if st.form_submit_button(t("Guardar evaluación")):
            if not nombre_plaga.strip():
                st.error(t("Escribe el nombre de la plaga."))
            else:
                try:
                    plagas.registrar_monitoreo(con, parcela["id"], fecha.isoformat(), nombre_plaga,
                                               int(evaluadas), int(afectadas), notas or None)
                    st.success(f"{t('Guardado: incidencia ')}{plagas.incidencia(int(afectadas), int(evaluadas))} %")
                except ValueError as error:
                    st.error(str(error))
    estado = plagas.alertas_monitoreo(con, parcela["id"])
    if estado:
        html(estilo.panel(t("Estado actual por plaga"), "".join(
            estilo.alerta(f"{a['plaga'].capitalize()}: {a['incidencia']} %",
                          f"{t('umbral ')}{a['umbral']}{t(' % · tendencia ')}{t(a['tendencia'])} · {a['fecha']}",
                          "alto" if a["supera_umbral"] else "ok") for a in estado)))
        historial = pd.DataFrame(plagas.historial(con, parcela["id"]))
        tabla = historial.pivot_table(index="fecha", columns="plaga", values="incidencia", aggfunc="last")
        st.subheader(t("Evolución de la incidencia (%)"))
        st.line_chart(tabla)

# ---------------------------------------------------------------- Mercado
elif pagina == "Mercado":
    st.header(t("Precios de mercado"))
    archivo = None
    if auth.es_admin(usuario_actual):
        archivo = st.file_uploader(t("Importar precios en CSV (fecha, producto, mercado, precio_kg)"), type="csv")
    else:
        st.caption(t("Los precios los carga un administrador a partir de fuentes oficiales."))
    if archivo is not None:
        try:
            texto = archivo.getvalue().decode("utf-8-sig")
            st.success(f"{mercado.importar_texto(con, texto, archivo.name)}{t(' precios importados')}")
        except (UnicodeDecodeError, ValueError) as error:
            st.error(str(error))
    lista = mercado.productos(con)
    if not lista:
        html(estilo.alerta(t("Aún no hay precios"), t("Importa un CSV para ver tendencias."), "info"))
    else:
        c1, c2 = st.columns(2)
        producto = c1.selectbox(t("Producto"), lista)
        lugar = c2.selectbox(t("Mercado"), ["Todos"] + mercado.mercados(con, producto), format_func=t)
        filtro = None if lugar == "Todos" else lugar
        resumen = mercado.resumen_precios(con, producto, filtro)
        datos = mercado.serie(con, producto, filtro)
        t1, t2, t3, t4 = st.columns(4)
        with t1:
            html(estilo.tarjeta(t("Último precio"), f"{resumen['ultimo'][1]:.2f}", "S/ kg", "verde", "tienda",
                                nota=resumen["ultimo"][0]))
        with t2:
            tend = resumen["tendencia_30d_pct"]
            html(estilo.tarjeta(t("Tendencia"), f"{tend:+.1f}" if tend is not None else "–", t("% / 30 días"),
                                "naranja", "tendencia"))
        with t3:
            html(estilo.tarjeta(t("Promedio"), f"{resumen['promedio']:.2f}", "S/ kg", "azul", "gotas",
                                nota=f"n = {resumen['n']}"))
        with t4:
            mes = MESES[resumen["mejor_mes"] - 1] if resumen["mejor_mes"] else "–"
            html(estilo.tarjeta(t("Mejor mes para vender"), mes, "", "morado", "hoja"))
        col_precio, col_media = t("Precio"), t("Media móvil (3)")
        tabla = pd.DataFrame(datos, columns=["fecha", col_precio]).set_index("fecha")
        tabla[col_media] = mercado.media_movil(tabla[col_precio].tolist(), 3)
        st.subheader(t("Evolución del precio (S/ por kg)"))
        st.line_chart(tabla, color=["#059669", "#f97316"])
        mensual = mercado.promedio_mensual(datos)
        st.subheader(t("Precio promedio por mes"))
        st.bar_chart(pd.DataFrame({"S/ kg": list(mensual.values())},
                                  index=[f"{m:02d}-{MESES[m - 1]}" for m in mensual]), color="#3b82f6")

    st.subheader(t("Rentabilidad de la campaña"))
    c1, c2, c3 = st.columns(3)
    rendimiento = c1.number_input("Cosecha esperada (kg)", min_value=1.0, value=10000.0, step=100.0)
    precio = c2.number_input("Precio de venta (S/ por kg)", min_value=0.0, value=1.5, step=0.1)
    costos = c3.number_input("Costos totales (S/)", min_value=0.0, value=9000.0, step=100.0)
    r = mercado.margen(rendimiento, precio, costos)
    m1, m2, m3 = st.columns(3)
    with m1:
        html(estilo.tarjeta(t("Ingreso"), f"{r['ingreso']:,.0f}", "S/", "azul", "tienda"))
    with m2:
        html(estilo.tarjeta(t("Margen"), f"{r['margen']:,.0f}", "S/", "verde" if r["margen"] >= 0 else "naranja",
                            "tendencia", nota=f"{r['margen_pct']} %" if r["margen_pct"] is not None else None))
    with m3:
        html(estilo.tarjeta(t("Precio de equilibrio"), f"{r['precio_equilibrio_kg']:.2f}", "S/ kg", "morado", "hoja"))

# ---------------------------------------------------------------- Ofertas
elif pagina == "Ofertas":
    st.header(t("Ofertas de venta directa"))
    with st.form("oferta", clear_on_submit=True):
        c1, c2 = st.columns(2)
        productor = c1.text_input("Productor")
        producto = c2.text_input("Producto")
        cantidad = c1.number_input("Cantidad (kg)", min_value=1.0, value=100.0)
        precio = c2.number_input("Precio (S/ por kg)", min_value=0.0, value=2.0)
        contacto = c1.text_input("Contacto (teléfono)")
        lugar = c2.text_input("Lugar")
        if st.form_submit_button(t("Publicar oferta")):
            if productor.strip() and producto.strip():
                mercado.publicar_oferta(con, productor.strip(), producto, cantidad, precio,
                                        contacto or None, lugar or None, usuario_id=usuario_actual["id"])
                st.success(t("Oferta publicada"))
            else:
                st.error(t("Productor y producto son obligatorios."))
    ofertas = mercado.listar_ofertas(con)
    if not ofertas:
        html(estilo.alerta(t("No hay ofertas activas"), t("Publica la primera con el formulario."), "info"))
    columnas = st.columns(3)
    for i, oferta in enumerate(ofertas):
        with columnas[i % 3]:
            html(estilo.tarjeta_oferta(oferta))
            if oferta.get("usuario_id") == usuario_actual["id"] and \
                    st.button(t("Marcar como vendida"), key=f"cerrar_{oferta['id']}"):
                mercado.cerrar_oferta(con, oferta["id"], usuario_actual["id"])
                st.rerun()

# ---------------------------------------------------------------- Parcelas
elif pagina == "Parcelas":
    st.header("Parcelas")
    with st.form("parcela", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nombre = c1.text_input("Nombre de la parcela")
        cultivo = c2.selectbox(t("Cultivo"), sorted(CULTIVOS))
        lat = c1.number_input("Latitud", value=-15.8402, format="%.4f", min_value=-90.0, max_value=90.0)
        lon = c2.number_input("Longitud", value=-70.0219, format="%.4f", min_value=-180.0, max_value=180.0)
        area = c1.number_input("Área (ha)", min_value=0.01, value=1.0)
        siembra = c2.date_input("Fecha de siembra", value=None)
        if st.form_submit_button(t("Registrar parcela")):
            if nombre.strip():
                db.agregar_parcela(con, nombre.strip(), cultivo, lat, lon, area,
                                   siembra.isoformat() if siembra else None, usuario_actual["id"])
                st.success(t("Parcela registrada"))
                st.rerun()
            else:
                st.error(t("El nombre es obligatorio."))
    if parcelas:
        st.dataframe(pd.DataFrame(parcelas).drop(columns=["id", "usuario_id"]), width="stretch", hide_index=True)
