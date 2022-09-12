import mysql.connector
import password

db = mysql.connector.connect(
    host=password.HOST,
    user=password.USER_NAME,
    password=password.PASSWORD,
    database=password.DATABASE_NAME
)

cursor = db.cursor("SHOW TABLES")

# insert
def insert_author(name, picture_path):
    query = f"INSERT INTO author (name,picture_path) VALUES ('{name}','{picture_path}')"
    cursor.execute(query)
    db.commit()
    return True


def insert_book(name, author_id, cover_image, lang, is_translated, pages, pages_read, rate, full_review):
    query = f"INSERT INTO books (name,author_id,cover_image,lang,is_translated,pages,pages_read,rate,full_review)\
     VALUES ('{name}',{author_id},'{cover_image}','{lang}',{is_translated},{pages},\
     {pages_read},{rate},'{full_review}')"
    cursor.execute(query)
    db.commit()
    return True


def insert_quote(body, book_id, page_from):
    query = f'''INSERT INTO quotes (body,book_id,page_from) VALUES ("{body}",{book_id},{page_from})'''
    cursor.execute(query)
    db.commit()


# select
def book_view(book_id):
    query = f'select books.name , author.name, books.cover_image,books.lang , books.is_translated,books.pages,\
    books.pages_read,books.rate,books.full_review from books left join author on books.author_id = author.id\
    where books.id = {book_id}'
    cursor.execute(query)
    result = cursor.fetchall()
    return result


# update
def update_book(name, author_id, cover_image, lang, is_translated, pages, pages_read, rate, full_review, id_number):
    query = f"UPDATE `books` SET `name` = '{name}',`author_id` = '{author_id}', `cover_image` = '{cover_image}', `lang` = '{lang}',\
     `is_translated` = {is_translated},     `pages` = {pages}, `pages_read` = {pages_read},\
      `rate` = '{rate}', `full_review` = '{full_review}' WHERE (`id` = '{id_number}')"
    cursor.execute(query)
    db.commit()
    return True


# delete
def delete(table_name, id_number):
    query = f"DELETE FROM {table_name} WHERE (id = {id_number})"
    cursor.execute(query)
    db.commit()


#main_page_fetch
def main_page():
    query = "select books.name , author.name , books.cover_image , books.lang, books.is_translated , books.pages \
    , books.pages_read , books.rate, books.full_review ,books.id from books join author where books.author_id = author.id ORDER BY books.id DESC;"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_quote(book_id):
    query = f"SELECT * FROM quotes WHERE book_id={book_id} ORDER BY page_from"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def get_quotes():
    query = f"SELECT quotes.book_id, quotes.body, books.name FROM quotes join books where books.id = quotes.book_id order by book_id;"
    cursor.execute(query)
    result = cursor.fetchall()
    return result