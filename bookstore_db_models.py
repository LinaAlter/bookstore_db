import sqlalchemy
import sqlalchemy as sq
import datetime as dt
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq. Column(sq.String(length=40), unique=True)
    books = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f'Publisher: {self.id}:{self.name}'
    
class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq. Column(sq.String(length=80))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship("Publisher", back_populates="books") 
    stock = relationship("Stock", back_populates="books")
    
    def __str__(self):
        return f'Book: {self.id}:{self.title}'

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq. Column(sq.String(length=40), unique=True)
    stock = relationship("Stock", back_populates="shops")
    def __str__(self):
        return f'Shop: {self.id}:{self.name}'

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True) 
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)
    sales = relationship("Sale", back_populates="stock")
    books = relationship("Book", back_populates="stock")
    shops = relationship("Shop", back_populates="stock")

    def __str__(self):
        return f'Stock: {self.id}, shop: {self.id_shop}, book: {self.id_book}, count: {self.count}'
    

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL(5,2), nullable=False)
    date_sale = sq.Column(sq.DateTime, default=dt.datetime.now)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)
    stock = relationship("Stock", back_populates="sales")

    def __str__(self):
        return f'Sale: {self.id}, price: {self.price}, stock: {self.id_stock}, count: {self.count}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)






