from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession
from telethon.extensions import markdown
from telethon import types

import json

with open('channel_relations.json') as f:
  data = json.load(f)

api_id = '22368708'
api_hash = 'YOUR_API_HASH'
String_session = "1BVtsOJQBu6yQogLqkSMAD5Iblkqb7K_QUqmnpeg4mKZfQMQxHIt9yVchK-q3viXd9pMuM4p8Ufeh-cxZNSioIRzop8Mqp9E6hokdGMLNKCiuMFjlxuo2ZFqdL6UTrcbfHi8TlW8SZm2le-1gl5-nrsrVEmRUPwap1mgr8WLl4PVEHZkCWIHSXzwri_skoFbrydWqS-dPeIJwiifIybCywl305R1Pfez35akyxdNxjNO2R5lEqFRY45gNk6nYODKv3SR-fF6qBxPvJJjTTOB6_OnjS0H8TxpuM6CexafmmStBYuq8n06hS-fJcF08SVVYpT-uW088ZMwyn7PHtgd5701QiIFoFcE="

source_channel = [i for i in data]  # The channel from which to listen for new posts
# print(source_channel)

# # Create the client and connect to Telegram
client = TelegramClient(StringSession(String_session),api_id,api_hash)

class CustomMarkdown:
    @staticmethod
    def parse(text):
        text, entities = markdown.parse(text)
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, int(e.url.split('/')[1]))
        return text, entities
    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return markdown.unparse(text, entities)

client.parse_mode = CustomMarkdown()

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message
    channel_name = event.chat.username if event.chat.username else "Username not available"
    print(f"Copying message from @{channel_name}")

    destination_channels = data[channel_name]
    print(destination_channels)
    for dest_channel in destination_channels:
        try:
            await client.send_message(dest_channel, msg)
        except Exception as e:
            print(e)
        print(dest_channel)
# # Start the client
with client:
    client.run_until_disconnected()
