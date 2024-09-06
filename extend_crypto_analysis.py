"""
Этот скрипт расширяет анализ криптовалют, добавляя информацию о текущей рыночной капитализации.
Он использует API CryptoCompare для получения данных о капитализации и добавляет эту информацию в CSV-файл с результатами анализа.
"""

import csv
import requests
import time
from datetime import datetime

INPUT_FILE = 'crypto_analysis.csv'
OUTPUT_FILE = 'crypto_analysis_extended.csv'
CRYPTOCOMPARE_API_KEY = ''
CRYPTOCOMPARE_API_URL = 'https://min-api.cryptocompare.com/data/pricemultifull'

def get_current_market_cap(symbol):
    params = {
        'fsyms': symbol,
        'tsyms': 'USD',
        'api_key': CRYPTOCOMPARE_API_KEY
    }
    try:
        response = requests.get(CRYPTOCOMPARE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if 'RAW' in data and symbol in data['RAW'] and 'USD' in data['RAW'][symbol]:
            market_cap = data['RAW'][symbol]['USD']['MKTCAP']
            print(f"Successfully got market cap for {symbol}: ${market_cap:,.2f}")
            return market_cap
        else:
            print(f"Error getting market cap for {symbol}: Data not found in response")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting market cap for {symbol}: {e}")
        return None

def process_csv():
    with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['current_market_cap']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        total_rows = sum(1 for row in infile) - 1  # Subtract 1 for header
        infile.seek(0)
        next(reader)  # Skip header

        for index, row in enumerate(reader, 1):
            print(f"Processing row {index}/{total_rows} - Crypto: {row['crypto']}")
            market_cap = get_current_market_cap(row['crypto'])
            row['current_market_cap'] = market_cap
            writer.writerow(row)
            time.sleep(0.25)  # Небольшая задержка между запросами

    print(f"Processing complete. Results saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    process_csv()