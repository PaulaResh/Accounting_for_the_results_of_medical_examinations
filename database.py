'''
Модуль для работы с базой данных.
Обеспечивает чтение, запись, добавление и редактирование записей.
'''

from utils import validate_date, validate_group, validate_conclusion, parse_date
from utils import process_records_batch


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
        # Быстрый парсинг только года
        year_str = birth_date.split('-')[0]
        if not year_str.isdigit():
            return False, 'Год рождения должен быть числом'

        year = int(year_str)

        # Определяем ожидаемые годы для каждой группы
        group_years = {
            'младшая': [2022, 2023],
            'средняя': [2020, 2021],
            'старшая': [2018, 2019]
        }

        if group not in group_years:
            return False, f'Неизвестная группа: {group}'

        if year not in group_years[group]:
            expected_years = group_years[group]
            return False, f'Ребенок {year} года рождения не может быть в {group} группе. ' \
                          f'Для {group} группы допустимы годы: {expected_years[0]}-{expected_years[1]}'

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
        return records, f'Файл {filename} не найден. Будет создан новый.'
    except Exception as e:
        return records, f'Ошибка при чтении файла: {e}'

    current_record = {}
    valid_records = 0
    skipped_records = 0

    for line in lines:
        line = line.strip()

        if not line:
            if current_record:
                # Проверяем обязательные поля
                required = ['фамилия', 'имя', 'дата_рождения', 'группа']
                if all(field in current_record for field in required):
                    # Проверяем соответствие группы и года рождения
                    birth_date = current_record['дата_рождения']
                    group = current_record['группа']
                    is_valid, error_msg = validate_group_by_birth_year(birth_date, group)
                    if is_valid:
                        records.append(current_record)
                        valid_records += 1
                    else:
                        skipped_records += 1
                else:
                    skipped_records += 1
                current_record = {}
            continue

        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            current_record[key] = value

    # Добавляем последнюю запись
    if current_record:
        required = ['фамилия', 'имя', 'дата_рождения', 'группа']
        if all(field in current_record for field in required):
            birth_date = current_record['дата_рождения']
            group = current_record['группа']
            is_valid, error_msg = validate_group_by_birth_year(birth_date, group)
            if is_valid:
                records.append(current_record)
                valid_records += 1
            else:
                skipped_records += 1
        else:
            skipped_records += 1

    # Обрабатываем пакет записей для кеширования
    if records:
        records = process_records_batch(records)

    message = f'Загружено {valid_records} записей'
    if skipped_records > 0:
        message += f', пропущено {skipped_records} некорректных записей'

    return records, message


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
        # Удаляем внутренние поля перед сохранением
        clean_records = []
        for record in records:
            clean_record = {}
            for key, value in record.items():
                if not key.startswith('_'):  # Пропускаем внутренние поля
                    clean_record[key] = value
            clean_records.append(clean_record)

        # Буферизованная запись
        buffer = []
        for record in clean_records:
            buffer.append(f'фамилия: {record["фамилия"]}\n')
            buffer.append(f'имя: {record["имя"]}\n')
            buffer.append(f'дата_рождения: {record["дата_рождения"]}\n')
            buffer.append(f'группа: {record["группа"]}\n')

            # Специалисты (могут отсутствовать)
            specialists = ['невропатолог', 'отоларинголог', 'ортопед', 'окулист']
            for specialist in specialists:
                if specialist in record:
                    buffer.append(f'{specialist}: {record[specialist]}\n')

            buffer.append('\n')  # Пустая строка между записями

        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(buffer)

        return f'Данные сохранены в файл {filename} ({len(records)} записей)'

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
        # Сначала получаем дату рождения
        birth_date = input('Дата рождения (ГГГГ-ММ-ДД): ').strip()
        is_valid_date, error_msg_date = validate_date(birth_date)
        if not is_valid_date:
            print(f'Ошибка: {error_msg_date}')
            continue

        # Быстро определяем год
        try:
            year = int(birth_date.split('-')[0])
        except:
            print('Ошибка: не удалось определить год рождения')
            continue

        # Определяем доступные группы для этого года рождения
        available_groups = []
        if year in [2022, 2023]:
            available_groups.append('младшая')
        if year in [2020, 2021]:
            available_groups.append('средняя')
        if year in [2018, 2019]:
            available_groups.append('старшая')

        if not available_groups:
            print(f'Ошибка: ребенок {year} года рождения не подходит ни для одной группы. '
                  f'Допустимые годы: младшая (2022-2023), средняя (2020-2021), старшая (2018-2019)')
            continue

        # Получаем группу
        print(f'Доступные группы для {year} года рождения: {", ".join(available_groups)}')
        group = input(f'Группа ({"/".join(available_groups)}): ').strip().lower()

        if not validate_group(group):
            print('Ошибка: группа должна быть "младшая", "средняя" или "старшая"')
            continue

        # Быстрая проверка соответствия группы и года
        if group == 'младшая' and year not in [2022, 2023]:
            print(f'Ошибка: ребенок {year} года рождения не может быть в младшей группе')
            continue
        elif group == 'средняя' and year not in [2020, 2021]:
            print(f'Ошибка: ребенок {year} года рождения не может быть в средней группе')
            continue
        elif group == 'старшая' and year not in [2018, 2019]:
            print(f'Ошибка: ребенок {year} года рождения не может быть в старшей группе')
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
                break  # Пропускаем если нет данных

            conclusion_lower = conclusion.lower()
            if conclusion_lower in ['здоров', 'нуждается в лечении']:
                new_record[key] = conclusion_lower
                break
            print('Ошибка: заключение должно быть "здоров" или "нуждается в лечении"')

    # Обрабатываем новую запись для добавления кешированных полей
    processed_record = process_records_batch([new_record])[0]
    records.append(processed_record)

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
        print(f'{i}. {record["фамилия"]} {record["имя"]} - {record["группа"]} группа, '
              f'{record["дата_рождения"]} г.р.')

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
                        # Обновляем кешированные значения
                        from utils import process_records_batch
                        records = process_records_batch(records)
                    return records, 'Фамилия изменена'

                elif field_choice == '2':
                    new_value = input('Новое имя: ').strip()
                    if new_value:
                        record['имя'] = new_value
                    return records, 'Имя изменено'

                elif field_choice == '3':
                    # При изменении даты рождения проверяем соответствие с группой
                    current_group = record['группа']
                    new_birth_date = input('Новая дата рождения (ГГГГ-ММ-ДД): ').strip()

                    is_valid_date, error_msg_date = validate_date(new_birth_date)
                    if not is_valid_date:
                        return records, f'Ошибка: {error_msg_date}'

                    # Быстрая проверка соответствия
                    try:
                        year = int(new_birth_date.split('-')[0])
                        if current_group == 'младшая' and year not in [2022, 2023]:
                            return records, f'Ошибка: ребенок {year} года рождения не может быть в младшей группе'
                        elif current_group == 'средняя' and year not in [2020, 2021]:
                            return records, f'Ошибка: ребенок {year} года рождения не может быть в средней группе'
                        elif current_group == 'старшая' and year not in [2018, 2019]:
                            return records, f'Ошибка: ребенок {year} года рождения не может быть в старшей группе'
                    except:
                        return records, 'Ошибка: не удалось определить год рождения'

                    record['дата_рождения'] = new_birth_date
                    # Обновляем кешированные значения
                    from utils import process_records_batch
                    records = process_records_batch(records)
                    return records, 'Дата рождения изменена'

                elif field_choice == '4':
                    # При изменении группы проверяем соответствие с датой рождения
                    current_birth_date = record['дата_рождения']
                    new_group = input('Новая группа (младшая/средняя/старшая): ').strip().lower()

                    if not validate_group(new_group):
                        return records, 'Ошибка: неверное название группы'

                    # Быстрая проверка соответствия
                    try:
                        year = int(current_birth_date.split('-')[0])
                        if new_group == 'младшая' and year not in [2022, 2023]:
                            return records, f'Ошибка: ребенок {year} года рождения не может быть в младшей группе'
                        elif new_group == 'средняя' and year not in [2020, 2021]:
                            return records, f'Ошибка: ребенок {year} года рождения не может быть в средней группе'
                        elif new_group == 'старшая' and year not in [2018, 2019]:
                            return records, f'Ошибка: ребенок {year} года рождения не может быть в старшей группе'
                    except:
                        return records, 'Ошибка: не удалось определить год рождения'

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
                    new_value = input(f'Новое заключение {specialist} (здоров/нуждается в лечении): ').strip().lower()

                    if not new_value:  # Удалить запись
                        if specialist in record:
                            del record[specialist]
                        # Обновляем кешированные значения
                        from utils import process_records_batch
                        records = process_records_batch(records)
                        return records, f'Заключение {specialist} удалено'
                    elif new_value in ['здоров', 'нуждается в лечении']:
                        record[specialist] = new_value
                        # Обновляем кешированные значения
                        from utils import process_records_batch
                        records = process_records_batch(records)
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
            return records, f'Ошибка при удалении: {e}'