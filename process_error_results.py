"""
Этот скрипт обрабатывает файлы с ошибками, возникшими при анализе сообщений.
Он извлекает валидный JSON из файлов с ошибками и добавляет эту информацию в основной файл результатов.
"""

import json
import os
import re

# Константы
INPUT_FILE = 'processed_messages.json'
OUTPUT_FILE = 'processed_messages_full.json'
ERROR_FILE_PREFIX = 'error_result_'

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_valid_json(text):
    # Ищем текст, заключенный в квадратные скобки, который может быть JSON-массивом
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if match:
        try:
            # Пробуем распарсить найденный текст как JSON
            return json.loads(match.group())
        except json.JSONDecodeError:
            print(f"Found text in brackets, but it's not a valid JSON: {match.group()}")
    return None

def process_error_files():
    processed_messages = load_json(INPUT_FILE)
    processed_ids = set(msg['id'] for msg in processed_messages)
    
    for filename in os.listdir('.'):
        if filename.startswith(ERROR_FILE_PREFIX):
            print(f"Processing file: {filename}")
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            valid_json = extract_valid_json(content)
            if valid_json:
                for item in valid_json:
                    if item['id'] not in processed_ids:
                        processed_messages.append(item)
                        processed_ids.add(item['id'])
                print(f"Added {len(valid_json)} new items from {filename}")
            else:
                print(f"No valid JSON found in {filename}")
    
    # Сортируем сообщения по ID перед сохранением
    processed_messages.sort(key=lambda x: x['id'])
    
    save_json(processed_messages, OUTPUT_FILE)
    print(f"Processing complete. Results saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    process_error_files()