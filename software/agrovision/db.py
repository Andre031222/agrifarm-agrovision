"""Persistencia en SQLite (un solo archivo, sin servidor)."""
import os
import sqlite3

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id      INTEGER PRIMARY KEY,
    usuario TEXT NOT NULL UNIQUE,
    nombre  TEXT NOT NULL,
    sal     TEXT NOT NULL,
    hash    TEXT NOT NULL,
    rol     TEXT NOT NULL DEFAULT 'productor' CHECK (rol IN ('productor', 'admin')),
    creado  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS parcelas (
    id            INTEGER PRIMARY KEY,
    nombre        TEXT NOT NULL,
    cultivo       TEXT NOT NULL,
    latitud       REAL NOT NULL CHECK (latitud BETWEEN -90 AND 90),
    longitud      REAL NOT NULL CHECK (longitud BETWEEN -180 AND 180),
    area_ha       REAL CHECK (area_ha IS NULL OR area_ha > 0),
    fecha_siembra TEXT,
    usuario_id    INTEGER REFERENCES usuarios(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS monitoreos_plaga (
    id                INTEGER PRIMARY KEY,
    parcela_id        INTEGER NOT NULL REFERENCES parcelas(id) ON DELETE CASCADE,
    fecha             TEXT NOT NULL,
    plaga             TEXT NOT NULL,
    plantas_evaluadas INTEGER NOT NULL CHECK (plantas_evaluadas > 0),
    plantas_afectadas INTEGER NOT NULL CHECK (plantas_afectadas >= 0),
    notas             TEXT,
    CHECK (plantas_afectadas <= plantas_evaluadas)
);
CREATE TABLE IF NOT EXISTS precios (
    id        INTEGER PRIMARY KEY,
    fecha     TEXT NOT NULL,
    producto  TEXT NOT NULL,
    mercado   TEXT NOT NULL,
    precio_kg REAL NOT NULL CHECK (precio_kg >= 0),
    fuente    TEXT,
    UNIQUE (fecha, producto, mercado)
);
CREATE TABLE IF NOT EXISTS ofertas (
    id          INTEGER PRIMARY KEY,
    fecha       TEXT NOT NULL,
    productor   TEXT NOT NULL,
    producto    TEXT NOT NULL,
    cantidad_kg REAL NOT NULL CHECK (cantidad_kg > 0),
    precio_kg   REAL NOT NULL CHECK (precio_kg >= 0),
    contacto    TEXT,
    lugar       TEXT,
    activa      INTEGER NOT NULL DEFAULT 1,
    usuario_id  INTEGER REFERENCES usuarios(id) ON DELETE CASCADE
);
"""


def conectar(ruta=None):
    """Abre (y si hace falta crea) la base. Usa AGROVISION_DB o 'agrovision.db'."""
    ruta = ruta or os.environ.get("AGROVISION_DB", "agrovision.db")
    con = sqlite3.connect(ruta, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(ESQUEMA)
    _migrar(con)
    return con


def _migrar(con):
    """Agrega columnas nuevas a bases creadas con versiones anteriores."""
    columnas_usuarios = {f["name"] for f in con.execute("PRAGMA table_info(usuarios)")}
    if "rol" not in columnas_usuarios:
        con.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT NOT NULL DEFAULT 'productor'")
        con.commit()
    for tabla in ("parcelas", "ofertas"):
        columnas = {f["name"] for f in con.execute(f"PRAGMA table_info({tabla})")}
        if "usuario_id" not in columnas:
            con.execute(f"ALTER TABLE {tabla} ADD COLUMN usuario_id INTEGER REFERENCES usuarios(id)")
            con.commit()


def agregar_parcela(con, nombre, cultivo, latitud, longitud, area_ha=None, fecha_siembra=None, usuario_id=None):
    from .config import parametros_cultivo
    parametros_cultivo(cultivo)  # valida que el cultivo exista
    cur = con.execute(
        "INSERT INTO parcelas (nombre, cultivo, latitud, longitud, area_ha, fecha_siembra, usuario_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nombre, cultivo.lower(), latitud, longitud, area_ha, fecha_siembra, usuario_id),
    )
    con.commit()
    return cur.lastrowid


def listar_parcelas(con, usuario_id=None):
    """Todas las parcelas, o solo las del usuario indicado."""
    if usuario_id is None:
        filas = con.execute("SELECT * FROM parcelas ORDER BY id")
    else:
        filas = con.execute("SELECT * FROM parcelas WHERE usuario_id = ? ORDER BY id", (usuario_id,))
    return [dict(f) for f in filas]


def obtener_parcela(con, parcela_id):
    fila = con.execute("SELECT * FROM parcelas WHERE id = ?", (parcela_id,)).fetchone()
    if fila is None:
        raise ValueError(f"No existe la parcela {parcela_id}")
    return dict(fila)
