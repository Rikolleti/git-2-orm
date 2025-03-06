import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from main import create_tables,Publisher,Book,Shop,Stock,Sale

DSN = "postgresql://postgres:postgres@localhost:5432/orm_db"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Ввод от пользователя
def input_publisher_name():
    output = input("Введите название издателя: ")
    return output

publisher_name = input_publisher_name()

# Добавляем нового издателя
new_publisher = Publisher(name=publisher_name)
session.add(new_publisher)

# Добавляем новую книгу
new_book = Book(title="Ночная смена", id_publisher="1")
session.add(new_book)

# Добавляем новый магазин
new_shop = Shop(name="Читай-Город")
session.add(new_shop)

# Добавляем новый сток
new_stock = Stock(id_book=1, id_shop=1, count=500)
session.add(new_stock)

# Добавляем продажи
new_sale = Sale(price=1500, date_sale="2018-10-25T09:45:24.552Z", id_stock=1, count=40)
session.add(new_sale)
session.commit()

# Запрос
query = (
    session.query(Book.title, Shop.name, Sale.price * Sale.count, Sale.date_sale)
    .select_from(Book)
    .join(Stock, Stock.id_book == Book.id)
    .join(Shop, Shop.id == Stock.id_shop)
    .join(Sale, Sale.id_stock == Stock.id)
)
results = query.all()
for res in results:
    title, shop_name, price, date = res
    print(f"{title} | {shop_name} | {price} | {date}")