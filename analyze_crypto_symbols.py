"""
Этот скрипт анализирует символы криптовалют в обработанных данных.
Он проверяет, соответствуют ли символы криптовалют стандартному формату (2-6 заглавных букв) и выводит список несоответствующих символов.
"""

import json
import re

# Константа
INPUT_FILE = 'processed_messages_hand.json'

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_valid_crypto_symbol(symbol):
    # Проверяем, что символ состоит из 2-4 заглавных латинских букв
    return bool(re.match(r'^[A-Z]{2,6}$', symbol))

def analyze_crypto_symbols():
    messages = load_json(INPUT_FILE)
    invalid_symbols = []

    for message in messages:
        crypto = message.get('crypto')
        if crypto and not is_valid_crypto_symbol(crypto):
            invalid_symbols.append(crypto)

    if invalid_symbols:
        print("Найдены следующие некорректные значения crypto:")
        for symbol in sorted(set(invalid_symbols)):
            print(f"- {symbol}")
    else:
        print("Все значения crypto соответствуют правилам написания котировочного символа.")

    print(f"Всего проанализировано сообщений: {len(messages)}")
    print(f"Количество некорректных значений: {len(invalid_symbols)}")

if __name__ == '__main__':
    analyze_crypto_symbols()