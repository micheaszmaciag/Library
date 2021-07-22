from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from service import *


def main():
    engine = create_engine(f"sqlite:///author_book_publisher.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    add_new_book(session, 'J.R.R. Tolkien', 'Władca pierścieni', 'Testowy')
    add_new_book(session, 'J.R.R. Tolkien', 'Hobbit', 'Testowy')
    add_new_book(session, 'Andrzej Sapkowski', 'Narrenturm', 'Nowa Fantastyka')
    add_new_book(session, 'Andrzej Sapkowski', 'Wiedźmin', 'Nowa Fantastyka')

    books_by_publisher = get_books_by_publishers(session, ascending=False)
    for row in books_by_publisher:
        print(f'Publisher: {row.name}, total books: {row.total_books}')
    print()
    authors_by_publisher = get_authors_by_publishers(session, ascending=False)
    for row in authors_by_publisher:
        print(f'Publisher: {row.name}, total authors: {row.total_authors}')
    print()
    authors = get_authors(session)
    print(authors)


if __name__ == '__main__':
    main()
