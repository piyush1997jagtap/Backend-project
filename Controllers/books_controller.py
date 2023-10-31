import flask
from flask import request, send_file
from app import app
from Models.auth_model import auth_model
from Models.book_model import book_model
import os
from datetime import datetime
bookObject = book_model()
auth = auth_model()

@app.route("/books/all")
def get_all_books():
    return bookObject.get_all_books_data()

@app.route("/book/add", methods=["POST"])
@auth.token_auth()
def add_book():
    return bookObject.add_book_data(request.form)

@app.route("/book/delete/<id>", methods=["DELETE"])
def delete_book(id):
    print(request.form)
    print(id)
    return bookObject.delete_book_data(id)

@app.route("/book/update/<id>", methods=["PUT"])
def update_book(id):
    print(request.form)
    return bookObject.update_book_data(request.form, id)