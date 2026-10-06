"""Clima: descarga de Open-Meteo (sin API key) e indicadores agroclimáticos."""
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from .config import ZONA_HORARIA, parametros_cultivo

URL_PRONOSTICO = "https://api.open-meteo.com/v1/forecast"


def obtener_clima(latitud, longitud, dias_pasados=7, dias_pronostico=7, timeout=20):
    """Devuelve {'horario': [...], 'diario': [...]} para el punto dado."""
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": ZONA_HORARIA,
        "past_days": dias_pasados,
        "forecast_days": dias_pronostico,
    }
    with urlopen(f"{URL_PRONOSTICO}?{urlencode(parametros)}", timeout=timeout) as respuesta:
        return normalizar(json.load(respuesta))


def normalizar(datos):
    """Convierte la respuesta de Open-Meteo en listas de registros."""
    h, d = datos["hourly"], datos["daily"]
    horario = [
        {"hora": t, "temp": temp, "hr": hr, "precip": p}
        for t, temp, hr, p in zip(h["time"], h["temperature_2m"],
                                  h["relative_humidity_2m"], h["precipitation"])
    ]
    diario = [
        {"fecha": f, "tmax": tmax, "tmin": tmin, "precip": p}
        for f, tmax, tmin, p in zip(d["time"], d["temperature_2m_max"],
                                    d["temperature_2m_min"], d["precipitation_sum"])
    ]
    return {"horario": horario, "diario": diario}


def riesgo_helada(diario, helada_critica, margen=2.0):
    """Días con helada: 'alto' si Tmin <= umbral, 'moderado' si está a menos de `margen` °C."""
    alertas = []
    for dia in diario:
        tmin = dia["tmin"]
        if tmin is None:
            continue
        if tmin <= helada_critica:
            alertas.append({"fecha": dia["fecha"], "tmin": tmin, "nivel": "alto"})
        elif tmin <= helada_critica + margen:
            alertas.append({"fecha": dia["fecha"], "tmin": tmin, "nivel": "moderado"})
    return alertas


def racha_seca_maxima(diario, umbral_mm=1.0):
    """Mayor número de días consecutivos con precipitación < umbral_mm."""
    maxima = actual = 0
    for dia in diario:
        if dia["precip"] is not None and dia["precip"] < umbral_mm:
            actual += 1
            maxima = max(maxima, actual)
        else:
            actual = 0
    return maxima


def grados_dia(diario, temp_base):
    """Suma de grados-día (método del promedio, sin umbral superior)."""
    total = 0.0
    for dia in diario:
        if dia["tmax"] is None or dia["tmin"] is None:
            continue
        total += max(0.0, (dia["tmax"] + dia["tmin"]) / 2 - temp_base)
    return round(total, 1)


def condicion_actual(clima, hora_iso):
    """Registro horario de la hora dada ('AAAA-MM-DDTHH:..') y el diario de ese día."""
    hora = hora_iso[:13]
    actual = next((h for h in clima["horario"] if h["hora"][:13] == hora), None)
    dia = next((d for d in clima["diario"] if d["fecha"] == hora[:10]), None)
    return actual, dia


def resumen_climatico(clima, cultivo):
    parametros = parametros_cultivo(cultivo)
    diario = clima["diario"]
    return {
        "heladas": riesgo_helada(diario, parametros["helada_critica"]),
        "racha_seca_max": racha_seca_maxima(diario),
        "grados_dia": grados_dia(diario, parametros["temp_base"]),
        "precip_total": round(sum(d["precip"] or 0 for d in diario), 1),
    }
