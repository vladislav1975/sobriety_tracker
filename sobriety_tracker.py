from datetime import date, datetime
from calendar import monthrange
import os
import json
from json import JSONDecodeError
from dateutil.relativedelta import relativedelta

FNAME = "sobriety_start_date.json"

# 🌍 Language dictionary
messages = {
    'en': {
        'choose_lang': "Choose language (En/ru - Enter - English): ",
        'invalid_lang': "Language not supported. Defaulting to English.",
        'error_prefix': "❌ Error:",
        'exit_setup': "👋 Exiting setup.",
        'enter_year': "Enter sobriety starting year (or 'q' to quit): ",
        'enter_month': "Month (1–12): ",
        'enter_day': "Day (1–{max_d}): ",
        'invalid_input': "Invalid input. Please enter a valid number.",
        'range_error': "Please enter a number between {min_val} and {max_val}.",
        'future_date': "Date is in the future.",
        'date_saved': "✅ Date saved: {date_str}",
        'saved_date': "📅 Saved date: {date_str}",
        'corrupted_file': "Corrupted file. Creating new...",
        'no_saved_date': "📂 No saved date found.",
        'days_sober': "\n🎉 You've been sober for {days} day(s), which is:",
        'duration': "   🗓️ {years} year(s), {months} month(s), {days} day(s)"
    },
    'ru': {
        'choose_lang': "Выберите язык (en/ru): ",
        'invalid_lang': "Язык не поддерживается. Используется английский.",
        'error_prefix': "❌ Ошибка:",
        'exit_setup': "👋 Выход из настройки.",
        'enter_year': "Введите год начала трезвости (или 'q' для выхода): ",
        'enter_month': "Месяц (1–12): ",
        'enter_day': "День (1–{max_d}): ",
        'invalid_input': "Неверный ввод. Пожалуйста, введите число.",
        'range_error': "Введите число от {min_val} до {max_val}.",
        'future_date': "Дата в будущем.",
        'date_saved': "✅ Дата сохранена: {date_str}",
        'saved_date': "📅 Сохраненная дата: {date_str}",
        'corrupted_file': "Файл поврежден. Создание нового...",
        'no_saved_date': "📂 Сохраненная дата не найдена.",
        'days_sober': "\n🎉 Вы трезвы уже {days} дн., что составляет:",
        'duration': "   🗓️ {years} лет, {months} мес., {days} дн."
    }
}

# 🌐 Language selection
def choose_language():
    lang = input(messages['en']['choose_lang']).strip().lower()
    if not lang:
        lang = 'en'
    elif lang not in messages:
        print(messages['en']['invalid_lang'])
        lang = 'en'
    return lang


# 🛑 Error display
def error(msg, lang):
    print(f"{messages[lang]['error_prefix']} {msg}")

# 🔢 Valid integer input
def get_valid_int(prompt, lang, min_val=None, max_val=None):
    while True:
        response = input(prompt)
        if response.lower() == 'q':
            print(messages[lang]['exit_setup'])
            return None
        try:
            value = int(response)
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print(messages[lang]['range_error'].format(min_val=min_val, max_val=max_val))
                continue
            return value
        except ValueError:
            print(messages[lang]['invalid_input'])

# 📂 Read saved date
def read_saved_date(lang):
    if os.path.exists(FNAME):
        try:
            with open(FNAME, 'r') as file:
                content = json.load(file)
                saved_date = datetime.strptime(content, '%Y-%m-%d').date()
                print(messages[lang]['saved_date'].format(date_str=saved_date.strftime('%A %d %B %Y')))
                return saved_date
        except (ValueError, JSONDecodeError):
            error(messages[lang]['corrupted_file'], lang)
            os.remove(FNAME)
    else:
        print(messages[lang]['no_saved_date'])
    return None

# 📅 Prompt for new date
def prompt_for_date(lang):
    while True:
        y = get_valid_int(messages[lang]['enter_year'], lang, 1900, date.today().year)
        if y is None:
            return None

        m = get_valid_int(messages[lang]['enter_month'], lang, 1, 12)
        if m is None:
            return None

        max_d = monthrange(y, m)[1]
        d = get_valid_int(messages[lang]['enter_day'].format(max_d=max_d), lang, 1, max_d)
        if d is None:
            return None

        start_date = date(y, m, d)
        if start_date > date.today():
            error(messages[lang]['future_date'], lang)
            continue

        with open(FNAME, 'w') as file:
            json.dump(start_date.strftime('%Y-%m-%d'), file)
        print(messages[lang]['date_saved'].format(date_str=start_date.strftime('%A %d %B %Y')))
        return start_date

# 🚀 Main logic
def main():
    lang = choose_language()
    start_date = read_saved_date(lang)
    if not start_date:
        start_date = prompt_for_date(lang)

    if start_date:
        today = date.today()
        days_sober = (today - start_date).days
        delta = relativedelta(today, start_date)

        print(messages[lang]['days_sober'].format(days=days_sober))
        print(messages[lang]['duration'].format(
            years=delta.years,
            months=delta.months,
            days=delta.days
        ))

if __name__ == '__main__':
    main()
