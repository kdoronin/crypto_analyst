"""
Этот скрипт парсит сообщения из Telegram-канала без использования официального API.
Он собирает сообщения, начиная с определенного ID, и сохраняет их в JSON-файл.
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import os

channel_username = ''
start_message_id = 1
json_filename = 'messages.json'

def get_channel_messages(channel_username, start_message_id):
    all_messages = load_existing_messages()
    current_id = start_message_id
    consecutive_empty_responses = 0
    max_empty_responses = 3

    while True:
        url = f"https://t.me/s/{channel_username}/{current_id}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to fetch messages. Status code: {response.status_code}")
            break
        
        messages = extract_messages(response.text)
        
        if not messages:
            consecutive_empty_responses += 1
            print(f"No messages found for ID {current_id}. Empty responses: {consecutive_empty_responses}")
            if consecutive_empty_responses >= max_empty_responses:
                print("Reached maximum number of consecutive empty responses. Stopping.")
                break
        else:
            consecutive_empty_responses = 0
            new_messages = [msg for msg in messages if msg['id'] not in [m['id'] for m in all_messages]]
            all_messages.extend(new_messages)
            print(f"Fetched {len(new_messages)} new messages. Total: {len(all_messages)}")
            save_messages_to_json(all_messages)
            current_id = min(msg['id'] for msg in messages) - 1

        if current_id <= 1:
            print("Reached the beginning of the channel. Stopping.")
            break
        
        time.sleep(1)
    
    return all_messages

def extract_messages(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    messages = []
    
    for message_div in soup.find_all('div', class_='tgme_widget_message'):
        message_id = message_div.get('data-post', '').split('/')[-1]
        date = message_div.find('time', class_='time')['datetime'] if message_div.find('time', class_='time') else ''
        text = message_div.find('div', class_='tgme_widget_message_text')
        text = text.get_text(strip=True) if text else ''
        
        messages.append({
            'id': int(message_id) if message_id.isdigit() else None,
            'date': date,
            'message': text
        })
    
    return messages

def load_existing_messages():
    if os.path.exists(json_filename):
        with open(json_filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_messages_to_json(messages):
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def main():
    messages = get_channel_messages(channel_username, start_message_id)
    print(f"Parsed {len(messages)} messages and saved to {json_filename}")

if __name__ == '__main__':
    main()