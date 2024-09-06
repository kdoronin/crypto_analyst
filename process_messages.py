"""
Этот скрипт обрабатывает собранные сообщения из Telegram-канала, используя API Groq.
Он анализирует содержимое сообщений, извлекает информацию о криптовалютах и сохраняет результаты в JSON-файл.
"""
import json
import requests
import os
import time
from datetime import datetime

# Константы
INPUT_FILE = 'buff_10_messages.json'
OUTPUT_FILE = 'processed_messages.json'
GROQ_API_KEY = ''
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
BATCH_SIZE = 12
RATE_LIMIT_DELAY = 60
MAX_TOKENS = 8000
TOKEN_OVERFLOW_DELAY = 60
START_STEP = 364

def load_messages():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_processed_messages(messages):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def process_batch(batch):
    prompt = """Проанализируй следующие сообщения из Telegram-канала. В поле message может быть информация о том, какой вид криптовалюты закупаем сегодня на $10. Это также называют экспериментальным портфелем или используют другие метафоры. Тебе нужно распознать метафору и понять, какую монету покупают в эту дату. 

Для каждого сообщения создай JSON-объект с следующими полями:
- id: ID сообщения
- date: дата публикации
- crypto: криптовалюта, которую предлагали закупать (если есть, иначе null)

Верни только список этих JSON-объектов без каких-либо дополнительных комментариев или форматирования. Твой ответ должен быть валидным JSON-массивом. Без постороннего текста до или после этого JSON-а.

Вот сообщения для анализа:

"""
    for message in batch:
        prompt += f"ID: {message['id']}\nDate: {message['date']}\nMessage: {message['message']}\n\n"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }

    data = {
        'model': 'llama-3.1-70b-versatile',
        'messages': [
            {"role": "system", "content": "You are a helpful assistant that analyzes Telegram messages and extracts information about cryptocurrency purchases."},
            {"role": "user", "content": prompt}
        ],
        'max_tokens': MAX_TOKENS,
        'temperature': 0.2
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        if "rate limit" in str(e).lower():
            print(f"Rate limit reached. Waiting for {RATE_LIMIT_DELAY} seconds before retrying.")
            time.sleep(RATE_LIMIT_DELAY)
        elif "maximum context length" in str(e).lower():
            print(f"Token overflow. Waiting for {TOKEN_OVERFLOW_DELAY} seconds before retrying with a smaller batch.")
            time.sleep(TOKEN_OVERFLOW_DELAY)
        else:
            print(f"Unexpected error: {str(e)}")
        return None

def main():
    all_messages = load_messages()
    processed_messages = []

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            processed_messages = json.load(f)

    start_index = (START_STEP - 1) * BATCH_SIZE
    current_batch_size = BATCH_SIZE

    for i in range(start_index, len(all_messages), current_batch_size):
        batch = all_messages[i:i+current_batch_size]
        current_step = i // BATCH_SIZE + 1
        print(f"Processing batch {current_step}/{len(all_messages)//BATCH_SIZE + 1}")
        
        result = process_batch(batch)
        if result:
            try:
                processed_batch = json.loads(result)
                processed_messages.extend(processed_batch)
                
                save_processed_messages(processed_messages)
                print(f"Processed and saved batch {current_step}")
                
                intermediate_filename = f"intermediate_results_{current_step}.json"
                with open(intermediate_filename, 'w', encoding='utf-8') as f:
                    json.dump(processed_batch, f, ensure_ascii=False, indent=2)
                print(f"Intermediate results saved to {intermediate_filename}")
                
                current_batch_size = BATCH_SIZE
            except json.JSONDecodeError:
                print(f"Error decoding JSON for batch {current_step}")
                print(f"Raw result: {result}")
                
                error_filename = f"error_result_{current_step}.txt"
                with open(error_filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"Error result saved to {error_filename}")
        else:
            print(f"Error processing batch {current_step}. Reducing batch size and retrying.")
            current_batch_size = max(1, current_batch_size // 2)
            i -= current_batch_size  # Повторяем обработку текущего пакета с меньшим размером
        
        time.sleep(5)

    print(f"Processing complete. All results saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()