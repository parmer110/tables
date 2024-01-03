import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# تعریف مسیر‌های مورد نظر
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')
DEBUG_LOG_DIR = os.path.join(LOGGING_DIR, 'debug')
ERROR_LOG_DIR = os.path.join(LOGGING_DIR, 'error')
WARNING_LOG_DIR = os.path.join(LOGGING_DIR, 'warning')

log_directories = [
    LOGGING_DIR,
    DEBUG_LOG_DIR,
    ERROR_LOG_DIR,
    WARNING_LOG_DIR
]

# ایجاد پوشه‌ها به صورت خودکار
for directory in log_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error/error.log'),
            'formatter': 'verbose',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'warning/warning.log'),
            'formatter': 'verbose',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'debug/debug.log'),
            'formatter': 'verbose',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'error_file', 'warning_file', 'debug_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
