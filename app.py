from flask import request, jsonify, make_response
from model_wrappers import books_wrapper, authors_wrapper, subs_wrapper, loans_wrapper, \
    subscriptions_wrapper, categories_wrapper, book_types_wrapper

# enable CORS
from models import app
from flask_cors import cross_origin


# @app.route('/login', methods=['POST'])
# @cross_origin()
# def login():
#     if request.json is None:
#         return make_response(), 401
#     token = request.json.get('token')
#     try:
#         idinfo = id_token.verify_oauth2_token(token, grequests.Request(), Auth.CLIENT_ID)
#     except ValueError:
#         print('Invalid google login!')
#         return make_response(), 401
#     except Exception:
#         print('Something went wrong with the connection')
#         return make_response(), 500
#
#     if idinfo['email'] not in ['amishosh@gmail.com', 'shoshi611@gmail.com']:
#         return make_response(), 403
#
#     return make_response(json.dumps(idinfo)), 200


@app.route('/books', methods=['GET', 'POST'])
@cross_origin()
def books():
    if request.method == 'GET':
        books = books_wrapper.get_all()
        return jsonify(books)
    elif request.method == 'POST':
        book = request.json
        if not books_wrapper.valid(book) or not authors_wrapper.valid(book['author']):
            return make_response(), 400
        new_book = books_wrapper.add(book)
        return jsonify(new_book['id'])


@app.route('/books/<id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def books_single(id):
    if request.method == 'GET':
        book = books_wrapper.get_by_id(id)
        return jsonify(book)
    if request.method == 'PUT':
        book = request.json
        books_wrapper.update(id=id, updated_item=book)
        return make_response(), 200
    if request.method == 'DELETE':
        books_wrapper.delete(id)
        return make_response(), 200


@app.route('/subscribers', methods=['GET', 'POST'])
@cross_origin()
def subscribers():
    if request.method == 'GET':
        subs = subs_wrapper.get_all()
        return jsonify(subs)
    elif request.method == 'POST':
        subscriber = request.json
        if not subs_wrapper.valid(subscriber):
            return make_response(), 400
        subs_wrapper.add(subscriber)
        return make_response(), 201


@app.route('/subscriptions', methods=['GET', 'POST'])
@cross_origin()
def subscriptions():
    if request.method == 'GET':
        subscriptions = subscriptions_wrapper.get_all()
        return jsonify(subscriptions)
    elif request.method == 'POST':
        subscription = request.json
        if not subscriptions_wrapper.valid(subscription):
            return make_response(), 400
        sub = subscriptions_wrapper.add(subscription)
        return jsonify(sub)


@app.route('/subscriptions/<id>', methods=['GET'])
@cross_origin()
def subscriptions_single(id):
    if request.method == 'GET':
        subscription = subscriptions_wrapper.get_by_id(id)
        return jsonify(subscription)


@app.route('/loans', methods=['GET', 'POST'])
@cross_origin()
def loans():
    if request.method == 'GET':
        if request.args:
            loans = loans_wrapper.search(**request.args)
        else:
            loans = loans_wrapper.get_all()
        return jsonify(loans)
    elif request.method == 'POST':
        loan = request.json
        if not loans_wrapper.valid(loan):
            pass
        loans = loans_wrapper.add(loan)
        return jsonify(loans)


@app.route('/loans/<id>', methods=['GET', 'DELETE', 'PUT'])
@cross_origin()
def loans_single(id):
    if request.method == 'GET':
        loans = loans_wrapper.get_by_id(id)
        return jsonify(loans)
    if request.method == 'DELETE':
        loans_wrapper.delete(id)
        return make_response(), 200
    if request.method == 'PUT':
        loans_wrapper.update(id)
        return make_response(), 200


@app.route('/subscribers/<id>', methods=['GET', 'PUT'])
@cross_origin()
def single_subscriber_data(id):
    if request.method == 'GET':
        sub = subs_wrapper.get_by_id(int(id))
        return jsonify(sub)
    if request.method == 'PUT':
        subscriber = request.json
        subs_wrapper.update(id=id, updated_item=subscriber)

        return make_response(), 200


@app.route('/subscribers/<id>/extend', methods=['POST'])
@cross_origin()
def single_subscriber_extend(id):
    if request.method == 'POST':
        subscription = request.json
        subs_wrapper.extend(id=id, subscription=subscription)

        return make_response(), 200


@app.route('/categories', methods=['GET', 'POST'])
@cross_origin()
def categories():
    if request.method == 'GET':
        categories = categories_wrapper.get_all()
        return jsonify(categories)
    elif request.method == 'POST':
        category = request.json
        if not categories_wrapper.valid(category):
            return make_response(), 400
        category = categories_wrapper.add(category)
        return jsonify(category['id'])


@app.route('/categories/<id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def category(id):
    if request.method == 'GET':
        category = categories_wrapper.get_by_id(id)
        return jsonify(category)
    if request.method == 'PUT':
        category = request.json
        try:
            categories_wrapper.update(id=id, updated_item=category)
        except Exception as _:
            return make_response(), 500

        return make_response(), 200
    if request.method == 'DELETE':
        try:
            categories_wrapper.delete(id)
        except Exception as _:
            return make_response(), 500

        return make_response(), 200


@app.route('/book_types', methods=['GET', 'POST'])
@cross_origin()
def book_types():
    if request.method == 'GET':
        types = book_types_wrapper.get_all()
        return jsonify(types)
    elif request.method == 'POST':
        book_type = request.json
        if not book_types_wrapper.valid(book_type):
            return make_response(), 400
        book_type = book_types_wrapper.add(book_type)
        return jsonify(book_type['id'])

    return make_response(), 200


@app.route('/book_types/<id>', methods=['GET', 'PUT'])
@cross_origin()
def book_type(id):
    if request.method == 'PUT':
        book_type = request.json
        if not book_types_wrapper.valid(book_type):
            return make_response(), 400
        try:
            book_types_wrapper.update(id=id, updated_item=book_type)
        except Exception as _:
            return make_response(), 500

        return make_response(), 200


if __name__ == '__main__':
    app.run()
