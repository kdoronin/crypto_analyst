"""
Этот скрипт анализирует инвестиции в криптовалюты на основе обработанных данных.
Он подсчитывает общую сумму инвестиций, сумму инвестиций в подешевевшие криптовалюты и создает распределение инвестиций по криптовалютам.
"""

import csv
from collections import defaultdict

INPUT_FILE = 'crypto_analysis_extended.csv'

def analyze_crypto_investments():
    total_sum = 0
    cheaper_sum = 0
    crypto_investments = defaultdict(float)

    with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            investment = float(row['sum'])
            total_sum += investment
            
            if row['cheaper'].lower() == 'true':
                cheaper_sum += investment
                crypto_investments[row['crypto']] += investment

    print(f"1. Общая сумма инвестиций: ${total_sum:.2f}")
    print(f"2. Сумма инвестиций в подешевевшие криптовалюты: ${cheaper_sum:.2f}")
    print("\n3. Распределение инвестиций по подешевевшим криптовалютам:")
    
    for crypto, amount in sorted(crypto_investments.items(), key=lambda x: x[1], reverse=True):
        print(f"   {crypto}: ${amount:.2f}")

    print(f"\nВсего уникальных криптовалют: {len(crypto_investments)}")

if __name__ == '__main__':
    analyze_crypto_investments()