import os
import logging
import logging.handlers as handlers
from functools import wraps

from cli_log_config import LOG_CLI
from srv_log_config import LOG_SRV


class DebugLogConf:
    LOGGER_NAME = 'debugger'
    DIR_NAME = 'logs'
    FILE_NAME = 'debug'
    RECORD_FORMAT = '%(asctime)s.%(msecs)03d;%(name)s;%(levelname)s;%(module)s;%(message)s'
    HEADER = 'TIMESTAMP;LOGGER_NAME;MSG_LEVEL;MODULE_NAME;MSG_TEXT'
    RECORD_TIME_FORMAT = '%d.%m.%Y-%H:%M:%S'
    FILE_EXTENSION = 'log'
    WARN_LEVEL = 'INFO'


def get_logger(log_conf):
    header = log_conf.HEADER
    if not header.endswith('\n'):
        header += '\n'

    file_name = '.'.join([log_conf.FILE_NAME, log_conf.FILE_EXTENSION])
    dir_path = os.path.join(os.getcwd(), log_conf.DIR_NAME)
    full_file_name = os.path.join(dir_path, file_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    if not os.path.exists(full_file_name):
        with open(full_file_name, 'w', encoding='utf-8') as file:
            file.writelines(header)

    logger = logging.getLogger(name=log_conf.LOGGER_NAME)
    logger.setLevel(log_conf.WARN_LEVEL)

    if hasattr(log_conf, "TIMED_ROTATING"):
        handler = handlers.TimedRotatingFileHandler(filename=full_file_name,
                                                    when=log_conf.TIMED_ROTATING.INTERVAL_TYPE,
                                                    interval=log_conf.TIMED_ROTATING.INTERVALS_COUNT,
                                                    backupCount=log_conf.TIMED_ROTATING.BACKUP_COUNT)
        handler.suffix = log_conf.TIMED_ROTATING.SUFFIX
    elif hasattr(log_conf, "FILE_ROTATING"):
        handler = handlers.RotatingFileHandler(filename=full_file_name,
                                               maxBytes=log_conf.FILE_ROTATING.MAX_BYTES,
                                               backupCount=log_conf.FILE_ROTATING.BACKUP_COUNT)
    else:
        handler = handlers.RotatingFileHandler(filename=full_file_name,
                                               maxBytes=0,
                                               backupCount=0)
    handler.setFormatter(logging.Formatter(fmt=log_conf.RECORD_FORMAT,
                                           datefmt=log_conf.RECORD_TIME_FORMAT))
    handler.setLevel(log_conf.WARN_LEVEL)
    logger.addHandler(handler)

    return logger


debug_logger = get_logger(DebugLogConf)
srv_logger = get_logger(log_conf=LOG_SRV)
cli_logger = get_logger(log_conf=LOG_CLI)


def log_func_call(func_to_log):
    @wraps(func_to_log)
    def wrapper(*args, **kwargs):
        module = func_to_log.__module__
        func_name = func_to_log.__name__
        args_list = [str(x) for x in list(args) + list(kwargs.values())]
        arguments = '\"{}\"'.format(','.join(args_list))
        msg = "\"" + ','.join([module, func_name, arguments]) + "\""
        debug_logger.info(msg)
        return func_to_log(*args, **kwargs)

    return wrapper
