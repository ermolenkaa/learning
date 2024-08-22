from bs4 import BeautifulSoup
import requests
from datetime import datetime
import logging
from database import engine, Base, Link, News, sessionmaker

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Вспомогательные функции
def getSimbols(n: int, k: int, string: str) -> str:
    returnvalue = ""
    for i in range(n, k):
        returnvalue += string[i]
    return returnvalue

def clear_text(text: str) -> str:
    text = text.replace('© 2024, РИА «Новый День»', '')
    text = text.replace('Написать автору или сообщить новость', '')
    text = text.replace('Подписывайтесь на каналыДзен YouTube', '')
    text = text.replace('Подписаться на ТГ-канал «Новый День – Передовица»', '')
    return text

def job():
    url = 'https://newdaynews.ru/today/'
    page = requests.get(url)
    if page.status_code == 200:
        logging.info("Страница успешно загружена")
    else:
        logging.error(f"Ошибка загрузки страницы: {page.status_code}")
        return

    new_news = []
    news = []

    # Используем BeautifulSoup для парсинга HTML:
    soup = BeautifulSoup(page.text, "html.parser")

    # Поиск элементов с нужным классом:
    news = soup.findAll('a', class_='gbc-b gbc-opc')

    # Проверка, найдены ли элементы:
    if news:
        logging.info("Найдены элементы")
    else:
        logging.info("Элементы не найдены")
        return

    # Создание сессии для работы с базой данных
    Session = sessionmaker(bind=engine)
    session = Session()

    # Вывод результатов и их загрузка в базу данных:
    news_from_links, news_ids, links, dates, times, titles = [], [], [], [], [], []

    logging.info(f"Количество найденных новостей: {len(news)}")
    # Вывод для проверки кода
    for item in news:
        date = getSimbols(0, 6, item.text) + '20' + getSimbols(6, 8, item.text)
        time = getSimbols(9, 14, item.text)  # Если честно не знаю зачем писал гетсимболс, забыл что на питоне можно делать [0:6]
        title = getSimbols(14, len(item.text), item.text)
        dates.append(date)
        times.append(time)  # Загрузка в массивы
        titles.append(title)

        referenc = item.get('href')
        news_id = referenc.split('/')[-1].split('.')[0]  # Получение id новости из ссылки
        new_link = url + referenc
        links.append(new_link)

        news_from_links.append(BeautifulSoup(requests.get(new_link).text, "html.parser").findAll('div', class_='afo-txt afo-txt_0_' + news_id + ' mmar-h2'))
        logging.info(f"Дата: {date}, Время: {time}, Заголовок: {title}")

        link_entry = session.query(Link).filter_by(link=new_link).first()
        if not link_entry:
            # Сохранение ссылки в базу данных
            link_entry = Link(link=new_link)
            session.add(link_entry)
            session.commit()
            logging.info(f"Новая ссылка добавлена: {new_link}")

        # Сохранение новости в базу данных
        news_entry = News(
            link_id=link_entry.id,
            news_id=news_id,
            date=datetime.strptime(date, "%d.%m.%Y"),
            time=time,
            title=title,
            text=clear_text(news_from_links[-1][0].text) if news_from_links[-1] else ""
        )
        session.add(news_entry)
        session.commit()
        logging.info(f"Новость добавлена: {title}")

    # Закрытие сессии
    session.close()
