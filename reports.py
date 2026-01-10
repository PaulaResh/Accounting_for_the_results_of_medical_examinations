'''
Модуль для генерации отчетов.
Содержит  функции для создания всех требуемых отчетов.
'''

from sort import sort_by_health_then_name, sort_by_birth_date, sort_by_group_then_name
from sort import sort_by_health_group_name, sort_by_name_only
from utils import print_records_table


def generate_full_report(records):
    '''
    Генерирует полный отчет, отсортированный по количеству здоровых заключений.

    Args:
        records (list): Список всех записей
    '''
    if not records:
        print('Нет данных для отчета')
        input('\nНажмите Enter для продолжения...')
        return

    print('\n' + '=' * 80)
    print('ПОЛНЫЙ ОТЧЕТ (сортировка по здоровым заключениям)'.center(80))
    print('=' * 80)

    # Сортировка с использованием кешированных значений
    sorted_records = sort_by_health_then_name(records)

    # Вывод таблицы
    print_records_table(sorted_records)

    # Статистика - используем предвычисленные значения
    print('\n' + '=' * 80)
    print('СТАТИСТИКА:')
    total = len(sorted_records)

    # Одним проходом вычисляем все статистики
    healthy_all = 0
    need_treatment_count = 0
    healthy_distribution = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

    for record in sorted_records:
        healthy = record.get('_healthy_count', 0)
        healthy_distribution[healthy] += 1

        if healthy == 4:
            healthy_all += 1

        if record.get('_needs_treatment', False):
            need_treatment_count += 1

    print(f'Всего детей: {total}')
    if total > 0:
        print(f'Абсолютно здоровых (4/4): {healthy_all} ({healthy_all / total * 100:.1f}%)')
        print(f'Нуждающихся в лечении: {need_treatment_count} ({need_treatment_count / total * 100:.1f}%)')

        # Распределение по количеству здоровых заключений
        print('\nРаспределение по количеству здоровых заключений:')
        for i in range(5):
            count = healthy_distribution[i]
            print(f'  {i} здоровых: {count} детей ({count / total * 100:.1f}%)')

    input('\nНажмите Enter для продолжения...')


def generate_group_report(records):
    '''
    Генерирует отчет по заданной группе, отсортированный по дате рождения.

    Args:
        records (list): Список всех записей
    '''
    if not records:
        print('Нет данных для отчета')
        input('\nНажмите Enter для продолжения...')
        return

    print('\nВыберите группу:')
    print('1. Младшая')
    print('2. Средняя')
    print('3. Старшая')
    print('4. Все группы')

    group_map = {
        '1': 'младшая',
        '2': 'средняя',
        '3': 'старшая',
        '4': 'все'
    }

    while True:
        choice = input('Ваш выбор (1-4): ').strip()
        if choice in group_map:
            selected_group = group_map[choice]
            break
        print('Ошибка: выберите 1, 2, 3 или 4')

    # Быстрая фильтрация по группе
    if selected_group == 'все':
        group_records = records
        title = 'ОТЧЕТ ПО ВСЕМ ГРУППАМ (сортировка по дате рождения)'
    else:
        group_records = [r for r in records if r['группа'].lower() == selected_group]
        title = f'ОТЧЕТ ПО {selected_group.upper()} ГРУППЕ (сортировка по дате рождения)'

    if not group_records:
        print(f'\nНет данных для группы "{selected_group}"')
        input('\nНажмите Enter для продолжения...')
        return

    # Сортировка по дате рождения
    sorted_records = sort_by_birth_date(group_records)

    print('\n' + '=' * 80)
    print(title.center(80))
    print('=' * 80)

    print_records_table(sorted_records)

    # Статистика по группе
    print('\n' + '=' * 80)
    print(f'СТАТИСТИКА ПО ГРУППЕ "{selected_group}":')
    total = len(group_records)
    print(f'Всего детей в группе: {total}')

    if total > 0:
        # Самый младший и самый старший
        youngest = sorted_records[0]
        oldest = sorted_records[-1]
        print(f'Самый младший: {youngest["фамилия"]} {youngest["имя"]} ({youngest["дата_рождения"]})')
        print(f'Самый старший: {oldest["фамилия"]} {oldest["имя"]} ({oldest["дата_рождения"]})')

        # Распределение по годам рождения
        years = {}
        for record in group_records:
            year = record['дата_рождения'].split('-')[0]
            years[year] = years.get(year, 0) + 1

        print('\nРаспределение по годам рождения:')
        for year in sorted(years.keys()):
            print(f'  {year} год: {years[year]} детей')

    input('\nНажмите Enter для продолжения...')


def generate_treatment_report(records):
    '''
    Генерирует отчет по детям, нуждающимся в лечении.

    Args:
        records (list): Список всех записей
    '''
    if not records:
        print('Нет данных для отчета')
        input('\nНажмите Enter для продолжения...')
        return

    print('\n' + '=' * 80)
    print('ДЕТИ, НУЖДАЮЩИЕСЯ В ЛЕЧЕНИИ'.center(80))
    print('=' * 80)

    # Фильтрация нуждающихся в лечении с использованием предвычисленных значений
    treatment_records = [r for r in records if r.get('_needs_treatment', False)]

    if not treatment_records:
        print('\nНет детей, нуждающихся в лечении!')
        input('\nНажмите Enter для продолжения...')
        return

    # Сортировка по группе и фамилии
    sorted_records = sort_by_health_group_name(treatment_records)

    print_records_table(sorted_records)

    # Подробная информация - используем предвычисленные данные
    print('\n' + '=' * 80)
    print('ПОДРОБНАЯ ИНФОРМАЦИЯ:')

    for i, record in enumerate(sorted_records, 1):
        print(f'\n{i}. {record["фамилия"]} {record["имя"]} ({record["группа"]})')

        needs_specialists = record.get('_needs_specialists', [])
        if needs_specialists:
            print(f'   Требуется лечение у: {", ".join(needs_specialists)}')

    # Статистика по группам
    print('\n' + '=' * 80)
    print('СТАТИСТИКА ПО ГРУППАМ:')

    # Одним проходом вычисляем статистику по группам
    group_stats = {}
    total_by_group = {}

    for record in records:
        group = record['группа']
        total_by_group[group] = total_by_group.get(group, 0) + 1
        if record.get('_needs_treatment', False):
            group_stats[group] = group_stats.get(group, 0) + 1

    for group in ['младшая', 'средняя', 'старшая']:
        count = group_stats.get(group, 0)
        total_in_group = total_by_group.get(group, 0)
        if total_in_group > 0:
            percentage = (count / total_in_group) * 100
            print(f'  {group.capitalize()}: {count} из {total_in_group} ({percentage:.1f}%)')
        else:
            print(f'  {group.capitalize()}: 0 детей в группе')

    input('\nНажмите Enter для продолжения...')


def show_statistics(records):
    '''
    Показывает общую статистику по всем данным.

    Args:
        records (list): Список всех записей
    '''
    if not records:
        print('Нет данных для статистики')
        input('\nНажмите Enter для продолжения...')
        return

    print('\n' + '=' * 80)
    print('ОБЩАЯ СТАТИСТИКА ДЕТСКОГО САДА'.center(80))
    print('=' * 80)

    total = len(records)

    # Одним проходом вычисляем все статистики
    groups_stats = {'младшая': 0, 'средняя': 0, 'старшая': 0}
    healthy_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    need_treatment_count = 0
    specialist_counts = {
        'невропатолог': 0,
        'отоларинголог': 0,
        'ортопед': 0,
        'окулист': 0
    }

    for record in records:
        # Группа
        group = record['группа'].lower()
        if group in groups_stats:
            groups_stats[group] += 1

        # Здоровые заключения
        healthy = record.get('_healthy_count', 0)
        healthy_counts[healthy] += 1

        # Нуждается в лечении
        if record.get('_needs_treatment', False):
            need_treatment_count += 1

        # Специалисты
        for spec in ['невропатолог', 'отоларинголог', 'ортопед', 'окулист']:
            if record.get(spec, '').lower() == 'нуждается в лечении':
                specialist_counts[spec] += 1

    print(f'\nВсего детей: {total}')

    # Распределение по группам
    print('\nРаспределение по группам:')
    for group in ['младшая', 'средняя', 'старшая']:
        count = groups_stats[group]
        if total > 0:
            percentage = (count / total) * 100
            print(f'  {group.capitalize()}: {count} детей ({percentage:.1f}%)')

    # Распределение по здоровью
    print('\nРаспределение по состоянию здоровья:')
    for i in range(5):
        count = healthy_counts[i]
        if total > 0:
            percentage = (count / total) * 100
            print(f'  {i} здоровых заключений: {count} детей ({percentage:.1f}%)')

    # Дети, нуждающиеся в лечении
    if total > 0:
        print(f'\nНуждаются в лечении: {need_treatment_count} детей ({(need_treatment_count / total) * 100:.1f}%)')

        # По специалистам
        print('\nКоличество детей, нуждающихся в лечении по специалистам:')
        for spec in ['невропатолог', 'отоларинголог', 'ортопед', 'окулист']:
            count = specialist_counts[spec]
            print(f'  {spec.capitalize()}: {count} детей ({(count / total) * 100:.1f}%)')

    input('\nНажмите Enter для продолжения...')