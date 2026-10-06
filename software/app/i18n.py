"""Traducción de la interfaz. Las claves son los textos en español.

Para agregar quechua o aymara, añadir un diccionario en IDIOMAS con traducciones
revisadas por hablantes nativos; los textos que falten se muestran en español.
"""

EN = {
    # Navegación y sesión
    "Inicio": "Home", "Clima": "Weather", "Plagas": "Pests", "Mercado": "Market", "Ofertas": "Offers",
    "Parcelas": "Plots", "Todos": "All", "Menú Principal": "Main menu", "NAVEGACIÓN": "NAVIGATION", "Panel": "Panel",
    "Iniciar sesión": "Sign in", "Crear cuenta": "Create account", "Empieza gratis →": "Start for free →",
    "¡Bienvenido a ": "Welcome to ", "Cerrar sesión": "Sign out", "← Volver al inicio": "← Back to home",
    "Sistema inteligente": "Smart system", "Parcela activa": "Active plot", "productor": "farmer",
    "admin": "administrator", "Idioma": "Language",
    "Aún no hay parcelas. Regístralas en «Parcelas».": "No plots yet. Add them under “Plots”.",
    # Inicio
    "Hola, ": "Hello, ", "Tu panel de monitoreo climático, de plagas y de mercado":
        "Your weather, pest and market monitoring panel",
    "SISTEMA ACTIVO · EN LÍNEA": "SYSTEM ACTIVE · ONLINE", "Hora actual": "Current time",
    "Parcelas registradas": "Registered plots", "Mínima de hoy": "Today's minimum",
    "Humedad relativa": "Relative humidity", "Ofertas activas": "Active offers",
    "Alertas recientes": "Recent alerts", "Ver todas las alertas →": "See all alerts →",
    "Todo en orden": "All clear", "No hay alertas activas.": "No active alerts.",
    "Humedad": "Humidity", "Lluvia hoy": "Rain today", "Mínima hoy": "Min today",
    "Sin datos de clima por ahora": "No weather data yet", "Revisa la conexión a internet.": "Check your internet connection.",
    "Registra tu primera parcela": "Register your first plot", "Ve a «Parcelas» en el menú.": "Go to “Plots” in the menu.",
    "Primero registra una parcela": "Register a plot first",
    "Ve a la sección «Parcelas» del menú.": "Open the “Plots” section of the menu.",
    "No se pudo consultar Open-Meteo: ": "Could not reach Open-Meteo: ",
    "Riesgo alto de helada": "High frost risk", "Riesgo moderado de helada": "Moderate frost risk",
    "Periodo crítico de rancha (Hutton)": "Late-blight critical period (Hutton)", "sobre el umbral": "above threshold",
    # Clima
    "Clima y riesgo agroclimático": "Weather and agro-climatic risk",
    " · últimos 7 días y pronóstico de 7 (Open-Meteo)": " · last 7 days and 7-day forecast (Open-Meteo)",
    "Lluvia acumulada": "Accumulated rain", "Racha seca máxima": "Longest dry spell", "días": "days",
    "Grados-día": "Degree-days", "Días con helada": "Frost days", "Temperaturas diarias": "Daily temperatures",
    "Máxima": "Maximum", "Mínima": "Minimum", "Precipitación diaria": "Daily precipitation",
    "Días con riesgo de helada": "Days with frost risk", "Riesgo ": "Risk ", "alto": "high", "moderado": "moderate",
    " · mínima ": " · minimum ",
    # Plagas
    "Monitoreo de plagas": "Pest monitoring", "Rancha · criterio ": "Late blight · criterion ", "periodos": "periods",
    " días favorables": " favourable days",
    "Criterios definidos para el Reino Unido; su calibración al altiplano es parte del estudio.":
        "Criteria defined for the United Kingdom; their calibration to the altiplano is part of the study.",
    "Registrar evaluación de campo": "Record field evaluation", "Plaga o enfermedad": "Pest or disease",
    "rancha, gorgojo de los andes…": "late blight, Andean weevil…", "Fecha": "Date",
    "Plantas evaluadas": "Plants evaluated", "Plantas afectadas": "Plants affected", "Notas (opcional)": "Notes (optional)",
    "Guardar evaluación": "Save evaluation", "Escribe el nombre de la plaga.": "Enter the pest name.",
    "Guardado: incidencia ": "Saved: incidence ", "Estado actual por plaga": "Current status by pest",
    "umbral ": "threshold ", " % · tendencia ": " % · trend ", "sube": "rising", "baja": "falling", "estable": "stable",
    "Evolución de la incidencia (%)": "Incidence over time (%)",
    # Mercado
    "Precios de mercado": "Market prices",
    "Importar precios en CSV (fecha, producto, mercado, precio_kg)": "Import prices from CSV (date, product, market, price_kg)",
    "Los precios los carga un administrador a partir de fuentes oficiales.":
        "Prices are loaded by an administrator from official sources.",
    " precios importados": " prices imported", "Aún no hay precios": "No prices yet",
    "Importa un CSV para ver tendencias.": "Import a CSV to see trends.", "Producto": "Product",
    "Último precio": "Latest price", "Tendencia": "Trend", "% / 30 días": "% / 30 days", "Promedio": "Average",
    "Mejor mes para vender": "Best month to sell", "Evolución del precio (S/ por kg)": "Price over time (S/ per kg)",
    "Precio promedio por mes": "Average price by month", "Media móvil (3)": "Moving average (3)", "Precio": "Price",
    "Rentabilidad de la campaña": "Season profitability", "Cosecha esperada (kg)": "Expected harvest (kg)",
    "Precio de venta (S/ por kg)": "Selling price (S/ per kg)", "Costos totales (S/)": "Total costs (S/)",
    "Ingreso": "Revenue", "Margen": "Margin", "Precio de equilibrio": "Break-even price",
    # Ofertas
    "Ofertas de venta directa": "Direct-sale offers", "Productor": "Farmer", "Cantidad (kg)": "Quantity (kg)",
    "Precio (S/ por kg)": "Price (S/ per kg)", "Contacto (teléfono)": "Contact (phone)", "Lugar": "Place",
    "Publicar oferta": "Publish offer", "Oferta publicada": "Offer published",
    "Productor y producto son obligatorios.": "Farmer and product are required.",
    "No hay ofertas activas": "No active offers", "Publica la primera con el formulario.": "Publish the first one with the form.",
    "Marcar como vendida": "Mark as sold", "por kg": "per kg", "kg disponibles": "kg available",
    "Sin contacto": "No contact", "publicado": "published",
    # Parcelas
    "Nombre de la parcela": "Plot name", "Cultivo": "Crop", "Latitud": "Latitude", "Longitud": "Longitude",
    "Área (ha)": "Area (ha)", "Fecha de siembra": "Sowing date", "Registrar parcela": "Register plot",
    "Parcela registrada": "Plot registered", "El nombre es obligatorio.": "The name is required.",
    # Acceso
    "Usuario": "Username", "Contraseña": "Password", "Iniciar sesión →": "Sign in →",
    "Usuario o contraseña incorrectos.": "Wrong username or password.", "Nombre completo": "Full name",
    "3 a 32 caracteres: letras, números, punto o guion": "3 to 32 characters: letters, numbers, dot or hyphen",
    "Mínimo 8 caracteres": "At least 8 characters", "Repite la contraseña": "Repeat the password",
    "Las contraseñas no coinciden.": "Passwords do not match.",
    "Cuenta creada. Ya puedes iniciar sesión.": "Account created. You can sign in now.",
    "¡Bienvenido de vuelta!": "Welcome back!", "Inicia sesión para continuar con tu parcela": "Sign in to continue with your plot",
    # Landing y panel de acceso
    "PLATAFORMA ABIERTA · ALTIPLANO DE PUNO": "OPEN PLATFORM · PUNO ALTIPLANO",
    "Clima, plagas y mercado en una sola plataforma": "Weather, pests and market in one platform",
    "Alertas de helada y de rancha, registro de plagas en campo y precios para decidir cuándo vender. Gratis y de código abierto.":
        "Frost and late-blight alerts, field pest records and prices to decide when to sell. Free and open source.",
    "días de clima": "days of weather", "cultivos andinos": "Andean crops", "criterios de rancha": "late-blight criteria",
    "Gratis": "Free", "y abierto": "and open", "SERVICIOS": "SERVICES",
    "Todo lo que necesitas para tu parcela": "Everything you need for your plot",
    "Riesgo climático": "Climate risk", "Alertas de plagas": "Pest alerts", "Precios de mercado ": "Market prices",
    "Venta directa": "Direct sales",
    "Heladas por cultivo, rachas secas y grados-día con datos abiertos de Open-Meteo.":
        "Frost by crop, dry spells and degree-days from open Open-Meteo data.",
    "Periodos críticos de rancha y evaluaciones de campo con umbral de acción.":
        "Late-blight critical periods and field evaluations with action thresholds.",
    "Tendencia, estacionalidad, mejor mes de venta y precio de equilibrio.":
        "Trend, seasonality, best selling month and break-even price.",
    "Publica tu cosecha y conecta con compradores sin intermediarios.":
        "Publish your harvest and reach buyers without middlemen.",
    "CÓMO FUNCIONA": "HOW IT WORKS", "Empieza en tres pasos": "Start in three steps",
    "Crea tu cuenta": "Create your account", "Regístrate gratis con tu usuario y contraseña.": "Sign up for free with a username and password.",
    "Registra tus parcelas": "Register your plots", "Indica el cultivo y la ubicación de cada parcela.": "Enter the crop and location of each plot.",
    "Recibe alertas": "Get alerts", "Revisa el clima, las plagas y los precios cada día.": "Check weather, pests and prices every day.",
    "ACERCA DE": "ABOUT", "Nacido en las aulas de la UNAP": "Born in the classrooms of UNAP",
    "El proyecto empezó en 2025 en los cursos de Ingeniería de Software y Taller de Desarrollo de Software de la Universidad Nacional del Altiplano, como Green Modern Agrifarm y luego AgroVision 360. Esta versión la desarrolla el equipo original:":
        "The project began in 2025 in the Software Engineering and Software Development Workshop courses at the Universidad Nacional del Altiplano, as Green Modern Agrifarm and then AgroVision 360. This version is developed by the original team:",
    "Escuela Profesional de Ingeniería Estadística e Informática · UNAP, Puno":
        "School of Statistical and Informatics Engineering · UNAP, Puno",
    "Contacto": "Contact", "Licencia": "Licence", "MIT · código abierto": "MIT · open source",
    "Agricultura Inteligente": "Smart Agriculture",
    "Monitorea el clima, las plagas y el mercado de tu parcela en el altiplano":
        "Monitor the weather, pests and market of your plot in the altiplano",
    "Cultivos": "Crops", "Días de clima": "Days of weather", "Código abierto": "Open source",
}

IDIOMAS = {"es": None, "en": EN}
NOMBRES = {"es": "Español", "en": "English"}
MESES = {"es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "set", "oct", "nov", "dic"],
         "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
DIAS = {"es": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
        "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

idioma = "es"


def t(texto):
    """Traduce un texto de la interfaz al idioma activo (si no hay traducción, lo deja en español)."""
    tabla = IDIOMAS.get(idioma)
    return tabla.get(texto, texto) if tabla else texto
