"""Monitoreo de plagas: riesgo climático de rancha y registros de campo."""
from collections import defaultdict
from datetime import date, timedelta

from .config import CRITERIOS_RANCHA, umbral_plaga


def _resumen_por_dia(horario, hr_min):
    """Por día completo (24 h): temperatura mínima y horas con HR >= hr_min."""
    dias = defaultdict(list)
    for registro in horario:
        if registro["temp"] is None or registro["hr"] is None:
            continue
        dias[registro["hora"][:10]].append(registro)
    resumen = {}
    for fecha, registros in dias.items():
        if len(registros) < 24:
            continue  # día incompleto: no se evalúa
        resumen[fecha] = {
            "tmin": min(r["temp"] for r in registros),
            "horas_humedas": sum(1 for r in registros if r["hr"] >= hr_min),
        }
    return resumen


def dias_favorables_rancha(horario, criterio="hutton"):
    """Fechas que cumplen por sí solas el criterio (Tmin y horas húmedas)."""
    c = CRITERIOS_RANCHA[criterio]
    resumen = _resumen_por_dia(horario, c["hr_min"])
    return sorted(
        fecha for fecha, r in resumen.items()
        if r["tmin"] >= c["temp_min"] and r["horas_humedas"] >= c["horas_min"]
    )


def periodos_criticos_rancha(horario, criterio="hutton"):
    """Fechas en que se completa un periodo crítico (2 días favorables seguidos)."""
    favorables = dias_favorables_rancha(horario, criterio)
    conjunto = set(favorables)
    periodos = []
    for fecha in favorables:
        anterior = (date.fromisoformat(fecha) - timedelta(days=1)).isoformat()
        if anterior in conjunto:
            periodos.append(fecha)
    return periodos


def incidencia(plantas_afectadas, plantas_evaluadas):
    if plantas_evaluadas <= 0:
        raise ValueError("plantas_evaluadas debe ser mayor que 0")
    if not 0 <= plantas_afectadas <= plantas_evaluadas:
        raise ValueError("plantas_afectadas debe estar entre 0 y plantas_evaluadas")
    return round(100.0 * plantas_afectadas / plantas_evaluadas, 1)


def registrar_monitoreo(con, parcela_id, fecha, plaga, plantas_evaluadas, plantas_afectadas, notas=None):
    incidencia(plantas_afectadas, plantas_evaluadas)  # valida antes de insertar
    cur = con.execute(
        "INSERT INTO monitoreos_plaga (parcela_id, fecha, plaga, plantas_evaluadas, "
        "plantas_afectadas, notas) VALUES (?, ?, ?, ?, ?, ?)",
        (parcela_id, fecha, plaga.strip().lower(), plantas_evaluadas, plantas_afectadas, notas),
    )
    con.commit()
    return cur.lastrowid


def historial(con, parcela_id, plaga=None):
    sql = "SELECT * FROM monitoreos_plaga WHERE parcela_id = ?"
    args = [parcela_id]
    if plaga:
        sql += " AND plaga = ?"
        args.append(plaga.strip().lower())
    filas = con.execute(sql + " ORDER BY fecha, id", args).fetchall()
    return [dict(f, incidencia=incidencia(f["plantas_afectadas"], f["plantas_evaluadas"])) for f in filas]


def alertas_monitoreo(con, parcela_id=None):
    """Último registro por parcela y plaga, comparado con su umbral y con el registro previo."""
    sql = "SELECT DISTINCT parcela_id, plaga FROM monitoreos_plaga"
    args = []
    if parcela_id is not None:
        sql += " WHERE parcela_id = ?"
        args.append(parcela_id)
    alertas = []
    for fila in con.execute(sql, args).fetchall():
        registros = historial(con, fila["parcela_id"], fila["plaga"])
        ultimo = registros[-1]
        previo = registros[-2]["incidencia"] if len(registros) > 1 else None
        umbral = umbral_plaga(fila["plaga"])
        if previo is None or ultimo["incidencia"] == previo:
            tendencia = "estable"
        else:
            tendencia = "sube" if ultimo["incidencia"] > previo else "baja"
        alertas.append({
            "parcela_id": fila["parcela_id"],
            "plaga": fila["plaga"],
            "fecha": ultimo["fecha"],
            "incidencia": ultimo["incidencia"],
            "umbral": umbral,
            "supera_umbral": ultimo["incidencia"] >= umbral,
            "tendencia": tendencia,
        })
    return sorted(alertas, key=lambda a: (not a["supera_umbral"], -a["incidencia"]))
