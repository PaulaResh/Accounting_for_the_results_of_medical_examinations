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
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    pivot_key = key_func(pivot)

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

    if reverse:
        return quicksort(greater, key_func, reverse) + equal + quicksort(less, key_func, reverse)
    else:
        return quicksort(less, key_func, reverse) + equal + quicksort(greater, key_func, reverse)


def sort_by_health_then_name(records):
    '''
    Сортировка по убыванию количества здоровых заключений, затем по фамилии.

    Args:
        records (list): Список записей

    Returns:
        list: Отсортированный список
    '''
    from utils import count_healthy_specialists

    def key_func(record):
        healthy = count_healthy_specialists(record)
        return (-healthy, record['фамилия'].lower())

    return quicksort(records, key_func)


def sort_by_birth_date(records):
    '''
    Сортировка по дате рождения (год, месяц, день).

    Args:
        records (list): Список записей

    Returns:
        list: Отсортированный список
    '''

    def key_func(record):
        year, month, day = parse_date(record['дата_рождения'])
        return (year, month, day)

    return quicksort(records, key_func)


def sort_by_group_then_name(records):
    '''
    Сортировка по группе, затем по фамилии.

    Args:
        records (list): Список записей

    Returns:
        list: Отсортированный список
    '''
    group_order = {'младшая': 1, 'средняя': 2, 'старшая': 3}

    def key_func(record):
        group = record['группа'].lower()
        group_num = group_order.get(group, 99)
        return (group_num, record['фамилия'].lower())

    return quicksort(records, key_func)


def sort_by_health_group_name(records):
    '''
    Специальная сортировка для отчета 3: группа + фамилия.

    Args:
        records (list): Список записей, нуждающихся в лечении

    Returns:
        list: Отсортированный список
    '''
    group_order = {'младшая': 1, 'средняя': 2, 'старшая': 3}

    def key_func(record):
        group = record['группа'].lower()
        group_num = group_order.get(group, 99)
        return (group_num, record['фамилия'].lower())

    return quicksort(records, key_func)
