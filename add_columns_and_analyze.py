"""
Этот скрипт добавляет новые столбцы с расчетами в CSV-файл с данными о криптовалютах и проводит финальный анализ инвестиций.
Он рассчитывает количество купленных монет, их будущую стоимость и общую прибыль/убыток от инвестиций.
"""
import csv
from decimal import Decimal, getcontext
from collections import defaultdict

# Устанавливаем точность для десятичных вычислений
getcontext().prec = 10

INPUT_FILE = 'crypto_analysis_extended.csv'
OUTPUT_FILE = 'crypto_analysis_final.csv'

def process_csv():
    total_coins_bought = Decimal('0')
    total_future_value = Decimal('0')
    rows_removed = 0
    total_investment = Decimal('0')
    cheaper_investment = Decimal('0')
    crypto_investments = defaultdict(Decimal)

    with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['coins_bought', 'future_value']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            price_at_date = Decimal(row['price_at_date'])
            
            if price_at_date == 0:
                rows_removed += 1
                continue

            sum_value = Decimal(row['sum'])
            price_at_future = Decimal(row['price_at_future'])

            coins_bought = sum_value / price_at_date
            future_value = coins_bought * price_at_future

            total_coins_bought += coins_bought
            total_future_value += future_value
            total_investment += sum_value

            if row['cheaper'].lower() == 'true':
                cheaper_investment += sum_value
                crypto_investments[row['crypto']] += sum_value

            row['coins_bought'] = str(coins_bought)
            row['future_value'] = str(future_value)
            writer.writerow(row)

    profit = total_future_value - total_investment
    growth_percentage = (profit / total_investment) * 100 if total_investment != 0 else Decimal('0')

    print(f"Обработка завершена. Результаты сохранены в {OUTPUT_FILE}")
    print(f"Удалено строк с нулевой ценой: {rows_removed}")
    print(f"\nОбщая сумма инвестиций: ${total_investment:.2f}")
    print(f"Сумма инвестиций в подешевевшие криптовалюты: ${cheaper_investment:.2f}")
    print(f"Общее количество купленных монет: {total_coins_bought:.4f}")
    print(f"Общая будущая стоимость: ${total_future_value:.2f}")
    print(f"Прибыль/убыток: ${profit:.2f}")
    print(f"Процент прироста: {growth_percentage:.2f}%")

    print("\nРаспределение инвестиций по подешевевшим криптовалютам:")
    for crypto, amount in sorted(crypto_investments.items(), key=lambda x: x[1], reverse=True):
        print(f"   {crypto}: ${amount:.2f}")

    print(f"\nВсего уникальных подешевевших криптовалют: {len(crypto_investments)}")

if __name__ == '__main__':
    process_csv()