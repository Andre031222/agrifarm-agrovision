# AgriFarm AgroVision · v0.1

Monitoreo climático, de plagas y de mercado para pequeños productores del altiplano.
Sin IoT ni modelos de lenguaje: datos climáticos abiertos (Open-Meteo, sin API key),
reglas de alerta de rancha, registros de campo y análisis de precios.

## Instalación

```bash
cd software
python3 -m venv .venv
.venv/bin/pip install -e ".[dev,panel]"
```

El núcleo (`agrovision/`) solo usa la biblioteca estándar de Python. Streamlit se usa únicamente para el panel web.

## Uso

Panel web (estilo visual de AgroVision 360), con inicio de sesión:

```bash
AGROVISION_DB=agrovision.db .venv/bin/streamlit run app/streamlit_app.py
```

Abre http://localhost:8501. Para crear cuentas, usa la pestaña «Crear cuenta» o la línea de comandos (pide la contraseña sin mostrarla):

```bash
.venv/bin/agrovision --db agrovision.db usuario crear --usuario flor --nombre "Flor Yanarico"
```

Las contraseñas se guardan con PBKDF2-SHA256 y sal aleatoria; nunca en texto plano. Cada usuario ve solo sus parcelas, y las ofertas de venta son públicas. El usuario de desarrollo local está en `CREDENCIALES_LOCALES.txt`, que está excluido de git.

Línea de comandos:

```bash
.venv/bin/agrovision parcela agregar --nombre "Lote 1" --cultivo papa --lat -15.84 --lon -70.02
.venv/bin/agrovision clima --parcela 1
.venv/bin/agrovision plaga registrar --parcela 1 --plaga rancha --evaluadas 50 --afectadas 4
.venv/bin/agrovision plaga alertas
.venv/bin/agrovision precios importar datos/precios_ejemplo_SINTETICO.csv --fuente ejemplo
.venv/bin/agrovision precios resumen --producto quinua
.venv/bin/agrovision oferta publicar --productor Ana --producto papa --cantidad 300 --precio 1.8
.venv/bin/agrovision margen --rendimiento 10000 --precio 1.5 --costos 9000
```

La base SQLite se guarda en `agrovision.db`, o en la ruta indicada por `AGROVISION_DB` o `--db`.

## Pruebas

```bash
.venv/bin/python -m pytest
```

Son 24 pruebas sin conexión a internet.

## Estructura

| Ruta | Contenido |
|---|---|
| `agrovision/config.py` | Parámetros por cultivo, umbrales de plaga, criterios de rancha |
| `agrovision/clima.py` | Open-Meteo, heladas, rachas secas, grados-día |
| `agrovision/plagas.py` | Criterios Hutton/Smith, incidencia, alertas y tendencia |
| `agrovision/mercado.py` | Precios (CSV), tendencia, estacionalidad, margen, ofertas |
| `agrovision/db.py` | Esquema SQLite y migración |
| `agrovision/auth.py` | Usuarios y contraseñas |
| `agrovision/cli.py` | Comandos |
| `app/` | Panel Streamlit y estilos |

## Advertencias para el artículo

- Los valores de `config.py` son **provisionales** y deben validarse con un agrónomo y con bibliografía.
- `datos/precios_ejemplo_SINTETICO.csv` contiene datos **inventados**, útiles solo para probar el software. En el artículo se usan datos oficiales citando su fuente.
- Los criterios de Hutton y Smith vienen del Reino Unido. En Puno casi nunca se activan; calibrarlos es la pregunta de investigación.
