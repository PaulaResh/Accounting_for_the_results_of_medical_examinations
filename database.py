'''
Модуль для работы с базой данных.
Обеспечивает чтение, запись, добавление и редактирование записей.
'''

from utils import validate_date, validate_group, validate_conclusion, parse_date


def validate_group_by_birth_year(birth_date, group):
    '''
    Проверяет соответствие года рождения и группы.

    Args:
        birth_date (str): Дата рождения в формате ГГГГ-ММ-ДД
        group (str): Название группы

    Returns:
        tuple: (bool, str) - успешность проверки и сообщение об ошибке
    '''
    try:
        year, month, day = parse_date(birth_date)

        group_years = {
            'младшая': [2022, 2023],
            'средняя': [2020, 2021],
            'старшая': [2018, 2019]
        }

        if group not in group_years:
            return False, f'Неизвестная группа: {group}'

        if year not in group_years[group]:
            expected_years = group_years[group]
            return False, f'Ребенок {year} года рождения не может быть в {group} группе'

        return True, ''

    except Exception as e:
        return False, f'Ошибка при проверке соответствия группы и года рождения: {e}'


def load_database(filename='data.txt'):
    '''
    Загружает данные из файла.

    Args:
        filename (str): Имя файла с данными

    Returns:
        tuple: (список записей, сообщение об ошибке)
    '''
    records = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return records, f'Файл {filename} не найден'
    except Exception as e:
        return records, f'Ошибка при чтении файла: {e}'

    current_record = {}
    valid_records = 0

    for line in lines:
        line = line.strip()

        if not line:
            if current_record:
                required = ['фамилия', 'имя', 'дата_рождения', 'группа']
                if all(field in current_record for field in required):
                    birth_date = current_record['дата_рождения']
                    group = current_record['группа']
                    is_valid, error_msg = validate_group_by_birth_year(birth_date, group)
                    if is_valid:
                        records.append(current_record)
                        valid_records += 1
                current_record = {}
            continue

        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            current_record[key] = value

    if current_record:
        required = ['фамилия', 'имя', 'дата_рождения', 'группа']
        if all(field in current_record for field in required):
            birth_date = current_record['дата_рождения']
            group = current_record['группа']
            is_valid, error_msg = validate_group_by_birth_year(birth_date, group)
            if is_valid:
                records.append(current_record)
                valid_records += 1

    return records, f'Загружено {valid_records} записей'


def save_database(records, filename='data.txt'):
    '''
    Сохраняет данные в файл.

    Args:
        records (list): Список записей
        filename (str): Имя файла для сохранения

    Returns:
        str: Сообщение о результате
    '''
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for record in records:
                file.write(f'фамилия: {record["фамилия"]}\n')
                file.write(f'имя: {record["имя"]}\n')
                file.write(f'дата_рождения: {record["дата_рождения"]}\n')
                file.write(f'группа: {record["группа"]}\n')

                specialists = ['невропатолог', 'отоларинголог', 'ортопед', 'окулист']
                for specialist in specialists:
                    if specialist in record:
                        file.write(f'{specialist}: {record[specialist]}\n')

                file.write('\n')

        return f'Данные сохранены в файл {filename}'

    except Exception as e:
        return f'Ошибка при сохранении: {e}'


def add_record(records):
    '''
    Добавляет новую запись о ребенке.

    Args:
        records (list): Текущий список записей

    Returns:
        tuple: (обновленный список, сообщение)
    '''
    print('\n' + '=' * 60)
    print('ДОБАВЛЕНИЕ НОВОЙ ЗАПИСИ')
    print('=' * 60)

    new_record = {}

    # Фамилия
    while True:
        last_name = input('Фамилия: ').strip()
        if last_name:
            new_record['фамилия'] = last_name
            break
        print('Ошибка: фамилия не может быть пустой')

    # Имя
    while True:
        first_name = input('Имя: ').strip()
        if first_name:
            new_record['имя'] = first_name
            break
        print('Ошибка: имя не может быть пустой')

    # Дата рождения и группа
    while True:
        birth_date = input('Дата рождения (ГГГГ-ММ-ДД): ').strip()
        is_valid_date, error_msg_date = validate_date(birth_date)
        if not is_valid_date:
            print(f'Ошибка: {error_msg_date}')
            continue

        year, month, day = parse_date(birth_date)
        year = int(year)

        available_groups = []
        if year in [2022, 2023]:
            available_groups.append('младшая')
        if year in [2020, 2021]:
            available_groups.append('средняя')
        if year in [2018, 2019]:
            available_groups.append('старшая')

        if not available_groups:
            print(f'Ошибка: ребенок {year} года рождения не подходит ни для одной группы')
            continue

        print(f'Доступные группы для {year} года рождения: {", ".join(available_groups)}')
        group = input(f'Группа ({"/".join(available_groups)}): ').strip().lower()

        if not validate_group(group):
            print('Ошибка: группа должна быть "младшая", "средняя" или "старшая"')
            continue

        is_valid_group, error_msg_group = validate_group_by_birth_year(birth_date, group)
        if not is_valid_group:
            print(f'Ошибка: {error_msg_group}')
            continue

        new_record['дата_рождения'] = birth_date
        new_record['группа'] = group
        break

    # Заключения специалистов
    print('\nЗаключения специалистов (оставьте пустым если нет данных):')
    specialists = {
        'невропатолог': 'невропатолога',
        'отоларинголог': 'отоларинголога',
        'ортопед': 'ортопеда',
        'окулист': 'окулиста'
    }

    for key, name in specialists.items():
        while True:
            conclusion = input(f'Заключение {name} (здоров/нуждается в лечении): ').strip()
            if not conclusion:
                break

            if validate_conclusion(conclusion):
                new_record[key] = conclusion
                break
            print('Ошибка: заключение должно быть "здоров" или "нуждается в лечении"')

    records.append(new_record)
    return records, 'Запись успешно добавлена'


def edit_record(records):
    '''
    Редактирует существующую запись.

    Args:
        records (list): Текущий список записей

    Returns:
        tuple: (обновленный список, сообщение)
    '''
    if not records:
        return records, 'Нет записей для редактирования'

    print('\nСПИСОК ЗАПИСЕЙ:')
    for i, record in enumerate(records, 1):
        print(f'{i}. {record["фамилия"]} {record["имя"]} - {record["группа"]}')

    while True:
        try:
            choice = input('\nВведите номер записи для редактирования (0 для отмены): ').strip()
            if choice == '0':
                return records, 'Редактирование отменено'

            index = int(choice) - 1
            if 0 <= index < len(records):
                record = records[index]
                from utils import print_record
                print_record(record, index + 1)

                print('\nКакое поле изменить?')
                print('1. Фамилия')
                print('2. Имя')
                print('3. Дата рождения')
                print('4. Группа')
                print('5. Заключение невропатолога')
                print('6. Заключение отоларинголога')
                print('7. Заключение ортопеда')
                print('8. Заключение окулиста')
                print('0. Отмена')

                field_choice = input('Ваш выбор: ').strip()

                if field_choice == '1':
                    new_value = input('Новая фамилия: ').strip()
                    if new_value:
                        record['фамилия'] = new_value
                    return records, 'Фамилия изменена'

                elif field_choice == '2':
                    new_value = input('Новое имя: ').strip()
                    if new_value:
                        record['имя'] = new_value
                    return records, 'Имя изменено'

                elif field_choice == '3':
                    current_group = record['группа']
                    new_birth_date = input('Новая дата рождения (ГГГГ-ММ-ДД): ').strip()

                    is_valid_date, error_msg_date = validate_date(new_birth_date)
                    if not is_valid_date:
                        return records, f'Ошибка: {error_msg_date}'

                    is_valid_group, error_msg_group = validate_group_by_birth_year(new_birth_date, current_group)
                    if not is_valid_group:
                        return records, f'Ошибка: {error_msg_group}'

                    record['дата_рождения'] = new_birth_date
                    return records, 'Дата рождения изменена'

                elif field_choice == '4':
                    current_birth_date = record['дата_рождения']
                    new_group = input('Новая группа (младшая/средняя/старшая): ').strip().lower()

                    if not validate_group(new_group):
                        return records, 'Ошибка: неверное название группы'

                    is_valid, error_msg = validate_group_by_birth_year(current_birth_date, new_group)
                    if not is_valid:
                        return records, f'Ошибка: {error_msg}'

                    record['группа'] = new_group
                    return records, 'Группа изменена'

                elif field_choice in ['5', '6', '7', '8']:
                    specialist_map = {
                        '5': 'невропатолог',
                        '6': 'отоларинголог',
                        '7': 'ортопед',
                        '8': 'окулист'
                    }
                    specialist = specialist_map[field_choice]
                    new_value = input(f'Новое заключение {specialist} (здоров/нуждается в лечении): ').strip()

                    if not new_value:
                        if specialist in record:
                            del record[specialist]
                        return records, f'Заключение {specialist} удалено'
                    elif validate_conclusion(new_value):
                        record[specialist] = new_value
                        return records, f'Заключение {specialist} изменено'
                    else:
                        return records, 'Ошибка: неверное заключение'

                elif field_choice == '0':
                    return records, 'Редактирование отменено'

                else:
                    return records, 'Неверный выбор поля'

            else:
                print('Ошибка: неверный номер записи')
                continue

        except ValueError:
            print('Ошибка: введите число')
            continue
        except Exception as e:
            return records, f'Ошибка при редактировании: {e}'


def delete_record(records):
    '''
    Удаляет запись о ребенке.

    Args:
        records (list): Текущий список записей

    Returns:
        tuple: (обновленный список, сообщение)
    '''
    if not records:
        return records, 'Нет записей для удаления'

    print('\nСПИСОК ЗАПИСЕЙ:')
    for i, record in enumerate(records, 1):
        print(f'{i}. {record["фамилия"]} {record["имя"]} - {record["группа"]}')

    while True:
        try:
            choice = input('\nВведите номер записи для удаления (0 для отмены): ').strip()
            if choice == '0':
                return records, 'Удаление отменено'

            index = int(choice) - 1
            if 0 <= index < len(records):
                record = records.pop(index)
                return records, f'Запись {record["фамилия"]} {record["имя"]} удалена'
            else:
                print('Ошибка: неверный номер записи')
                continue

        except ValueError:
            print('Ошибка: введите число')
            continue
        except Exception as e:
            return records, f'Ошибка при удаления: {e}'
