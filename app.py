from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument  # Gerekli sınıfları import ettik
import logging
import re

# Telegram API bilgileri
api_id = '29444056'
api_hash = '2f4d6c5ad97e4f9fbb15a9809d5f9056'
phone = '+905525515184'

# Kaynak ve hedef grup ID'leri
SOURCE_CHAT_IDS = [
-1001692375261, -1001200424456, -1001688680661, -1002072387989, -1001358643502 
]
TARGET_CHAT_ID = -1002445915101  # Hedef grup ID

# Logging yapılandırması
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Telegram istemcisi
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHAT_IDS))
async def handler(event):
    message = event.message
    message_text = message.message

    # Grubun bilgilerini al
    chat = await event.get_chat()

    # Grup adı ve bağlantısı
    if hasattr(chat, 'username') and chat.username:  # Grubun kullanıcı adı varsa
        group_link = f"https://t.me/{chat.username}"
        group_name = f"[{chat.title}]({group_link})"
    else:  # Grubun kullanıcı adı yoksa
        group_name = f"{chat.title} (Bu grup bağlantısızdır)"

    # Grup bilgisini ekle
    source_chat_info = f"{group_name}\n\n"

    # Yasaklı argümanları belirle
    forbidden_pattern = re.compile(r'http[s]?://|www\.|@[\w_]+|t\.me')

    # Mesajın gönderileceği durumu kontrol et
    if forbidden_pattern.search(message_text):
        logging.info(f"Message contains prohibited content, not forwarding: {message_text}")
    else:
        # Grup bilgisi ile birleştir
        full_message = source_chat_info + message_text

        # Mesajı gönder
        if message.media:
            await client.send_message(TARGET_CHAT_ID, full_message, file=message.media, link_preview=False)
        else:
            await client.send_message(TARGET_CHAT_ID, full_message, link_preview=False)

        logging.info(f"Message forwarded: {full_message}")

async def main():
    # Giriş yap
    await client.start(phone)
    logging.info("Client started")
    # Dinlemeye başla
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
