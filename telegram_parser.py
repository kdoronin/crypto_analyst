from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
import os

# Replace these with your own values
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'
channel_username = ''
start_message_id = 1

async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone_number)

    channel = await client.get_entity(channel_username)
    
    offset_id = 0
    limit = 100
    all_messages = []

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        all_messages.extend(messages)
        offset_id = messages[-1].id
        if offset_id <= 1:
            break

    # Filter messages from the starting point
    filtered_messages = [msg for msg in all_messages if msg.id <= start_message_id]

    # Save messages to a file
    with open('buff_10_messages.txt', 'w', encoding='utf-8') as f:
        for message in reversed(filtered_messages):
            f.write(f"Message ID: {message.id}\n")
            f.write(f"Date: {message.date}\n")
            f.write(f"Text: {message.text}\n")
            f.write("-" * 50 + "\n")

    print(f"Parsed {len(filtered_messages)} messages and saved to buff_10_messages.txt")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())