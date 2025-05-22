import sqlite3

# Crear conexión
conn = sqlite3.connect("eventos.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    nombre TEXT,
    tipo TEXT,
    lugar TEXT,
    comentario TEXT
)
""")
conn.commit()

# Funciones CRUD
def agregar_evento(fecha, nombre, tipo, lugar, comentario):
    cursor.execute("INSERT INTO eventos (fecha, nombre, tipo, lugar, comentario) VALUES (?, ?, ?, ?, ?)",
                   (fecha, nombre, tipo, lugar, comentario))
    conn.commit()

def obtener_eventos():
    cursor.execute("SELECT * FROM eventos ORDER BY fecha DESC")
    return cursor.fetchall()

def eliminar_evento(id):
    cursor.execute("DELETE FROM eventos WHERE id = ?", (id,))
    conn.commit()
