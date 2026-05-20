from telethon import TelegramClient, events
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

api_id = 21083126
api_hash = '2354685507583d97b1e3583cc8ff747d'

client = TelegramClient('samandar_userbot', api_id, api_hash)

auto_replies = {}
DEFAULT = "Xabaringizni oldim! Hozir band edim, tez orada javob beraman 😊"
last_active = 0
TIMEOUT = 300

# Render uchun oddiy server
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot ishlayapti!')
    def log_message(self, *args):
        pass

def run_server():
    port = int(os.environ.get('PORT', 8080))
    HTTPServer(('', port), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

@client.on(events.NewMessage(outgoing=True))
async def track_active(event):
    global last_active
    last_active = time.time()

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handler(event):
    global last_active
    if event.out:
        return
    if time.time() - last_active < TIMEOUT:
        return
    text = event.raw_text.lower().strip()
    for keyword, reply in auto_replies.items():
        if keyword in text:
            await event.reply(reply)
            return
    await event.reply(DEFAULT)

client.start()
print("🤖 Samandar Userbot ishga tushdi!")
client.run_until_disconnected()