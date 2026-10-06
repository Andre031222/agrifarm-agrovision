# AgriFarm AgroVision

Open-source tool for climate, pest and market monitoring for smallholders in the Peruvian altiplano (Puno).

## What it does

- **Climate:** frost risk per crop, dry spells and growing degree-days from [Open-Meteo](https://open-meteo.com/) (no API key).
- **Pests:** Smith and Hutton late-blight critical periods; field-scouting records with incidence, action threshold and trend.
- **Market:** price import (CSV), trend, monthly seasonality, best selling month, margin and break-even price; direct-sale offers.
- **Web panel** (Streamlit) in Spanish and English, with user accounts and roles, plus a command-line interface.

## Quick start

```bash
cd software
python3 -m venv .venv
.venv/bin/pip install -e ".[dev,panel]"
.venv/bin/python -m pytest              # 27 offline tests
.venv/bin/streamlit run app/streamlit_app.py
```

See [`software/README.md`](software/README.md) for the CLI and details.

## Notes

- Agronomic thresholds in `software/agrovision/config.py` are provisional.
- `software/datos/precios_ejemplo_SINTETICO.csv` is synthetic demo data, not real prices.

## License

MIT — see [LICENSE](LICENSE).
