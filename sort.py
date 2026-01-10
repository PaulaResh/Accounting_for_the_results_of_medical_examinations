'''
Модуль с алгоритмами сортировки.
Реализует метод Хоара (быстрая сортировка) для различных критериев.
'''

from utils import parse_date


def quicksort(arr, key_func, reverse=False):
    '''
    Реализация быстрой сортировки (метод Хоара).

    Args:
        arr (list): Список для сортировки
        key_func (function): Функция для получения ключа сортировки
        reverse (bool): True для сортировки по убыванию

    Returns:
        list: Отсортированный список
    '''
    # Базовый случай рекурсии
    if len(arr) <= 1:
        return arr

    # Выбираем опорный элемент (середина массива)
    pivot = arr[len(arr) // 2]
    pivot_key = key_func(pivot)

    # Разделяем массив на три части
    less = []
    equal = []
    greater = []

    for item in arr:
        item_key = key_func(item)
        if item_key < pivot_key:
            less.append(item)
        elif item_key == pivot_key:
            equal.append(item)
        else:
            greater.append(item)

    # Рекурсивно сортируем и объединяем результаты
    if reverse:
        return quicksort(greater, key_func, reverse) + equal + quicksort(less, key_func, reverse)
    else:
        return quicksort(less, key_func, reverse) + equal + quicksort(greater, key_func, reverse)


def sort_by_health_then_name(records):
    '''
    Сортировка по убыванию количества здоровых заключений, затем по фамилии.
    Оптимизированная версия, использует предвычисленные значения.

    Args:
        records (list): Список записей

    Returns:
        list: Отсортированный список
    '''

    def key_func(record):
        # Используем предвычисленное количество здоровых или вычисляем на лету
        healthy = record.get('_healthy_count', 0)
        return (-healthy, record['фамилия'].lower())

    return quicksort(records, key_func)


def sort_by_birth_date(records):
    '''
    Сортировка по дате рождения (год, месяц, день).
    Оптимизированная версия с быстрым парсингом даты.

    Args:
        records (list): Список записей

    Returns:
        list: Отсортированный список
    '''

    def key_func(record):
        date_str = record['дата_рождения']
        # Быстрый парсинг даты (только для сортировки)
        parts = date_str.split('-')
        if len(parts) == 3:
            return (int(parts[0]), int(parts[1]), int(parts[2]))
        return (0, 0, 0)  # В случае ошибки формата

    return quicksort(records, key_func)


def sort_by_group_then_name(records):
    '''
    Сортировка по группе, затем по фамилии.
    Использует числовые значения групп для быстрого сравнения.

    Args:
        records (list): Список записей

    Returns:
        list: Отсортированный список
    '''
    # Порядок сортировки групп
    group_order = {'младшая': 1, 'средняя': 2, 'старшая': 3}

    def key_func(record):
        group = record['группа'].lower()
        group_num = group_order.get(group, 99)  # 99 для неизвестных групп
        return (group_num, record['фамилия'].lower())

    return quicksort(records, key_func)


def sort_by_health_group_name(records):
    '''
    Специальная сортировка для отчета 3: группа + фамилия.
    Оптимизированная версия.

    Args:
        records (list): Список записей, нуждающихся в лечении

    Returns:
        list: Отсортированный список
    '''
    # Порядок сортировки групп
    group_order = {'младшая': 1, 'средняя': 2, 'старшая': 3}

    def key_func(record):
        group = record['группа'].lower()
        group_num = group_order.get(group, 99)
        return (group_num, record['фамилия'].lower())

    return quicksort(records, key_func)


def sort_by_name_only(records):
    '''
    Быстрая сортировка только по фамилии.

    Args:
        records (list): Список записей

    Returns:
        list: Отсортированный список
    '''

    def key_func(record):
        return record['фамилия'].lower()

    return quicksort(records, key_func)