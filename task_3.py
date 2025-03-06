import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from main import create_tables,Publisher,Book,Shop,Stock,Sale

DSN = "postgresql://postgres:postgres@localhost:5432/orm_db"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

def json_loading():
    with open("fixtures/tests_data.json", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            model_value = item.get("model")
            pk_value = item.get("pk")
            fields_value = item.get("fields", {})
            if model_value == "publisher":
                name = fields_value.get("name")
                add_data_to_publisher(pk_value, name)
            elif model_value == "book":
                title = fields_value.get("title")
                id_publisher = fields_value.get("id_publisher")
                add_data_to_book(pk_value, title, id_publisher)
            elif model_value == "shop":
                name = fields_value.get("name")
                add_data_to_shop(pk_value, name)
            elif model_value == "stock":
                id_shop = fields_value.get("id_shop")
                id_book = fields_value.get("id_book")
                count = fields_value.get("count")
                add_data_to_stock(pk_value, id_shop, id_book, count)
            elif model_value == "sale":
                price = fields_value.get("price")
                date_sale = fields_value.get("date_sale")
                count = fields_value.get("count")
                id_stock = fields_value.get("id_stock")
                add_data_to_sale(pk_value, price, date_sale, count, id_stock)

def add_data_to_publisher(pk_value, name):
    new_publisher = Publisher(id = pk_value, name=name)
    session.add(new_publisher)
    session.commit()

def add_data_to_book(pk_value, title, id_publisher):
    new_book = Book(id = pk_value, title=title, id_publisher=id_publisher)
    session.add(new_book)
    session.commit()

def add_data_to_shop(pk_value, name):
    new_shop = Shop(id = pk_value, name=name)
    session.add(new_shop)
    session.commit()

def add_data_to_stock(pk_value, id_shop, id_book, count):
    new_stock = Stock(id = pk_value, id_book=id_book, id_shop=id_shop, count=count)
    session.add(new_stock)
    session.commit()

def add_data_to_sale(pk_value, price, date_sale, count, id_stock):
    new_sale = Sale(id=pk_value, price=price, date_sale=date_sale, id_stock=id_stock, count=count)
    session.add(new_sale)
    session.commit()


result = session.query(Publisher).all()
for res in result:
    print(res)

json_loading()