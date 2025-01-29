from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import pyodbc

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuración de la base de datos
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LENOVO2;'
        'DATABASE=TiendaLibros;'
        'UID=sa;'
        'PWD=123456;'
        'TrustServerCertificate=yes;'
    )
    return conn

# Usuarios y contraseñas
usuarios = {
    "juan": "ju2004",
    "andrea": "an2003"
}

@auth.verify_password
def verify_password(usuario, contraseña):
    if usuario in usuarios and usuarios[usuario] == contraseña:
        return usuario
    return None

# Ruta para obtener todos los libros
@app.route('/Libros', methods=['GET'])
@auth.login_required
def obtener_libros():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Libros')
    libros = cursor.fetchall()
    conn.close()
    return jsonify([{
        'ISBN': libro[0],
        'titulo': libro[1],
        'precio_compra': float(libro[2]),
        'precio_venta': float(libro[3]),
        'cantidad_actual': libro[4]
    } for libro in libros])

# Ruta para agregar un libro
@app.route('/Libros', methods=['POST'])
@auth.login_required
def agregar_libro():
    nuevo_libro = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Libros (ISBN, titulo, precio_compra, precio_venta, cantidad_actual) VALUES (?, ?, ?, ?, ?)',
                        nuevo_libro['ISBN'], nuevo_libro['titulo'], nuevo_libro['precio_compra'], nuevo_libro['precio_venta'], nuevo_libro['cantidad_actual'])
        conn.commit()
        return jsonify({'mensaje': 'Libro agregado exitosamente'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(port=5000)



