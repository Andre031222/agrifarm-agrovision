"""Interfaz de línea de comandos: python -m agrovision.cli <comando> ..."""
import argparse
import getpass
import os
import sys
from datetime import date

from . import auth, clima, db, mercado, plagas
from .config import CULTIVOS


def _imprimir(filas):
    if not filas:
        print("(sin datos)")
    for fila in filas:
        print("  " + " | ".join(f"{k}={v}" for k, v in fila.items()))


def cmd_parcela(args, con):
    if args.accion == "agregar":
        pid = db.agregar_parcela(con, args.nombre, args.cultivo, args.lat, args.lon, args.area, args.siembra)
        print(f"Parcela {pid} registrada.")
    else:
        _imprimir(db.listar_parcelas(con))


def cmd_clima(args, con):
    parcela = db.obtener_parcela(con, args.parcela)
    datos = clima.obtener_clima(parcela["latitud"], parcela["longitud"])
    resumen = clima.resumen_climatico(datos, parcela["cultivo"])
    print(f"Parcela {parcela['nombre']} ({parcela['cultivo']}), últimos 7 días + pronóstico de 7:")
    print(f"  Precipitación total: {resumen['precip_total']} mm")
    print(f"  Racha seca máxima: {resumen['racha_seca_max']} días")
    print(f"  Grados-día acumulados: {resumen['grados_dia']}")
    print("  Heladas:")
    _imprimir(resumen["heladas"])
    for criterio in ("hutton", "smith"):
        periodos = plagas.periodos_criticos_rancha(datos["horario"], criterio)
        print(f"  Periodos críticos de rancha ({criterio}): {', '.join(periodos) or 'ninguno'}")


def cmd_plaga(args, con):
    if args.accion == "registrar":
        plagas.registrar_monitoreo(con, args.parcela, args.fecha, args.plaga, args.evaluadas, args.afectadas, args.notas)
        print(f"Incidencia registrada: {plagas.incidencia(args.afectadas, args.evaluadas)} %")
    else:
        _imprimir(plagas.alertas_monitoreo(con, args.parcela))


def cmd_precios(args, con):
    if args.accion == "importar":
        print(f"{mercado.importar_csv(con, args.archivo, args.fuente)} precios importados.")
    else:
        resumen = mercado.resumen_precios(con, args.producto, args.mercado)
        print(resumen if resumen else "(sin datos para ese producto)")


def cmd_oferta(args, con):
    if args.accion == "publicar":
        oid = mercado.publicar_oferta(con, args.productor, args.producto, args.cantidad, args.precio,
                                      args.contacto, args.lugar)
        print(f"Oferta {oid} publicada.")
    elif args.accion == "cerrar":
        mercado.cerrar_oferta(con, args.id)
        print(f"Oferta {args.id} cerrada.")
    else:
        _imprimir(mercado.listar_ofertas(con, args.producto))


def cmd_usuario(args, con):
    if args.accion == "crear":
        password = os.environ.get("AGROVISION_PASSWORD") or getpass.getpass("Contraseña (mín. 8): ")
        uid = auth.crear_usuario(con, args.usuario, password, args.nombre, "admin" if args.admin else "productor")
        print(f"Usuario {args.usuario} creado (id {uid}).")
    elif args.accion == "rol":
        auth.cambiar_rol(con, args.usuario, args.rol)
        print(f"Usuario {args.usuario}: rol {args.rol}.")
    else:
        _imprimir([dict(f) for f in con.execute("SELECT id, usuario, nombre, rol, creado FROM usuarios")])


def cmd_margen(args, con):
    print(mercado.margen(args.rendimiento, args.precio, args.costos))


def construir_parser():
    p = argparse.ArgumentParser(prog="agrovision", description="Monitoreo climático, de plagas y de mercado.")
    p.add_argument("--db", help="Ruta de la base SQLite (por defecto AGROVISION_DB o agrovision.db)")
    sub = p.add_subparsers(dest="comando", required=True)

    s = sub.add_parser("parcela", help="Registrar o listar parcelas")
    s.add_argument("accion", choices=["agregar", "listar"])
    s.add_argument("--nombre")
    s.add_argument("--cultivo", choices=sorted(CULTIVOS))
    s.add_argument("--lat", type=float)
    s.add_argument("--lon", type=float)
    s.add_argument("--area", type=float)
    s.add_argument("--siembra", help="AAAA-MM-DD")
    s.set_defaults(func=cmd_parcela, requeridos={"agregar": ["nombre", "cultivo", "lat", "lon"]})

    s = sub.add_parser("clima", help="Indicadores climáticos y riesgo de rancha de una parcela")
    s.add_argument("--parcela", type=int, required=True)
    s.set_defaults(func=cmd_clima)

    s = sub.add_parser("plaga", help="Registrar monitoreos o ver alertas")
    s.add_argument("accion", choices=["registrar", "alertas"])
    s.add_argument("--parcela", type=int)
    s.add_argument("--plaga")
    s.add_argument("--evaluadas", type=int)
    s.add_argument("--afectadas", type=int)
    s.add_argument("--fecha", default=date.today().isoformat())
    s.add_argument("--notas")
    s.set_defaults(func=cmd_plaga, requeridos={"registrar": ["parcela", "plaga", "evaluadas", "afectadas"]})

    s = sub.add_parser("precios", help="Importar precios o ver su resumen")
    s.add_argument("accion", choices=["importar", "resumen"])
    s.add_argument("archivo", nargs="?")
    s.add_argument("--fuente")
    s.add_argument("--producto")
    s.add_argument("--mercado")
    s.set_defaults(func=cmd_precios, requeridos={"importar": ["archivo"], "resumen": ["producto"]})

    s = sub.add_parser("oferta", help="Ofertas de venta directa")
    s.add_argument("accion", choices=["publicar", "listar", "cerrar"])
    s.add_argument("--id", type=int)
    s.add_argument("--productor")
    s.add_argument("--producto")
    s.add_argument("--cantidad", type=float)
    s.add_argument("--precio", type=float)
    s.add_argument("--contacto")
    s.add_argument("--lugar")
    s.set_defaults(func=cmd_oferta, requeridos={
        "publicar": ["productor", "producto", "cantidad", "precio"], "cerrar": ["id"]})

    s = sub.add_parser("usuario", help="Crear o listar usuarios del panel web")
    s.add_argument("accion", choices=["crear", "listar", "rol"])
    s.add_argument("--usuario")
    s.add_argument("--nombre")
    s.add_argument("--admin", action="store_true", help="Crear con rol de administrador")
    s.add_argument("--rol", choices=["productor", "admin"])
    s.set_defaults(func=cmd_usuario, requeridos={"crear": ["usuario", "nombre"], "rol": ["usuario", "rol"]})

    s = sub.add_parser("margen", help="Rentabilidad de una campaña")
    s.add_argument("--rendimiento", type=float, required=True, help="kg cosechados")
    s.add_argument("--precio", type=float, required=True, help="S/ por kg")
    s.add_argument("--costos", type=float, required=True, help="S/ totales")
    s.set_defaults(func=cmd_margen)
    return p


def main(argv=None):
    parser = construir_parser()
    args = parser.parse_args(argv)
    faltan = [f"--{c}" if c != "archivo" else "archivo"
              for c in getattr(args, "requeridos", {}).get(getattr(args, "accion", None), [])
              if getattr(args, c) is None]
    if faltan:
        parser.error(f"'{args.comando} {args.accion}' requiere: {', '.join(faltan)}")
    con = db.conectar(args.db)
    try:
        args.func(args, con)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
