import os
import logging
import logging.handlers as handlers
from functools import wraps

from log_config import LOG_SRV, LOG_CLI, LOG_DBG, FLUSH_LOGS_ON_START


def get_logger(log_conf):
    header = log_conf.HEADER
    if not header.endswith('\n'):
        header += '\n'

    file_name = '.'.join([log_conf.FILE_NAME, log_conf.FILE_EXTENSION])
    dir_path = os.path.join(os.getcwd(), log_conf.DIR_NAME)
    full_file_name = os.path.join(dir_path, file_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    if not os.path.exists(full_file_name) or FLUSH_LOGS_ON_START:
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


def log_func_call(logger):
    def decorator(func_to_log):
        @wraps(func_to_log)
        def decorated(*args, **kwargs):
            module = func_to_log.__module__
            func_name = func_to_log.__name__
            args_list = [str(x) for x in list(args) + list(kwargs.values())]
            arguments = '\"{}\"'.format(','.join(args_list))
            msg = "\"" + ','.join([module, func_name, arguments]) + "\""
            logger.info(msg)
            return func_to_log(*args, **kwargs)

        return decorated

    return decorator


def log_and_print(log_func, msg):
    log_func(msg)
    print(msg)


dbg_logger = get_logger(log_conf=LOG_DBG)
srv_logger = get_logger(log_conf=LOG_SRV)
cli_logger = get_logger(log_conf=LOG_CLI)
