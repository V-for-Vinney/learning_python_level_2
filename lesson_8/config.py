import time


def get_current_time():  # абстрагирует нас от конкретного формата времени
    return time.time()


class Common:
    DEFAULT_ENCODING = 'utf-8'
    BUFFER_SIZE = 4096
    DATETIME_FORMAT = '%d.%m.%Y-%H:%M:%S'
    DEFAULT_CLIENT_STATUS = 'Online'


class JIM:
    USER = 'user'
    TO = 'send_to'
    FROM = 'send_from'
    ALERT = 'alert'
    ERROR = 'error'
    ROOM = 'room'
    TIME = 'time'

    AUTH = 'authenticate'
    JOIN = 'join'
    LEAVE = 'leave'
    MSG = 'message'
    PRESENCE = 'presence'
    PROBE = 'probe'
    OFFLINE = 'quit'
    RESPONSE = 'response'

    ACTION = 'action'
    ACCOUNT = 'account_name'
    PASSWORD = 'password'
    STATUS = 'status'
    UNKNOWN_CODE = 'unknown code'
    TYPE = 'type'
    ENCODING = 'encoding'


class HTTPResponseCode:
    # 1xx - уведомление:
    BASIC_NOTICE = (100, 'обычное уведомление')
    IMPORTANT_NOTICE = (101, 'важное уведомление')
    # 2xx - успешное завершение:
    OK = (200, 'OK')
    CREATED = (201, 'объект создан')
    CONFIRMED = (202, 'подтверждение')
    # 3xx - зарезервировано
    RESERVED = (300, 'зарезервировано')
    # 4xx - ошибка на стороне клиента:
    BAD_REQUEST = (400, 'неправильный запрос/JSON-объект')
    NEED_AUTH = (401, 'не авторизован')
    BAD_AUTH = (402, 'неправильный логин/пароль')
    FORBIDDEN = (403, 'пользователь заблокирован')
    NOT_FOUND = (404, 'пользователь/чат отсутствует на сервере')
    ALREADY_CONNECTED = (409, 'уже имеется подключение с указанным логином')
    UNAVAILABLE = (410, 'адресат существует, но недоступен')
    ALREADY_EXISTS = (411, 'чат с таким названием уже существует')
    ALREADY_DONE = (412, 'пользователь уже был добавлен/удален ранее')
    # 5xx - ошибка на стороне сервера:
    UNKNOWN_ERROR = (500, 'неизвестная ошибка сервера')
