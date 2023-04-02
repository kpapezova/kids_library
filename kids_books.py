# Task: create an application that will store the content of our library. I chose children's books.
# more info about task is in the file "zadani_ukolu.txt"

import click
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Boolean

db = create_engine("sqlite:///books.sqlite")
Base = declarative_base()

## Create empty database
def connect_to():
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    return Session()
connect_to()       ## zavoláno pro vytvoreni databaze


class Book(Base):
    __tablename__ = "kids_books"
    id = Column(Integer, primary_key=True)
    book_name = Column(String)
    author = Column(String)
    number_of_pages = Column(Integer)
    date_added = Column(DateTime)
    read_yes_no = Column(Boolean, default=False)
    partially_read = Column(Boolean, default=False)
    lent_to = Column(String)        # name of person or None
    date_of_borrowing = Column(DateTime)
    notes = Column(String)

    def __repr__(self):
        return f"<Kniha(id={self.id}, book_name='{self.book_name}', author = '{self.author}', date_added={self.date_added})>"


@click.group()
def kids_library():
    pass


## ADD book into the library
@kids_library.command()
# @click.option("--adding", prompt="Add a book")
@click.option("--name", prompt="Name of the book")
@click.option("--author", prompt="Author of the book")
@click.option("--pages", prompt="Number of pages")
def add_book(name, author, pages):
    book_session = connect_to()
    book = Book(book_name=name, author=author, number_of_pages=pages, date_added=datetime.now())
    book_session.add(book)  
    book_session.commit()
    print(f"Added: {book.book_name}, {book.author}, {book.number_of_pages}")


## SUMMARY, write out the content of the library, dump file
@kids_library.command()
def dump_file():
    book_session = connect_to()
    qu = book_session.query(Book)   #qu (=query)
    books = qu.all()
    for book in books:
        if book.read_yes_no:
            print(f"{book.id}.) Název: {book.book_name}, autor: {book.author}, počet stran: {book.number_of_pages}, přidáno do knihovny: {book.date_added}, PŘEČTENO")
        elif book.partially_read:
            print(f"{book.id}.) Název: {book.book_name}, autor: {book.author}, počet stran: {book.number_of_pages}, přidáno do knihovny: {book.date_added}, ROZEČTENO")
        else:
            print(f"{book.id}.) Název: {book.book_name}, autor: {book.author}, počet stran: {book.number_of_pages}, přidáno do knihovny: {book.date_added}")


## READ, the books that we have already read
@kids_library.command()
@click.option("--book_id", prompt="Insert ID of the book")
def already_read(book_id):
    book_session = connect_to()
    qu = book_session.query(Book)
    read_book = qu.filter_by(id=book_id).one()
    read_book.read_yes_no = True
    book_session.add(read_book)
    book_session.commit()
    print(f"Kniha s ID {book_id} byla přečtena")


## PARTIALLY READ, the books where we are in the middle of the reading
@kids_library.command()
@click.option("--book_id", prompt="Insert ID of the book")
def partially_read(book_id):
    book_session = connect_to()
    qu = book_session.query(Book)
    read_book = qu.filter_by(id=book_id).one()
    read_book.partially_read = True
    book_session.add(read_book)
    book_session.commit()
    print(f"Kniha s ID {book_id} je rozečtená")



### Dodělat možnost půjčení + výpis půjčených knih
## LENT TO, the book was lent to "name of person", + date of borrowing
@kids_library.command()
@click.option("--book_id", prompt="Enter the ID of the borrowed book")
@click.option("--person", prompt="Enter the name of the person who borrowed the book")
def lend(book_id, person):
    book_session = connect_to()
    qu = book_session.query(Book)
    borrowed_book = qu.filter_by(id=book_id).one()
    borrowed_book.lent_to = person
    borrowed_book.date_of_borrowing = datetime.now()
    book_session.add(borrowed_book)
    book_session.commit()
    print(f"Kniha s ID {book_id} byla půjčena {borrowed_book.lent_to} dne {borrowed_book.date_of_borrowing}")


## PŘIDAT MOZNOST VRACENI





## NOTES
#doplnit funkci na zapsani poznamek






## UPDATE       #lze udelat v prikazove radce přes sqlite
#C:\Data\python_knihovny\04\kids_library>C:\sqlite\sqlite3.exe books.sqlite
# sqlite> update kids_book set book_name = 'opraveny_nazev' where id=1;
# ????? včera fungovalo, dnes píše přístup odepřen, tato aplikace nemůže běžet ve vašem počítači



if __name__ == "__main__":
    kids_library()