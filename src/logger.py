import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,  # Можно заменить на DEBUG, WARNING и т.д.
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

log = logging.getLogger()