import requests

#Funcion para establecer la autenticación
def establecer_aut(usuario, contraseña):
    global auth 
    auth = (usuario, contraseña)

#Funcion para obtener libros
def obtener_libros():
    try:
        response = requests.get('http://localhost:5000/Libros', auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print (f"Error al obtener Libros: {e}")
        return[]
    
#Funcion para agregar libros
def agregar_libro(ISBN, titulo, precio_compra, precio_venta, cantidad_actual):
    data = {
        "ISBN": ISBN,
        "titulo": titulo,
        "precio_compra": precio_compra,
        "precio_venta": precio_venta,
        "cantidad_actual": cantidad_actual
    }
    try:
        response = requests.post('http://localhost:5000/Libros', json=data, auth=auth)
        response.raise_for_status()
        print("Libro agregado correctamente")
    except requests.exceptions.RequestException as e:
        print(f"Error al agregar Libro: {e}")