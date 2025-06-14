from flask import Flask, jsonify, request
from flask_cors import CORS

from Store.store import Store
from Store.storeerror import StoreError

app = Flask(__name__)
CORS(app)

store = Store()
try:
    store.load_files()
except Exception:
    pass

@app.route('/api/products')
def get_products():
    products = []
    for prod in store.collection.values():
        products.append({
            'name': prod.name,
            'model': prod.model,
            'description': prod.description,
            'price': prod.price,
            'quantity': prod.quantity
        })
    return jsonify(products)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    user_id = data.get('user_id')
    password = data.get('password')
    try:
        user = store.log(user_id, password)
        return jsonify({'message': 'success', 'user_type': user.__class__.__name__})
    except StoreError.AuthenticationError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
