class LOG_SRV:
    LOGGER_NAME = 'msgr_srv'
    DIR_NAME = 'logs'
    FILE_NAME = 'msgr_srv'
    RECORD_FORMAT = '%(asctime)s.%(msecs)03d;%(name)s;%(levelname)s;%(module)s;%(message)s'
    HEADER = 'TIMESTAMP;LOGGER_NAME;MSG_LEVEL;MODULE_NAME;MSG_TEXT'
    RECORD_TIME_FORMAT = '%d.%m.%Y-%H:%M:%S'
    FILE_EXTENSION = 'log'
    WARN_LEVEL = 'INFO'

    class TIMED_ROTATING:
        INTERVAL_TYPE = 'D'
        INTERVALS_COUNT = 1
        BACKUP_COUNT = '5'
        SUFFIX = '%Y-%m-%d'
