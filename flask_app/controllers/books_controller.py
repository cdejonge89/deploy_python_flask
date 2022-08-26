from flask_app import app
from flask import render_template, redirect, session, request, flash, jsonify
from flask_app.models.user_model import User
from flask_app.models.book_model import Books 

# CREATE PAGE 
@app.route('/quote/create')
def create():
    if not "user_id" in session:
        return redirect('/quote/login')
    # this shows the user's name in the books list page
    user = User.get_by_id({'id':session['user_id']})
    return render_template("create.html", user=user)

# ADD A BOOK TO THE LIST
@app.route('/books/create', methods=['POST'])
def add_to_list():
    # needs to be logged in to see this page
    if not "user_id" in session:
        return redirect('/quote/login')
    # validating the form has been filled in
    if not Books.validator(request.form):
        return redirect('/quote/create')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Books.create(data)
    return redirect('/quote/create')

# EDIT
@app.route('/books/<int:id>/edit')
def edit_book_list(id):
    if not "user_id" in session:
        return redirect('/quote/login')
    book = Books.get_book_by_id({'id': id})
    return render_template("edit.html", book=book)
    
# PROCESES THE EDIT ROUTE TO UPDATE
@app.route('/books/<int:id>/update', methods=['POST'])
def update_book_list(id):
    if not "user_id" in session:
        return redirect('/quote/login')
    if not Books.validator(request.form):
        return redirect(f'/books/{id}/edit')
    data = {
        **request.form,
        'id': id
    }
    Books.update(data)
    return redirect('/quote/create')

# ADD BOOK FROM API
@app.route('/api/books/add', methods=['POST']) 
def add_book_api():
    if not "user_id" in session:
        return redirect('/quote/login')
    data = {
        'title': request.form['title'],
        'author': request.form['author'],
        'user_id': session['user_id']
    }
    Books.create(data)
    return redirect('/quote/create')

# API TO CREATE A BOOK FOR THE LIST
@app.route('/api/books/create', methods=['POST'])
def api_add_to_list():
    # needs to be logged in to see this page
    if not "user_id" in session:
        return redirect('/quote/login')
    print(request.form)
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    book_id = Books.create(data)
    res = {
        'msg': 'success',
        'form': data,
        'book_id': book_id
    }
    return jsonify(res)


# DELETES THE BOOK FROM THE LIST
@app.route("/books/<int:id>/delete")
def delete_book(id):
    if not "user_id" in session:
        return redirect('/quote/login')
    data = {
        'id': id
    }
    to_be_deleted = Books.get_by_id(data)
    # if not session['user_id'] == to_be_deleted.user_id:
    #     flash("You can't delete this book")
    #     return redirect('/quote/login')
    Books.delete(data)
    return redirect('/quote/create')
    
# shows the user their book list
@app.route('/my_book_list')
def my_book_list():
    if not "user_id" in session:
        return redirect('/quote/login')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('create.html', user=user)
