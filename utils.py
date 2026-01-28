import ctypes
from datetime import datetime
from pathlib import Path
import sys
import os


def obtener_ruta_base():
    """
    Devuelve la carpeta donde está el ejecutable o el script.
    Funciona para Python normal y para PyInstaller (--onefile).
    """
    if getattr(sys, 'frozen', False):
        # Ejecutable (.exe)
        return os.path.dirname(sys.executable)
    else:
        # Script .py
        return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = Path(obtener_ruta_base())
LOG_PATH = BASE_DIR / "log.txt"


def log_line(message):
    # Registra una linea en el log con timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
        

def show_msgbox(message):
    try:
        ctypes.windll.user32.MessageBoxW(0, message, "Resultado", 0x40)
    except Exception as exc:
        log_line(f"Error mostrando msgbox: {exc}")


def _handle_exception(exc_type, exc, tb):
    # Maneja excepciones no capturadas
    log_line(f"Fallo general del proceso: {exc}")
    show_msgbox("no se pudo procesar")
