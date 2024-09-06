import os

def get_script_info(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        description = content.split('"""')[1] if '"""' in content else "Описание отсутствует."
        functions = [line.split('def ')[1].split('(')[0] for line in content.split('\n') if line.startswith('def ')]
    return description.strip(), functions

def create_readme():
    scripts = [f for f in os.listdir('.') if f.endswith('.py') and f != 'readme_maker.py']
    
    with open('README.md', 'w', encoding='utf-8') as readme:
        readme.write("# Анализ криптовалютных инвестиций\n\n")
        readme.write("Этот проект состоит из нескольких Python-скриптов, предназначенных для сбора, обработки и анализа данных о криптовалютных инвестициях из Telegram-канала.\n\n")
        readme.write("## Скрипты\n\n")

        for script in scripts:
            description, functions = get_script_info(script)
            readme.write(f"### {script}\n\n")
            readme.write(f"{description}\n\n")
            readme.write("**Основные функции:**\n")
            for func in functions:
                readme.write(f"- `{func}()`\n")
            readme.write(f"\n**Использование:**\n```\npython {script}\n```\n\n")

        readme.write("## Порядок использования скриптов\n\n")
        correct_order = [
            "telegram_parser_unofficial.py",
            "process_messages.py",
            "process_error_results.py",
            "remove_null_crypto.py",
            "analyze_crypto_symbols.py",
            "process_crypto_data.py",
            "extend_crypto_analysis.py",
            "analyze_crypto_investments.py",
            "add_columns_and_analyze.py"
        ]
        for i, script in enumerate(correct_order, 1):
            readme.write(f"{i}. Запустите `{script}`\n")
        
        readme.write("\n## Зависимости\n\n")
        readme.write("Убедитесь, что у вас установлены следующие библиотеки Python:\n")
        readme.write("- requests\n- beautifulsoup4\n- csv\n- json\n- datetime\n\n")
        readme.write("Вы можете установить их с помощью pip:\n")
        readme.write("```\npip install requests beautifulsoup4\n```\n\n")
        
        readme.write("## Примечание\n\n")
        readme.write("Перед использованием скриптов убедитесь, что у вас есть необходимые API-ключи и права доступа к данным. Соблюдайте условия использования API и правила работы с данными.\n")

if __name__ == "__main__":
    create_readme()
    print("README.md успешно создан.")