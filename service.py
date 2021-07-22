from sqlalchemy import and_, asc, desc, func
from models import Author, Book, Publisher


def get_books_by_publishers(session, ascending=True):
    if not isinstance(ascending, bool):
        raise ValueError(f'Sorting value is invalid: {ascending}.')
    direction = asc if ascending else desc
    return (
        session.query(Publisher.name, func.count(Book.title).label('total_books'))
            .join(Publisher.books)
            .group_by(Publisher.name)
            .order_by(direction('total_books'))
    )


def get_authors_by_publishers(session, ascending=True):
    if not isinstance(ascending, bool):
        raise ValueError(f'Sorting value is invalid: {ascending}.')
    direction = asc if ascending else desc
    return (
        session.query(Publisher.name, func.count(Author.last_name).label('total_authors'))
            .join(Publisher.authors)
            .group_by(Publisher.name)
            .order_by(direction('total_authors'))
    )


def get_authors(session):
    return session.query(Author).order_by(Author.last_name).all()


def add_new_book(session, author_name, book_title, publisher_name):
    first_name, _, last_name = author_name.partition(" ")
    book = session.query(Book) \
        .join(Author) \
        .filter(Book.title == book_title) \
        .filter(and_(Author.first_name == first_name, Author.last_name == last_name)) \
        .filter(Book.publishers.any(Publisher.name == publisher_name)) \
        .one_or_none()
    if book is not None:
        return

    book = session.query(Book) \
        .join(Author) \
        .filter(Book.title == book_title) \
        .filter(and_(Author.first_name == first_name, Author.last_name == last_name)) \
        .one_or_none()

    if book is None:
        book = Book(title=book_title)

    author = session.query(Author) \
        .filter(and_(Author.first_name == first_name, Author.last_name == last_name)) \
        .one_or_none()

    if author is None:
        author = Author(first_name=first_name, last_name=last_name)
        session.add(author)

    publisher = session.query(Publisher) \
        .filter(Publisher.name == publisher_name).one_or_none()

    if publisher is None:
        publisher = Publisher(name=publisher_name)
        session.add(publisher)

    book.author = author
    book.publishers.append(publisher)
    session.add(book)
    session.commit()
