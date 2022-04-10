import re
from typing import Iterator


def create_response(result: Iterator, cmd: str, value: str) -> Iterator:
    """
    Принимает 5 параметров из запроса: где 1, 2, 3, 4 - запрос, 5-ый - имя файла, обрабатывает файл,
    следуя написанному запросу, и возвращает ответ клиенту.
    :param result: итератор последовательности с записями запросов сервера.
    :param cmd: запрос означающий, какая команда будет выполнена.
    :param value: аргумент, с которым выполнится команда cmd.
    :return: итератор обработанных в соответствии с запросом данных из файла логов.
    """

    if cmd == "filter":
        return filter(lambda x: value in x, result)
    if cmd == "map":
        return map(lambda x: x.split(" ")[int(value)], result)
    if cmd == "unique":
        return iter(set(result))
    if cmd == "sort":
        reverse = value == 'desc'
        return iter(sorted(result, reverse=reverse))
    if cmd == "limit":
        return get_by_limit(result, int(value))
    if cmd == "regex":
        pattern = re.compile(value)
        return filter(lambda v: pattern.search(v), result)

    return result


def get_by_limit(data: Iterator, limit: int) -> Iterator:
    """
    Возвращает строки в соответствии с лимитом из запроса.
    :param data: итератор последовательности с записями запросов сервера.
    :param limit: ограничение количества запросов, введённое пользователем.
    :return: итератор обработанных в соответствии с лимитом данных из файла логов.
    """
    i = 0
    for item in data:
        if i < limit:
            yield item
        else:
            break
        i += 1
