"""Mercado: precios, tendencias, rentabilidad y ofertas de venta directa."""
import csv
from collections import defaultdict
from datetime import date

COLUMNAS_PRECIOS = ("fecha", "producto", "mercado", "precio_kg")


def importar_csv(con, ruta, fuente=None):
    """Importa precios desde un archivo CSV (ver importar_texto)."""
    with open(ruta, encoding="utf-8-sig") as archivo:
        return importar_texto(con, archivo.read(), fuente)


def importar_texto(con, texto, fuente=None):
    """Importa precios (fecha,producto,mercado,precio_kg). Ignora líneas que empiezan con '#'."""
    lineas = [l for l in texto.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    lector = csv.DictReader(lineas)
    faltantes = set(COLUMNAS_PRECIOS) - set(lector.fieldnames or [])
    if faltantes:
        raise ValueError(f"Faltan columnas: {', '.join(sorted(faltantes))}")
    filas = []
    for n, fila in enumerate(lector, start=2):
        try:
            fecha = date.fromisoformat(fila["fecha"].strip()).isoformat()
            precio = float(fila["precio_kg"])
        except ValueError as error:
            raise ValueError(f"Fila {n} inválida: {error}") from None
        if precio < 0:
            raise ValueError(f"Fila {n}: precio negativo")
        filas.append((fecha, fila["producto"].strip().lower(), fila["mercado"].strip(), precio, fuente))
    con.executemany(
        "INSERT OR REPLACE INTO precios (fecha, producto, mercado, precio_kg, fuente) VALUES (?, ?, ?, ?, ?)",
        filas,
    )
    con.commit()
    return len(filas)


def productos(con):
    return [f[0] for f in con.execute("SELECT DISTINCT producto FROM precios ORDER BY producto")]


def mercados(con, producto=None):
    sql, args = "SELECT DISTINCT mercado FROM precios", []
    if producto:
        sql, args = sql + " WHERE producto = ?", [producto.lower()]
    return [f[0] for f in con.execute(sql + " ORDER BY mercado", args)]


def serie(con, producto, mercado=None):
    """[(fecha, precio)] ordenada; sin mercado, promedia los mercados de cada fecha."""
    sql = "SELECT fecha, AVG(precio_kg) FROM precios WHERE producto = ?"
    args = [producto.lower()]
    if mercado:
        sql += " AND mercado = ?"
        args.append(mercado)
    return [(f, round(p, 2)) for f, p in con.execute(sql + " GROUP BY fecha ORDER BY fecha", args)]


def media_movil(valores, ventana=3):
    if ventana < 1:
        raise ValueError("ventana debe ser >= 1")
    return [
        round(sum(valores[i - ventana + 1:i + 1]) / ventana, 2) if i >= ventana - 1 else None
        for i in range(len(valores))
    ]


def tendencia(datos):
    """Pendiente por mínimos cuadrados expresada como % de cambio cada 30 días."""
    if len(datos) < 2:
        return None
    x = [date.fromisoformat(f).toordinal() for f, _ in datos]
    y = [p for _, p in datos]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxx = sum((xi - mx) ** 2 for xi in x)
    if sxx == 0 or my == 0:
        return None
    pendiente = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sxx
    return round(100 * pendiente * 30 / my, 1) + 0.0  # evita -0.0


def promedio_mensual(datos):
    """{mes (1-12): precio promedio} sobre todos los años disponibles."""
    por_mes = defaultdict(list)
    for fecha, precio in datos:
        por_mes[int(fecha[5:7])].append(precio)
    return {mes: round(sum(v) / len(v), 2) for mes, v in sorted(por_mes.items())}


def mejor_mes_venta(datos):
    meses = promedio_mensual(datos)
    return max(meses, key=meses.get) if meses else None


def resumen_precios(con, producto, mercado=None):
    datos = serie(con, producto, mercado)
    if not datos:
        return None
    precios = [p for _, p in datos]
    return {
        "ultimo": datos[-1],
        "minimo": min(precios),
        "maximo": max(precios),
        "promedio": round(sum(precios) / len(precios), 2),
        "tendencia_30d_pct": tendencia(datos),
        "mejor_mes": mejor_mes_venta(datos),
        "n": len(datos),
    }


def margen(rendimiento_kg, precio_kg, costos):
    """Ingreso, margen y precio de equilibrio de una campaña."""
    if rendimiento_kg <= 0:
        raise ValueError("rendimiento_kg debe ser mayor que 0")
    ingreso = rendimiento_kg * precio_kg
    utilidad = ingreso - costos
    return {
        "ingreso": round(ingreso, 2),
        "costos": round(costos, 2),
        "margen": round(utilidad, 2),
        "margen_pct": round(100 * utilidad / ingreso, 1) if ingreso else None,
        "precio_equilibrio_kg": round(costos / rendimiento_kg, 2),
    }


def publicar_oferta(con, productor, producto, cantidad_kg, precio_kg, contacto=None, lugar=None, fecha=None):
    cur = con.execute(
        "INSERT INTO ofertas (fecha, productor, producto, cantidad_kg, precio_kg, contacto, lugar) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (fecha or date.today().isoformat(), productor, producto.strip().lower(),
         cantidad_kg, precio_kg, contacto, lugar),
    )
    con.commit()
    return cur.lastrowid


def listar_ofertas(con, producto=None, solo_activas=True):
    sql, args = "SELECT * FROM ofertas WHERE 1 = 1", []
    if solo_activas:
        sql += " AND activa = 1"
    if producto:
        sql += " AND producto = ?"
        args.append(producto.strip().lower())
    return [dict(f) for f in con.execute(sql + " ORDER BY fecha DESC, id DESC", args)]


def cerrar_oferta(con, oferta_id):
    cur = con.execute("UPDATE ofertas SET activa = 0 WHERE id = ?", (oferta_id,))
    con.commit()
    if cur.rowcount == 0:
        raise ValueError(f"No existe la oferta {oferta_id}")
