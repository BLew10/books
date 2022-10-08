# controllers.py, however many tables you have is however many controllers you need
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.book import Book
from flask_app.models.author import Author


#controllers file name shoudl be plural
#model file name should be singular
#table_name is plural
#table_class is uppercase and singular
#table_name_singular represents the singular version of whatever the table is representing. Ex: Dojos -> dojo. 

#route convention
#table_name/new -> displaying the form -> get method
#table_name/create -> processes form above -> post method
#table_name/<int:id> -> show -> get method
#table_name/<int:id>/edit -> displaying the form -> get method
#table_name/<int:id>/update -> processes the form -> post method
#table_name/<int:id>/delete-> deletes the row -> get method


@app.route('/books')
def books():
    all_books = Book.get_all()
    return render_template("books.html", books = all_books)

@app.route('/book/create', methods = ["post"])
def create_book():
    #creates a new __ from the client side and stores in the db
    if not Book.validate_book(request.form):
        return redirect('/books')
    new_book_data = { **request.form}
    Book.create(new_book_data)
    print(new_book_data)
    return redirect('/books')

# @app.route('/book/<int:id>')
# def book_show_one(id):

#     book_id = {
#         "id": id
#     }
#     #grabs all existing in the db
#     book = Book.get_one(book_id)
#     return render_template("one_book.html", book = book)

@app.route('/book/<int:id>/edit')
def book_edit(id):
    return render_template("book_edit.html")

@app.route('/book/<int:id>/update', methods = ['POST'])
def update_book(id):
    #deletes the target instance
    if not Book.validate_book(request.form):
        return redirect('/')
    updated_book_data = { **request.form}
    ## add an id w/ id argument
    Book.update_book(updated_book_data)
    print(updated_book_data)
    return redirect('/')

@app.route('/book/<int:id>/delete')
def delete_book(id):
    #deletes the target instance
    deleted_book_data = {
        "id": id
    }
    Book.delete_book(deleted_book_data)
    print(deleted_book_data)
    return redirect("/")

@app.route('/book/<int:id>')
def book_show_favs(id):
    print("hello")
    book_id = {
        "id": id
    }
    #grabs all existing in the db
    all_authors = Author.get_all()
    book = Book.get_one(book_id)
    
    book_fav_authors = Book.get_all_fav_authors(book_id)
    fav_authors = []
    non_favorited =[]

    if book_fav_authors:
        for fav_author in book_fav_authors:
            fav_authors.append(fav_author.name)
        for author in all_authors:
            if not author.name in fav_authors:
                non_favorited.append(author)
                    
    print(non_favorited)
    print(all_authors)
    if not non_favorited:
        non_favorited = all_authors

    return render_template("one_book.html", book=book, non_favs = non_favorited, book_fav_authors = book_fav_authors)

@app.route('/favorites/add_author/<int:id>', methods=["POST"])
def add_favorite_author(id):

    data = {
        "author_id": request.form['author_id'],
        "book_id": id
    }

    Book.add_new_author(data)

    return redirect(f"/book/{id}" )


