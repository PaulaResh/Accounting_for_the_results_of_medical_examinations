'''
Вспомогательные модули для работы программы.
Содержит функции валидации, форматирования и отображения данных.
'''


def validate_date(date_str):
    '''
    Проверяет корректность даты в формате ГГГГ-ММ-ДД.

    Args:
        date_str (str): Строка с датой

    Returns:
        tuple: (bool, str) - успешность проверки и сообщение об ошибке
    '''
    try:
        parts = date_str.split('-')
        if len(parts) != 3:
            return False, 'Дата должна быть в формате ГГГГ-ММ-ДД'

        year, month, day = parts
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return False, 'Год, месяц и день должны быть числами'

        year_int, month_int, day_int = int(year), int(month), int(day)

        if not (2010 <= year_int <= 2020):
            return False, 'Год рождения должен быть между 2010 и 2020'
        if not (1 <= month_int <= 12):
            return False, 'Месяц должен быть от 1 до 12'
        if not (1 <= day_int <= 31):
            return False, 'День должен быть от 1 до 31'

        if month_int == 2 and day_int > 29:
            return False, 'В феврале не может быть больше 29 дней'

        if month_int in [4, 6, 9, 11] and day_int > 30:
            return False, f'В месяце {month_int} не может быть больше 30 дней'

        return True, ''

    except Exception as e:
        return False, f'Ошибка при проверке даты: {e}'


def validate_group(group):
    '''
    Проверяет корректность названия группы.

    Args:
        group (str): Название группы

    Returns:
        bool: True если группа корректна
    '''
    return group.lower() in ['младшая', 'средняя', 'старшая']


def validate_conclusion(conclusion):
    '''
    Проверяет корректность заключения специалиста.

    Args:
        conclusion (str): Заключение

    Returns:
        bool: True если заключение корректно
    '''
    return conclusion.lower() in ['здоров', 'нуждается в лечении']


def parse_date(date_str):
    '''
    Разбирает строку с датой на составляющие.

    Args:
        date_str (str): Дата в формате ГГГГ-ММ-ДД

    Returns:
        tuple: (год, месяц, день) как целые числа
    '''
    parts = date_str.split('-')
    return int(parts[0]), int(parts[1]), int(parts[2])


def count_healthy_specialists(record):
    '''
    Подсчитывает количество специалистов, давших заключение 'здоров'.

    Args:
        record (dict): Запись о ребенке

    Returns:
        int: Количество здоровых заключений (0-4)
    '''
    specialists = ['невропатолог', 'отоларинголог', 'ортопед', 'окулист']
    count = 0
    for specialist in specialists:
        if record.get(specialist, '').lower() == 'здоров':
            count += 1
    return count


def needs_treatment(record):
    '''
    Проверяет, нуждается ли ребенок в лечении.

    Args:
        record (dict): Запись о ребенке

    Returns:
        bool: True если нуждается в лечении хотя бы по одному специалисту
    '''
    specialists = ['невропатолог', 'отоларинголог', 'ортопед', 'окулист']
    for specialist in specialists:
        if record.get(specialist, '').lower() == 'нуждается в лечении':
            return True
    return False


def print_record(record, index=None):
    '''
    Выводит запись о ребенке в удобочитаемом формате.

    Args:
        record (dict): Запись о ребенке
        index (int, optional): Номер записи
    '''
    if index is not None:
        print('\n' + '=' * 60)
        print(f'ЗАПИСЬ #{index}')
        print('=' * 60)

    print(f'Фамилия: {record["фамилия"]}')
    print(f'Имя: {record["имя"]}')
    print(f'Дата рождения: {record["дата_рождения"]}')
    print(f'Группа: {record["группа"]}')
    print('\nЗаключения специалистов:')
    print(f'  Невропатолог: {record.get("невропатолог", "НЕТ ДАННЫХ")}')
    print(f'  Отоларинголог: {record.get("отоларинголог", "НЕТ ДАННЫХ")}')
    print(f'  Ортопед: {record.get("ортопед", "НЕТ ДАННЫХ")}')
    print(f'  Окулист: {record.get("окулист", "НЕТ ДАННЫХ")}')

    healthy_count = count_healthy_specialists(record)
    print(f'\nЗдоровых заключений: {healthy_count}/4')
    if needs_treatment(record):
        print('СТАТУС: Требуется лечение')
    else:
        print('СТАТУС: Здоров')


def print_records_table(records, title=''):
    '''
    Выводит список записей в виде таблицы.

    Args:
        records (list): Список записей
        title (str): Заголовок таблицы
    '''
    if title:
        print('\n' + '=' * 80)
        print(f'{title:^80}')
        print('=' * 80)

    if not records:
        print('Нет данных для отображения')
        return

    # Заголовок таблицы
    header = '№   Фамилия           Имя               Группа     Дата рожд.  Здор./Всего'
    print(header)
    print('-' * 80)

    for i, record in enumerate(records, 1):
        healthy = count_healthy_specialists(record)
        needs_treat = 'ЛЕЧ' if needs_treatment(record) else '   '
        print(f'{i:<3} {record["фамилия"]:<17} {record["имя"]:<16} '
              f'{record["группа"]:<10} {record["дата_рождения"]:<11} '
              f'{healthy:>2}/4 {needs_treat}')


def clear_screen():
    '''
    Очищает экран консоли.
    '''
    print('\n' * 50)
