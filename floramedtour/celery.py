CELERY_BROKER_URL = 'redis://localhost:6379/0'  # اگر Redis را به عنوان بروکر انتخاب کرده‌اید
# یا
CELERY_BROKER_URL = 'pyamqp://guest:guest@localhost//'

# برای نتایج
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # اگر Redis را به عنوان بروکر انتخاب کرده‌اید
# یا
CELERY_RESULT_BACKEND = 'rpc://'
