import sqlite3
import random
from pathlib import Path

DB_PATH = Path("locations.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        )
    """)
    
    dados = [
        ("Cristo Redentor", "Brasil", "Rio de Janeiro", -22.9519, -43.2105),
        ("Pirâmides de Gizé", "Egito", "Gizé", 29.9792, 31.1342),
        ("Coliseu", "Itália", "Roma", 41.8902, 12.4922),
        ("Torre Eiffel", "França", "Paris", 48.8584, 2.2945),
        ("Estátua da Liberdade", "Estados Unidos", "Nova York", 40.6892, -74.0445),
        ("Machu Picchu", "Peru", "Cusco", -13.1631, -72.5450),
        ("Taj Mahal", "Índia", "Agra", 27.1751, 78.0421),
        ("Ópera de Sydney", "Austrália", "Sydney", -33.8568, 151.2153),
    ]
    
    conn.executemany(
        "INSERT OR IGNORE INTO locations (name, country, city, lat, lon) VALUES (?,?,?,?,?)",
        dados
    )
    conn.commit()
    conn.close()

def get_random_location():
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT id, name, country, city, lat, lon FROM locations ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    
    answer = f"{row[1]}, {row[2]}" if row[3] is None else f"{row[1]}, {row[2]}"
    return {
        "id": row[0],
        "name": row[1],
        "country": row[2],
        "city": row[3],
        "lat": row[4],
        "lon": row[5],
        "answer": answer
    }