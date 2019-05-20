class LOG_CLI:
    LOGGER_NAME = 'msgr_cli'
    DIR_NAME = 'logs'
    FILE_NAME = 'msgr_cli'
    RECORD_FORMAT = '%(asctime)s.%(msecs)03d;%(name)s;%(levelname)s;%(module)s;%(message)s'
    HEADER = 'TIMESTAMP;LOGGER_NAME;MSG_LEVEL;MODULE_NAME;MSG_TEXT'
    RECORD_TIME_FORMAT = '%d.%m.%Y-%H:%M:%S'
    FILE_EXTENSION = 'log'
    WARN_LEVEL = 'INFO'

    class FILE_ROTATING:
        MAX_BYTES = 1000000
        BACKUP_COUNT = 2
