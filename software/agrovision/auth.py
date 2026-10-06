"""Usuarios: contraseñas con PBKDF2-SHA256 y sal aleatoria (biblioteca estándar)."""
import hashlib
import hmac
import re
import secrets
import sqlite3

ITERACIONES = 200_000
ROLES = ("productor", "admin")
_PATRON_USUARIO = re.compile(r"^[a-z0-9._-]{3,32}$")


def _hash(password, sal):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sal, ITERACIONES).hex()


def crear_usuario(con, usuario, password, nombre, rol="productor"):
    usuario = usuario.strip().lower()
    if not _PATRON_USUARIO.match(usuario):
        raise ValueError("El usuario debe tener 3-32 caracteres: letras, números, punto, guion o guion bajo")
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    if not nombre.strip():
        raise ValueError("El nombre es obligatorio")
    if rol not in ROLES:
        raise ValueError(f"Rol no válido: {rol!r}")
    sal = secrets.token_bytes(16)
    try:
        cur = con.execute("INSERT INTO usuarios (usuario, nombre, sal, hash, rol) VALUES (?, ?, ?, ?, ?)",
                          (usuario, nombre.strip(), sal.hex(), _hash(password, sal), rol))
    except sqlite3.IntegrityError:
        raise ValueError(f"El usuario {usuario!r} ya existe") from None
    con.commit()
    return cur.lastrowid


def verificar(con, usuario, password):
    """Devuelve {'id', 'usuario', 'nombre', 'rol'} si las credenciales son válidas; si no, None."""
    fila = con.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario.strip().lower(),)).fetchone()
    if fila is None:
        _hash(password, b"\0" * 16)  # mismo costo de tiempo que un usuario existente
        return None
    if not hmac.compare_digest(fila["hash"], _hash(password, bytes.fromhex(fila["sal"]))):
        return None
    return {"id": fila["id"], "usuario": fila["usuario"], "nombre": fila["nombre"], "rol": fila["rol"]}


def cambiar_rol(con, usuario, rol):
    if rol not in ROLES:
        raise ValueError(f"Rol no válido: {rol!r}")
    cur = con.execute("UPDATE usuarios SET rol = ? WHERE usuario = ?", (rol, usuario.strip().lower()))
    con.commit()
    if cur.rowcount == 0:
        raise ValueError(f"No existe el usuario {usuario!r}")


def es_admin(usuario):
    return bool(usuario) and usuario.get("rol") == "admin"


def cambiar_password(con, usuario_id, nueva):
    if len(nueva) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    sal = secrets.token_bytes(16)
    con.execute("UPDATE usuarios SET sal = ?, hash = ? WHERE id = ?", (sal.hex(), _hash(nueva, sal), usuario_id))
    con.commit()
