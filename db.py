import pyodbc

from config import (
    DB_SERVER,
    DB_DATABASE,
    DB_USER,
    DB_PASSWORD,
    DB_DRIVER
)

def get_connection():
    conn_str = (
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)
