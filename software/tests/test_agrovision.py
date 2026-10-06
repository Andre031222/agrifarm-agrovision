"""Pruebas sin red: usan datos horarios y precios construidos a mano."""
from datetime import date, timedelta
from pathlib import Path

import pytest

from agrovision import auth, clima, db, mercado, plagas


@pytest.fixture
def con():
    conexion = db.conectar(":memory:")
    yield conexion
    conexion.close()


def horario_dias(dias):
    """dias: lista de (fecha, temp_constante, horas_con_hr_95)."""
    registros = []
    for fecha, temp, horas_humedas in dias:
        for h in range(24):
            registros.append({"hora": f"{fecha}T{h:02d}:00", "temp": temp,
                              "hr": 95 if h < horas_humedas else 60, "precip": 0})
    return registros


# --- clima ---------------------------------------------------------------

def test_normalizar_open_meteo():
    crudo = {
        "hourly": {"time": ["2026-01-01T00:00"], "temperature_2m": [5.0],
                   "relative_humidity_2m": [80], "precipitation": [0.2]},
        "daily": {"time": ["2026-01-01"], "temperature_2m_max": [15.0],
                  "temperature_2m_min": [-1.0], "precipitation_sum": [3.0]},
    }
    datos = clima.normalizar(crudo)
    assert datos["horario"][0] == {"hora": "2026-01-01T00:00", "temp": 5.0, "hr": 80, "precip": 0.2}
    assert datos["diario"][0]["tmin"] == -1.0


def test_riesgo_helada_niveles():
    diario = [{"fecha": "a", "tmin": -3}, {"fecha": "b", "tmin": -1}, {"fecha": "c", "tmin": 2},
              {"fecha": "d", "tmin": None}]
    alertas = clima.riesgo_helada(diario, helada_critica=-2)
    assert [(a["fecha"], a["nivel"]) for a in alertas] == [("a", "alto"), ("b", "moderado")]


def test_racha_seca_y_grados_dia():
    diario = [{"tmax": 20, "tmin": 4, "precip": p} for p in (0, 0.5, 5, 0, 0, 0)]
    assert clima.racha_seca_maxima(diario) == 3
    assert clima.grados_dia(diario, temp_base=7) == 30.0  # (12 - 7) * 6


def test_condicion_actual():
    datos = {"horario": horario_dias([("2026-02-01", 12, 3)]),
             "diario": [{"fecha": "2026-02-01", "tmax": 15, "tmin": 2, "precip": 0}]}
    actual, dia = clima.condicion_actual(datos, "2026-02-01T05:42")
    assert actual["hora"] == "2026-02-01T05:00" and actual["hr"] == 60
    assert dia["tmin"] == 2
    assert clima.condicion_actual(datos, "2026-03-01T00:00") == (None, None)


def test_resumen_cultivo_desconocido():
    with pytest.raises(ValueError):
        clima.resumen_climatico({"diario": []}, "cebada")


# --- plagas --------------------------------------------------------------

def test_periodo_critico_hutton_requiere_dos_dias_seguidos():
    horario = horario_dias([("2026-02-01", 12, 8), ("2026-02-02", 12, 8), ("2026-02-03", 12, 2)])
    assert plagas.dias_favorables_rancha(horario) == ["2026-02-01", "2026-02-02"]
    assert plagas.periodos_criticos_rancha(horario, "hutton") == ["2026-02-02"]


def test_smith_mas_exigente_que_hutton():
    horario = horario_dias([("2026-02-01", 12, 8), ("2026-02-02", 12, 8)])
    assert plagas.periodos_criticos_rancha(horario, "hutton") == ["2026-02-02"]
    assert plagas.periodos_criticos_rancha(horario, "smith") == []


def test_dias_no_consecutivos_y_dias_frios_no_cuentan():
    horario = horario_dias([("2026-02-01", 12, 12), ("2026-02-03", 12, 12), ("2026-02-04", 8, 12)])
    assert plagas.periodos_criticos_rancha(horario, "smith") == []


def test_dia_incompleto_se_ignora():
    horario = horario_dias([("2026-02-01", 12, 12), ("2026-02-02", 12, 12)])[:-1]
    assert plagas.dias_favorables_rancha(horario, "smith") == ["2026-02-01"]


def test_incidencia_validaciones():
    assert plagas.incidencia(5, 50) == 10.0
    with pytest.raises(ValueError):
        plagas.incidencia(6, 5)
    with pytest.raises(ValueError):
        plagas.incidencia(0, 0)


def test_alertas_umbral_y_tendencia(con):
    pid = db.agregar_parcela(con, "Lote 1", "papa", -15.8, -70.0, 1.0)
    plagas.registrar_monitoreo(con, pid, "2026-02-01", "Rancha", 50, 1)
    plagas.registrar_monitoreo(con, pid, "2026-02-08", "rancha", 50, 4)
    plagas.registrar_monitoreo(con, pid, "2026-02-08", "gorgojo de los andes", 50, 2)
    alertas = plagas.alertas_monitoreo(con, pid)
    assert alertas[0]["plaga"] == "rancha"
    assert alertas[0]["incidencia"] == 8.0 and alertas[0]["supera_umbral"]
    assert alertas[0]["tendencia"] == "sube"
    assert alertas[1]["supera_umbral"] is False and alertas[1]["tendencia"] == "estable"


# --- mercado -------------------------------------------------------------

def test_importar_csv_ejemplo(con):
    ruta = Path(__file__).resolve().parents[1] / "datos" / "precios_ejemplo_SINTETICO.csv"
    assert mercado.importar_csv(con, ruta, "ejemplo") == 144
    assert mercado.productos(con) == ["haba", "papa", "quinua"]
    # Reimportar no duplica (UNIQUE fecha+producto+mercado)
    mercado.importar_csv(con, ruta, "ejemplo")
    assert con.execute("SELECT COUNT(*) FROM precios").fetchone()[0] == 144


def test_importar_texto_errores(con):
    with pytest.raises(ValueError, match="Faltan columnas"):
        mercado.importar_texto(con, "fecha,producto\n2026-01-01,papa\n")
    with pytest.raises(ValueError, match="Fila 2"):
        mercado.importar_texto(con, "fecha,producto,mercado,precio_kg\n2026-13-01,papa,A,1\n")


def test_serie_promedia_mercados_y_tendencia(con):
    mercado.importar_texto(con, "fecha,producto,mercado,precio_kg\n"
                                "2026-01-01,papa,A,1.0\n2026-01-01,papa,B,2.0\n"
                                "2026-01-31,papa,A,2.0\n")
    assert mercado.serie(con, "papa") == [("2026-01-01", 1.5), ("2026-01-31", 2.0)]
    # Sube 0.5 en 30 días sobre una media de 1.75 -> 28.6 %
    assert mercado.tendencia(mercado.serie(con, "papa")) == 28.6
    assert mercado.tendencia([("2026-01-01", 1.0)]) is None


def test_media_movil_y_mejor_mes():
    assert mercado.media_movil([1, 2, 3, 4], 2) == [None, 1.5, 2.5, 3.5]
    datos = [("2025-03-10", 1.0), ("2025-07-10", 3.0), ("2026-07-10", 2.0)]
    assert mercado.promedio_mensual(datos) == {3: 1.0, 7: 2.5}
    assert mercado.mejor_mes_venta(datos) == 7


def test_margen():
    r = mercado.margen(rendimiento_kg=10000, precio_kg=1.5, costos=9000)
    assert r == {"ingreso": 15000.0, "costos": 9000.0, "margen": 6000.0,
                 "margen_pct": 40.0, "precio_equilibrio_kg": 0.9}
    with pytest.raises(ValueError):
        mercado.margen(0, 1, 1)


def test_ofertas(con):
    oid = mercado.publicar_oferta(con, "Ana", "Quinua", 200, 7.0, fecha=date.today().isoformat())
    assert mercado.listar_ofertas(con, "quinua")[0]["id"] == oid
    mercado.cerrar_oferta(con, oid)
    assert mercado.listar_ofertas(con) == []
    with pytest.raises(ValueError):
        mercado.cerrar_oferta(con, 999)


def test_cli_flujo_completo(tmp_path, capsys):
    from agrovision.cli import main
    base = str(tmp_path / "t.db")
    assert main(["--db", base, "parcela", "agregar", "--nombre", "L1", "--cultivo", "papa",
                 "--lat", "-15.8", "--lon", "-70"]) == 0
    assert main(["--db", base, "plaga", "registrar", "--parcela", "1", "--plaga", "rancha",
                 "--evaluadas", "20", "--afectadas", "2"]) == 0
    assert "10.0 %" in capsys.readouterr().out
    assert main(["--db", base, "margen", "--rendimiento", "100", "--precio", "2", "--costos", "50"]) == 0
    with pytest.raises(SystemExit):
        main(["--db", base, "parcela", "agregar", "--nombre", "sin datos"])


# --- usuarios ------------------------------------------------------------

def test_usuario_crear_y_verificar(con):
    uid = auth.crear_usuario(con, "Flor.Y", "clave-segura-1", "Flor")
    assert auth.verificar(con, "flor.y", "clave-segura-1") == {"id": uid, "usuario": "flor.y", "nombre": "Flor",
                                                               "rol": "productor"}
    assert auth.verificar(con, "flor.y", "otra-clave-xx") is None
    assert auth.verificar(con, "nadie", "clave-segura-1") is None
    fila = con.execute("SELECT hash FROM usuarios").fetchone()
    assert "clave-segura-1" not in fila["hash"]


def test_usuario_validaciones(con):
    auth.crear_usuario(con, "andre", "clave-de-prueba", "Andre")
    with pytest.raises(ValueError, match="ya existe"):
        auth.crear_usuario(con, "ANDRE", "clave-de-prueba", "Otro")
    with pytest.raises(ValueError, match="8 caracteres"):
        auth.crear_usuario(con, "nuevo", "corta", "N")
    with pytest.raises(ValueError, match="usuario debe"):
        auth.crear_usuario(con, "a b", "clave-de-prueba", "N")


def test_cambiar_password(con):
    uid = auth.crear_usuario(con, "sebas", "inicial-123", "Sebas")
    auth.cambiar_password(con, uid, "nueva-clave-9")
    assert auth.verificar(con, "sebas", "inicial-123") is None
    assert auth.verificar(con, "sebas", "nueva-clave-9")["id"] == uid


def test_parcelas_por_usuario(con):
    a = auth.crear_usuario(con, "user.a", "clave-de-prueba", "A")
    b = auth.crear_usuario(con, "user.b", "clave-de-prueba", "B")
    db.agregar_parcela(con, "PA", "papa", -15.8, -70.0, usuario_id=a)
    db.agregar_parcela(con, "PB", "quinua", -15.8, -70.0, usuario_id=b)
    assert [p["nombre"] for p in db.listar_parcelas(con, a)] == ["PA"]
    assert len(db.listar_parcelas(con)) == 2


def test_migracion_base_antigua(tmp_path):
    import sqlite3
    ruta = tmp_path / "vieja.db"
    vieja = sqlite3.connect(ruta)
    vieja.execute("CREATE TABLE parcelas (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, cultivo TEXT NOT NULL, "
                  "latitud REAL NOT NULL, longitud REAL NOT NULL, area_ha REAL, fecha_siembra TEXT)")
    vieja.commit()
    vieja.close()
    con = db.conectar(str(ruta))
    assert "usuario_id" in {f["name"] for f in con.execute("PRAGMA table_info(parcelas)")}
    con.close()


def test_cli_usuario(tmp_path, monkeypatch, capsys):
    from agrovision.cli import main
    monkeypatch.setenv("AGROVISION_PASSWORD", "clave-cli-123")
    base = str(tmp_path / "u.db")
    assert main(["--db", base, "usuario", "crear", "--usuario", "maribel", "--nombre", "Maribel"]) == 0
    assert "creado" in capsys.readouterr().out
    assert main(["--db", base, "usuario", "crear", "--usuario", "maribel", "--nombre", "X"]) == 1


def test_solo_el_duenio_cierra_su_oferta(con):
    a = auth.crear_usuario(con, "duenio", "clave-de-prueba", "A")
    b = auth.crear_usuario(con, "otro", "clave-de-prueba", "B")
    oid = mercado.publicar_oferta(con, "A", "papa", 100, 1.5, usuario_id=a)
    with pytest.raises(PermissionError):
        mercado.cerrar_oferta(con, oid, usuario_id=b)
    mercado.cerrar_oferta(con, oid, usuario_id=a)
    assert mercado.listar_ofertas(con) == []


# --- roles y CLI completo ---------------------------------------------------

def test_roles(con):
    auth.crear_usuario(con, "admin1", "clave-de-prueba", "Admin", rol="admin")
    auth.crear_usuario(con, "prod1", "clave-de-prueba", "Prod")
    assert auth.es_admin(auth.verificar(con, "admin1", "clave-de-prueba"))
    assert not auth.es_admin(auth.verificar(con, "prod1", "clave-de-prueba"))
    auth.cambiar_rol(con, "prod1", "admin")
    assert auth.es_admin(auth.verificar(con, "prod1", "clave-de-prueba"))
    with pytest.raises(ValueError):
        auth.cambiar_rol(con, "prod1", "superusuario")
    with pytest.raises(ValueError):
        auth.cambiar_rol(con, "nadie", "admin")
    with pytest.raises(ValueError):
        auth.crear_usuario(con, "x1", "clave-de-prueba", "X", rol="root")


def test_cli_todos_los_comandos(tmp_path, monkeypatch, capsys):
    from agrovision.cli import main
    base = str(tmp_path / "c.db")
    hoy = date.today()
    dias = [((hoy - timedelta(days=k)).isoformat(), 12, 8) for k in (1, 0)]
    falso = {"horario": horario_dias(dias),
             "diario": [{"fecha": f, "tmax": 15, "tmin": -3, "precip": 0} for f, _, _ in dias]}
    monkeypatch.setattr(clima, "obtener_clima", lambda lat, lon: falso)
    monkeypatch.setenv("AGROVISION_PASSWORD", "clave-de-prueba")
    csv = tmp_path / "p.csv"
    csv.write_text("fecha,producto,mercado,precio_kg\n2025-01-15,papa,A,1.2\n2025-02-15,papa,A,1.5\n")
    pasos = [
        ["parcela", "agregar", "--nombre", "L1", "--cultivo", "papa", "--lat", "-15.8", "--lon", "-70"],
        ["parcela", "listar"],
        ["clima", "--parcela", "1"],
        ["plaga", "registrar", "--parcela", "1", "--plaga", "rancha", "--evaluadas", "10", "--afectadas", "3"],
        ["plaga", "alertas"],
        ["precios", "importar", str(csv), "--fuente", "prueba"],
        ["precios", "resumen", "--producto", "papa"],
        ["oferta", "publicar", "--productor", "Ana", "--producto", "papa", "--cantidad", "10", "--precio", "2"],
        ["oferta", "listar"],
        ["oferta", "cerrar", "--id", "1"],
        ["usuario", "crear", "--usuario", "ana", "--nombre", "Ana", "--admin"],
        ["usuario", "rol", "--usuario", "ana", "--rol", "productor"],
        ["usuario", "listar"],
    ]
    for args in pasos:
        assert main(["--db", base] + args) == 0, args
    salida = capsys.readouterr().out
    assert "Periodos críticos de rancha (hutton): " + date.today().isoformat() in salida
    assert "nivel=alto" in salida  # mínima de -3 °C bajo el umbral de helada de la papa
    assert "2 precios importados" in salida and "rol productor" in salida
    assert main(["--db", base, "precios", "resumen", "--producto", "quinua"]) == 0
    assert "(sin datos" in capsys.readouterr().out
    assert main(["--db", base, "oferta", "cerrar", "--id", "99"]) == 1
