"""
Этот скрипт получает исторические данные о ценах криптовалют с использованием API CryptoCompare.
Он обрабатывает данные о криптовалютах, получает цены на указанные даты и сохраняет результаты в CSV-файл.
"""
import json
import csv
from datetime import datetime, date
import requests
import time

INPUT_FILE = 'processed_messages_hand.json'
OUTPUT_FILE = 'crypto_analysis.csv'
CRYPTOCOMPARE_API_KEY = ''  # Замените на ваш ключ API
CRYPTOCOMPARE_API_URL = 'https://min-api.cryptocompare.com/data/v2/histoday'
FUTURE_DATE = date(2024, 9, 5)

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_crypto_price(symbol, date):
    # Преобразуем date в datetime
    datetime_obj = datetime.combine(date, datetime.min.time())
    params = {
        'fsym': symbol,
        'tsym': 'USD',
        'limit': 1,
        'toTs': int(datetime_obj.timestamp()),
        'api_key': CRYPTOCOMPARE_API_KEY
    }
    try:
        response = requests.get(CRYPTOCOMPARE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data['Response'] == 'Success':
            price = data['Data']['Data'][0]['close']
            print(f"Successfully got price for {symbol} on {date.strftime('%Y-%m-%d')}: ${price}")
            return price
        else:
            print(f"Error getting price for {symbol}: {data['Message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

def extract_date(date_string):
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00')).date()
    except ValueError:
        print(f"Invalid date format: {date_string}")
        return None

def process_crypto_data():
    messages = load_json(INPUT_FILE)
    results = []
    total_messages = len(messages)

    print(f"Starting to process {total_messages} messages")

    for index, message in enumerate(messages, 1):
        crypto = message.get('crypto')
        if not crypto:
            print(f"Skipping message {index}/{total_messages} - No crypto specified")
            continue

        print(f"Processing message {index}/{total_messages} - Crypto: {crypto}")

        message_date = extract_date(message['date'])
        if not message_date:
            print(f"Skipping message {index}/{total_messages} - Invalid date format")
            continue

        price_at_date = get_crypto_price(crypto, message_date)
        price_at_future = get_crypto_price(crypto, FUTURE_DATE)

        if price_at_date is None or price_at_future is None:
            print(f"Could not get prices for {crypto}")
            continue

        results.append({
            'id': message['id'],
            'date': message['date'],
            'crypto': crypto,
            'price_at_date': price_at_date,
            'price_at_future': price_at_future,
            'sum': 10,
            'cheaper': price_at_future < price_at_date
        })

        print(f"Successfully processed {crypto}. Price at date: ${price_at_date}, Price at future: ${price_at_future}")

        time.sleep(0.25)  # Небольшая задержка между запросами

    print(f"Processing complete. Writing results to {OUTPUT_FILE}")

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'date', 'crypto', 'price_at_date', 'price_at_future', 'sum', 'cheaper']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Results successfully saved to {OUTPUT_FILE}")
    print(f"Total processed: {len(results)} out of {total_messages} messages")

if __name__ == '__main__':
    process_crypto_data()