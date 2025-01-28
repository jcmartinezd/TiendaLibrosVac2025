from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import pyodbc

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuración de la base de datos 
def get_db_connection():
    conn = pyodbc.connect(
        driver='{ODBC Driver 17 for SQL Server}',
        server='LENOVO2',
        database='TiendaLibrosVac2025',
        uid='sa',
        pwd='123456'
    )
    return conn

# Usuarios y contraseñas

usuarios = {
    'admin': 'admin123',
    'user': 'user123',
    'juan' : 'juan123',
}

@auth.verify_password
def verify_password(usuario, contraseña):
    if usuario in usuarios and usuarios[usuario] == contraseña:
        return usuario
    return None       




@app.route('/Libros', methods=['GET'])
@auth.login_required
def obtener_libros():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    conn.close()
    return jsonify([{
        'ISBN':libro[0],
        'titulo': libro[1],
        'precio_compra': float(libro[2]),
        'precio_venta': float(libro[3]),
        'cantidad_actual': int(libro[4])
    }for libro in libros ])

