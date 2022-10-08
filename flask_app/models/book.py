from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from .. import DATABASE
from flask_app.models import author
# we are creating an object called bcrypt, which is made by invoking the function Bcrypt with our app as an argument
#regex 




# model.py, however many tables you have is however many models you need

#Necessary if importing another Class to be referenced 
# from flask_app.models import (child_model file)
# Example
# from flask_app.models.ninja import Ninja

# Things to change:
# Table_Class_Name
# books lowercase
# book lowercase
# (scehma_name)


class Book():
    #these should be the same as the columns in the table
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_pages = data['num_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # We create a list so that later we can add in all the burgers that are associated with a restaurant.
        # self.ninjas = []

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO books ( title , num_pages, created_at , updated_at ) VALUES (%(title)s, %(num_pages)s, NOW(),NOW());"

        # users query
        # query = "INSERT INTO users (username, password) VALUES (%(username)s, %(password)s);"
        new_book_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_book_id
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        #returns a list of dicts
        list_of_books_dicts_from_db = connectToMySQL(DATABASE).query_db(query)

        if not list_of_books_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_books_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for book_dict in list_of_books_dicts_from_db:
            list_of_books_instances.append(cls(book_dict))
        return list_of_books_instances

    @classmethod
    def get_all_except(cls, data):
        query = "SELECT books.title FROM books LEFT JOIN favorites ON favorites.book_id = books.id WHERE id != %(author_id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        #returns a list of dicts
        list_of_books_dicts_from_db = connectToMySQL(DATABASE).query_db(query)

        if not list_of_books_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_books_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for book_dict in list_of_books_dicts_from_db:
            list_of_books_instances.append(cls(book_dict))
        return list_of_books_instances

    @classmethod
    def get_one(cls, data:dict):
        query = 'SELECT * FROM books WHERE id = %(id)s;'
        list_of_one_book_dict = connectToMySQL(DATABASE).query_db(query, data)
        if not list_of_one_book_dict:
            return False
        return cls(list_of_one_book_dict[0])

    @classmethod
    def get_all_fav_authors(cls, data:dict):
        query = 'SELECT authors.name, authors.id, authors.created_at, authors.updated_at FROM favorites RIGHT JOIN authors ON authors.id = favorites.author_id WHERE favorites.book_id = %(id)s;'
        list_of_all_authors_dicts_from_db = connectToMySQL(DATABASE).query_db(query, data)

        if not  list_of_all_authors_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_author_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for author_dict in  list_of_all_authors_dicts_from_db:
            list_of_author_instances.append(author.Author(author_dict))
        return list_of_author_instances
    
    @classmethod
    def add_new_author(cls, data:dict):
        query = 'INSERT INTO favorites ( book_id, author_id ) VALUES (%(book_id)s, %(author_id)s);'
        new_favorite_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_favorite_id

    @classmethod
    def delete_book(cls, data:dict):
        query = 'DELETE FROM books WHERE id = %(id)s;'
        book = connectToMySQL(DATABASE).query_db(query, data)
        return cls(book)

    @classmethod
    def update_book(cls, data:dict):
        query = 'UPDATE books SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id = %(id)s;'
        book = connectToMySQL(DATABASE).query_db(query, data)
        return cls(book)

    @staticmethod
    def validate_book(data:dict):
        is_valid = True

        if len(data['title']) < 1:
            flash("Title must be input to add", "book")
            is_valid = False
        if data['num_pages'] ==  "":
            flash("How many foo?", "book")
            is_valid = False
        return is_valid

