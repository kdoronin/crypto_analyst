"""
Этот скрипт удаляет записи с null значениями в поле 'crypto' из JSON-файла с результатами анализа.
Он создает новый файл, содержащий только записи с валидными значениями криптовалют.
"""

import json

# Константы
INPUT_FILE = 'processed_messages_full.json'
OUTPUT_FILE = 'processed_messages_not_null.json'

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def remove_null_crypto():
    # Загружаем данные из входного файла
    messages = load_json(INPUT_FILE)
    
    # Фильтруем сообщения, оставляя только те, где crypto не null
    filtered_messages = [msg for msg in messages if msg['crypto'] is not None]
    
    # Сохраняем отфильтрованные сообщения в новый файл
    save_json(filtered_messages, OUTPUT_FILE)
    
    print(f"Processing complete. Removed {len(messages) - len(filtered_messages)} messages with null crypto.")
    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    remove_null_crypto()