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