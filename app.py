from flask import Flask, redirect, url_for
from flask import render_template, request
from werkzeug.utils import secure_filename
import db_operator
from os import remove,path

app = Flask(__name__, static_url_path='/static')


@app.route("/" , methods=["GET"])
def main_page():
        books_data = db_operator.main_page()
        return render_template("main_page.html", books=books_data)


@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    if request.method == "POST":
        cover_image = request.files['CoverImage']
        file_name = secure_filename(cover_image.filename)
        if (db_operator.insert_book(request.form['bookName'], request.form['authorName'], file_name,
            request.form['lang'], request.form['isTranslated'], request.form['pages'], request.form['pagesRead'],
             request.form['rate'], request.form['fullReview'])):
            cover_image.save(f"static/media/book_cover/{file_name}")
            return render_template("add_book.html", status="true")
    else:
        return render_template("add_book.html")


@app.route('/view_book/<book_id>', methods=['GET'])
def view_book(book_id):
    book_data = db_operator.book_view(book_id)
    book_data = list(book_data[0])
    quotes = db_operator.get_quotes(book_id)
    return render_template("view_book.html", book=book_data, quotes=quotes)


@app.route('/edit_book/<book_id>', methods=["GET", "POST"])
def edit_book(book_id):
    book_data = db_operator.book_view(book_id)
    book_data = list(book_data[0])
    if request.method == "POST":
        if path.isfile(f"static/media/book_cover/{book_data[2]}"):
            remove(f"static/media/book_cover/{book_data[2]}")
        cover_image = request.files['CoverImage']
        file_name = secure_filename(cover_image.filename)
        if (db_operator.update_book(request.form['bookName'], request.form['authorName'], file_name,
            request.form['lang'], request.form['isTranslated'], request.form['pages'], request.form['pagesRead'],
             request.form['rate'], request.form['fullReview'], book_id)):
            cover_image.save(f"static/media/book_cover/{file_name}")
            return redirect(url_for('view_book',book_id=book_id))
    else:
        return render_template("edit_post.html", book=book_data)


# TODO: complete search function
@app.route('/search',methods=["POST"])
def search():
    if request.method == "POST":
        search = request.form['searched']
        return render_template("search.html" , search = search)
    else:
        return redirect(url_for('main_page'))

@app.route('/add_quote/<book_id>',methods=["GET","POST"])
def add_quote(book_id):
    book_data = db_operator.book_view(book_id)
    book_data = list(book_data[0])
    if request.method == "POST":
        db_operator.insert_quote(request.form['quoteBody'],book_id,request.form['pageFrom'])
        return render_template("add_quote.html", status="true", book_name=book_data)
    else:
        return render_template("add_quote.html", status="not send",book_name=book_data)


if __name__ == "__main__":
    app.run()
