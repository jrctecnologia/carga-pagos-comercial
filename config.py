from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent
CONFIG_INI_PATH = BASE_DIR / "config.ini"


def _load_config() -> ConfigParser:
    """Carga config.ini. Si no existe o faltan claves, lanza error."""
    if not CONFIG_INI_PATH.exists():
        error_msg = f"ERROR: Archivo de configuración no encontrado: {CONFIG_INI_PATH}"
        print(error_msg, file=sys.stderr)
        alert_msg = f"⚠️ Archivo de configuración faltante\n\nDebería existir en:\n{CONFIG_INI_PATH}"
        # Mostrar alerta visual en pantalla
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error de Configuración", alert_msg)
            root.destroy()
        except:
            pass
        sys.exit(1)
    
    parser = ConfigParser()
    parser.read(CONFIG_INI_PATH, encoding="utf-8")
    
    # Validar que existan todas las secciones y claves requeridas
    required_config = {
        "database": ["server", "database", "user", "password", "driver"],
        "excel": ["file", "sheet_name"],
    }
    
    for section, keys in required_config.items():
        if not parser.has_section(section):
            error_msg = f"ERROR: Falta la sección '[{section}]' en {CONFIG_INI_PATH}"
            print(error_msg, file=sys.stderr)
            alert_msg = f"⚠️ Configuración incompleta\n\nFalta la sección:\n[{section}]"
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error de Configuración", alert_msg)
                root.destroy()
            except:
                pass
            sys.exit(1)
        
        for key in keys:
            if not parser.has_option(section, key):
                error_msg = f"ERROR: Falta la clave '{key}' en sección '[{section}]' en {CONFIG_INI_PATH}"
                print(error_msg, file=sys.stderr)
                alert_msg = f"⚠️ Configuración incompleta\n\nFalta en [{section}]:\n{key} = "
                try:
                    import tkinter as tk
                    from tkinter import messagebox
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Error de Configuración", alert_msg)
                    root.destroy()
                except:
                    pass
                sys.exit(1)
    
    return parser


_config = _load_config()

# Carga las constantes sin fallback - si no están, el programa habrá salido antes
DB_SERVER = _config.get("database", "server")
DB_DATABASE = _config.get("database", "database")
DB_USER = _config.get("database", "user")
DB_PASSWORD = _config.get("database", "password")
DB_DRIVER = _config.get("database", "driver")

EXCEL_FILE = _config.get("excel", "file")
SHEET_NAME = _config.get("excel", "sheet_name")
