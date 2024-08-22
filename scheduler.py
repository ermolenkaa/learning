import schedule
import time
import logging
from pars_news import job

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Планирование задачи на выполнение раз в 30 минут
print("Скрипт запущен. Задача будет выполняться раз в 30 минут.")
logging.info("Скрипт запущен. Задача будет выполняться раз в 30 минут.")
schedule.every(30).minutes.do(job)

# Бесконечный цикл для выполнения запланированных задач
while True:
    schedule.run_pending()
    time.sleep(1)
