from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.book import Book
from .. import DATABASE




# model.py, however many tables you have is however many models you need

#Necessary if importing another Class to be referenced 
# from flask_app.models import (child_model file)
# Example
# from flask_app.models.ninja import Ninja

# Things to change:
# Table_Class_Name
# authors lowercase
# author lowercase
# (scehma_name)


class Author(Book):
    #these should be the same as the columns in the table
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # We create a list so that later we can add in all the burgers that are associated with a restaurant.
        # self.ninjas = []

    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO authors ( name , created_at , updated_at ) VALUES (%(name)s,NOW(),NOW());"

        # users query
        # query = "INSERT INTO users (username, password) VALUES (%(username)s, %(password)s);"
        new_author_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_author_id
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        #returns a list of dicts
        list_of_authors_dicts_from_db = connectToMySQL(DATABASE).query_db(query)

        if not list_of_authors_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_authors_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for author_dict in list_of_authors_dicts_from_db:
            list_of_authors_instances.append(cls(author_dict))
        return list_of_authors_instances

    @classmethod
    def get_one(cls, data:dict):
        query = 'SELECT * FROM authors WHERE id = %(id)s;'
        list_of_one_author_dict = connectToMySQL(DATABASE).query_db(query, data)
        if not list_of_one_author_dict:
            return False
        return cls(list_of_one_author_dict[0])

    @classmethod
    def add_new_book(cls, data:dict):
        query = 'INSERT INTO favorites ( book_id, author_id ) VALUES (%(book_id)s, %(author_id)s);'
        new_favorite_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_favorite_id

    @classmethod
    def get_all_fav_books(cls, data:dict):
        query = 'SELECT books.title, books.num_pages, books.id, books.created_at, books.updated_at FROM favorites RIGHT JOIN books ON books.id = favorites.book_id WHERE favorites.author_id = %(id)s;'
        list_of_all_books_dicts_from_db = connectToMySQL(DATABASE).query_db(query, data)

        if not  list_of_all_books_dicts_from_db:
            return False
        # Create an empty list to append our instances of friends
        list_of_book_instances = []
        # Iterate over the db results and create instances of friends with cls.
        for book_dict in  list_of_all_books_dicts_from_db:
            list_of_book_instances.append(Book(book_dict))
        return list_of_book_instances

    @staticmethod
    def validate_author(data:dict):
        is_valid = True

        if len(data['name']) < 1:
            flash("Name must be input to add", "author")
            is_valid = False
        return is_valid

