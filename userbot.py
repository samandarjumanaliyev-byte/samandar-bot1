from telethon import TelegramClient, events
import time

api_id = 21083126
api_hash = '2354685507583d97b1e3583cc8ff747d'

client = TelegramClient('samandar_userbot', api_id, api_hash)

auto_replies = {
    # O'z javoblaringizni shu yerga yozing
    # "salom": "Salom! 😊",
}

DEFAULT = "Xabaringizni oldim! Hozir band edim, tez orada javob beraman 😊"

last_active = 0
TIMEOUT = 300  # 5 daqiqa

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