import threading
import webbrowser
import importlib.resources as pkg_resources

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Crea l'app FastAPI
app = FastAPI()

# Serve la directory statica (build del frontend)
static_dir = str(pkg_resources.files(__package__).joinpath("static"))
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# (Opzionale) Importa e monta API REST per la GUI (es. api.py)
try:
    from belso.gui.api import router as api_router
    app.include_router(api_router, prefix="/api")
except ImportError:
    pass  # Nessuna API per ora, o API non ancora implementate

def start_gui():
    port = 7860
    url = f"http://127.0.0.1:{port}/"
    print(f"\n🌐 Belso GUI running at: {url}")
    # Apri il browser in un thread separato
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=port)
