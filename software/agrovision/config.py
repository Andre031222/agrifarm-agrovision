"""Parámetros agronómicos configurables.

IMPORTANTE: todos los valores numéricos de este archivo son valores iniciales
de trabajo. Deben validarse con un agrónomo y con bibliografía antes de usarse
en el artículo; cualquier valor que se reporte debe citar su fuente.
"""

# Temperatura base para grados-día (°C) y umbral de helada crítica (°C).
CULTIVOS = {
    "papa":   {"temp_base": 7.0,  "helada_critica": -2.0},
    "quinua": {"temp_base": 3.0,  "helada_critica": -4.0},
    "maiz":   {"temp_base": 10.0, "helada_critica": -1.0},
    "haba":   {"temp_base": 0.0,  "helada_critica": -3.0},
}

# Incidencia (% de plantas afectadas) a partir de la cual se recomienda actuar.
UMBRALES_PLAGA = {
    "rancha": 5.0,
    "gorgojo de los andes": 10.0,
    "polilla de la quinua": 10.0,
}
UMBRAL_PLAGA_POR_DEFECTO = 10.0

# Criterios de periodo crítico para rancha (Phytophthora infestans).
# Hutton: 2 días consecutivos con Tmin >= 10 °C y >= 6 h con HR >= 90 %.
# Smith:  igual, pero >= 11 h con HR >= 90 %.
# Ambos se definieron para el Reino Unido; su ajuste al altiplano es parte
# de la pregunta de investigación del proyecto.
CRITERIOS_RANCHA = {
    "hutton": {"temp_min": 10.0, "hr_min": 90.0, "horas_min": 6},
    "smith":  {"temp_min": 10.0, "hr_min": 90.0, "horas_min": 11},
}

ZONA_HORARIA = "America/Lima"


def parametros_cultivo(cultivo):
    clave = cultivo.strip().lower()
    if clave not in CULTIVOS:
        raise ValueError(f"Cultivo no configurado: {cultivo!r}. Opciones: {', '.join(CULTIVOS)}")
    return CULTIVOS[clave]


def umbral_plaga(plaga):
    return UMBRALES_PLAGA.get(plaga.strip().lower(), UMBRAL_PLAGA_POR_DEFECTO)
