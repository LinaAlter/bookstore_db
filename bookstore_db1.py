import sqlalchemy
from sqlalchemy.orm import sessionmaker
from bookstore_db_models import create_tables, Publisher, Shop, Book, Stock, Sale
import json
import pandas as pd




DSN = "postgresql://postgres:1358@localhost:5432/bookstore_db"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

def get_by_publisher(input):
    search = input
    if search.isnumeric():
        selected = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == search)
        for s in selected.all():
            print(f'{s[0]} | {s[1]} | {s[2]} | {s[3]}')
    if isinstance(search, str):
        selected = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name == search)
        for s in selected.all():
            print(f'{s[0]} | {s[1]} | {s[2]} | {s[3]}')
    
get_by_publisher(input('Введите название издательства или его идентификационный номер: '))




session.close()