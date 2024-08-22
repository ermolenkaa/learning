from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Создание базы данных и подключение к ней
engine = create_engine('postgresql://postgres:vbif@localhost/ParsNewsDB')
Base = declarative_base()

# Определение таблиц
class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    news = relationship("News", uselist=False, back_populates="link")

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey('links.id'), unique=True)
    news_id = Column(String, unique=True)
    date = Column(TIMESTAMP)
    time = Column(String)
    title = Column(String)
    text = Column(Text)
    link = relationship("Link", back_populates="news")

# Создание таблиц
Base.metadata.create_all(engine)
