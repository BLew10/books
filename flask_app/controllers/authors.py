# controllers.py, however many tables you have is however many controllers you need
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.author import Author
from flask_app.models.book import Book


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

@app.route('/')
def home():
    #grabs all existing in the db
    authors = Author.get_all()
    return render_template("authors.html", authors = authors)

@app.route('/author/create', methods = ["post"])
def create_author():
    #creates a new __ from the client side and stores in the db
    if not Author.validate_author(request.form):
        return redirect('/')
    new_author_data = { **request.form}
    Author.create(new_author_data)
    return redirect('/')

@app.route('/author/<int:id>')
def author_show_one(id):

    author_id = {
        "id": id
    }
    #grabs all existing in the db
    all_books = Book.get_all()
    author = Author.get_one(author_id)
    
    authors_fav_books = Author.get_all_fav_books(author_id)
    fav_titles = []
    non_favorited =[]

    if authors_fav_books:
        for fav_book in authors_fav_books:
            fav_titles.append(fav_book.title)
            
        for book in all_books:
            if not book.title in fav_titles:
                non_favorited.append(book)
                    
    print(non_favorited)

    if not non_favorited:
        non_favorited = all_books


    return render_template("author_page.html", author = author, non_favs = non_favorited, authors_fav_books= authors_fav_books )

@app.route('/favorites/add/<int:id>', methods=["POST"])
def add_favorite(id):

    data = {
        "book_id": request.form['book_id'],
        "author_id": id
    }

    Author.add_new_book(data)

    return redirect(f"/author/{id}" )

@app.route('/author/<int:id>/edit')
def author_edit(id):
    return render_template("author_edit.html")

@app.route('/author/<int:id>/update', methods = ['POST'])
def update_author(id):
    #deletes the target instance
    if not Author.validate_author(request.form):
        return redirect('/')
    updated_author_data = { **request.form}
    ## add an id w/ id argument
    Author.update_author(updated_author_data)
    print(updated_author_data)
    return redirect('/')

@app.route('/author/<int:id>/delete')
def delete_author(id):
    #deletes the target instance
    deleted_author_data = {
        "id": id
    }
    Author.delete_author(deleted_author_data)
    print(deleted_author_data)
    return redirect("/")
