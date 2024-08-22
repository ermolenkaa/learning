import logging
import schedule
import time
from database import engine, Base, Link, News, sessionmaker
from pars_news import job

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Планирование задачи на выполнение раз в 30 минут
schedule.every(30).minutes.do(job)

# Запуск планировщика
def run_scheduler():
    logging.info("Скрипт запущен. Задача будет выполняться раз в 30 минут.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
