from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
import sys
from utils import log_line, obtener_ruta_base, show_msgbox

BASE_DIR = Path(obtener_ruta_base())
CONFIG_INI_PATH = BASE_DIR / "config.ini"


def _load_config() -> ConfigParser:
    # Carga config.ini. Si no existe o faltan claves, lanza error.
    if not CONFIG_INI_PATH.exists():
        error_msg = f"ERROR: Archivo de configuracion no encontrado: {CONFIG_INI_PATH}"
        log_line(error_msg)
        show_msgbox("no se pudo procesar la información")
        sys.exit(1)
    
    parser = ConfigParser()
    parser.read(CONFIG_INI_PATH, encoding="utf-8")
    
    # Validar que existan todas las secciones y claves requeridas
    required_config = {
        "database": ["server", "database", "user", "password", "driver"],
        "excel": ["file", "sheet_name"],
        "conceptos": ["codigo_factura", "codigo_pago"],
    }
    
    for section, keys in required_config.items():
        if not parser.has_section(section):
            error_msg = f"ERROR: Falta la seccion '[{section}]' en {CONFIG_INI_PATH}"
            log_line(error_msg)
            sys.exit(1)
        
        for key in keys:
            if not parser.has_option(section, key):
                error_msg = f"ERROR: Falta la clave '{key}' en seccion '[{section}]' en {CONFIG_INI_PATH}"
                log_line(error_msg)
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

CODIGO_CONCEPTO_FACTURA = _config.get("conceptos", "codigo_factura")
CODIGO_CONCEPTO_PAGO = _config.get("conceptos", "codigo_pago")
