'''
Модуль для генерации отчетов.
Содержит функции для создания всех требуемых отчетов.
'''

from sort import sort_by_health_then_name, sort_by_birth_date, sort_by_group_then_name
from sort import sort_by_health_group_name
from utils import needs_treatment, print_records_table, count_healthy_specialists


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

    sorted_records = sort_by_health_then_name(records)

    print_records_table(sorted_records, 'ПОЛНЫЙ ОТЧЕТ (сортировка по здоровым заключениям)')

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

    sorted_records = sort_by_birth_date(group_records)

    print_records_table(sorted_records, title)

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

    treatment_records = [r for r in records if needs_treatment(r)]

    if not treatment_records:
        print('\nНет детей, нуждающихся в лечении!')
        input('\nНажмите Enter для продолжения...')
        return

    sorted_records = sort_by_health_group_name(treatment_records)

    print_records_table(sorted_records, 'ДЕТИ, НУЖДАЮЩИЕСЯ В ЛЕЧЕНИИ')

    input('\nНажмите Enter для продолжения...')
