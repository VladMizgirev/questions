import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

import json

#login = str(input())
#password = str(input())
#name_bd = str(input())
#DSN = f'postgresql://{login}:{password}@localhost:5432/{name_bd}'
DSN1 = 'postgresql://Vlad:19121996@localhost:5432/bd'
engine = sqlalchemy.create_engine(DSN1)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

meta = MetaData()
#sql_uri = 'sqlite:///db.sqlite'
#sql_engine = create_engine (sql_uri)
#sql_meta = MetaData (sql_engine)

class Publisher(Base):
    __tablename__ = "publisher"

    id_publisher = sq.Column(sq.Integer, primary_key=True)
    name_publisher = sq.Column(sq.String(length=40), unique=True)

class Book(Base):
    __tablename__ = "book"

    id_book = sq.Column(sq.Integer, primary_key=True)
    title_publisher = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("id_publisher"), nullable=False)

    publisher = relationship(Publisher, backref="book")

class Shop(Base):
    __tablename__ = "shop"

    id_shop = sq.Column(sq.Integer, primary_key=True)
    name_shop = sq.Column(sq.String(length=40), unique=True)

class Stock(Base):
    __tablename__ = "stock"

    id_stock = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("id_book"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("id_shop"), nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__ = "sale"

    id_sale = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer)
    data_sale = sq.Column(sq.Date)
    count = sq.Column(sq.Integer)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("id_stock"), nullable=False)

    stock = relationship(Stock, backref="sale")

#def create_tables(engine):
    #Base.sql_meta.create_all(engine)



with open ('База данных json.json', 'r', encoding='cp1251') as f:
    data = json.load(f)

for record in data:
    print(record.get('model'))
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

meta.create_all()

session.close()