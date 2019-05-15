import time


def get_current_time():  # абстрагирует нас от конкретного формата времени
    return time.time()


class Common:  # Config for JIM protocol keywords:
    DEFAULT_ENCODING = 'utf-8'
    BUFFER_SIZE = 4096
    DATETIME_FORMAT = '%d.%m.%Y-%H:%M:%S'


class Const:
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


class Code:
    # 1xx - уведомление:
    BASIC_NOTICE = 100
    IMPORTANT_NOTICE = 101
    # 2xx - успешное завершение:
    OK = 200
    CREATED = 201
    CONFIRMED = 202
    # 4xx - ошибка на стороне клиента:
    BAD_REQUEST = 400
    NEED_AUTH = 401
    BAD_AUTH = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    ALREADY_CONNECTED = 409
    UNAVAILABLE = 410
    ALREADY_EXISTS = 411
    ALREADY_DONE = 412
    # 5xx - ошибка на стороне сервера:
    UNKNOWN_ERROR = 500

    COMMENTS = {
        BASIC_NOTICE: 'обычное уведомление',
        IMPORTANT_NOTICE: 'важное уведомление',
        OK: 'OK',
        CREATED: 'объект создан',
        CONFIRMED: 'подтверждение',
        BAD_REQUEST: 'неправильный запрос/JSON-объект',
        NEED_AUTH: 'не авторизован',
        BAD_AUTH: 'неправильный логин/пароль',
        FORBIDDEN: 'пользователь заблокирован',
        NOT_FOUND: 'пользователь/чат отсутствует на сервере',
        ALREADY_CONNECTED: 'уже имеется подключение с указанным логином',
        UNAVAILABLE: 'адресат существует, но недоступен',
        ALREADY_EXISTS: 'чат с таким названием уже существует',
        ALREADY_DONE: 'пользователь уже был добавлен/удален ранее',
        UNKNOWN_ERROR: 'неизвестная ошибка сервера'
    }
    VALUES = tuple(COMMENTS.keys())
