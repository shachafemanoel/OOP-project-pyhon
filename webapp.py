from flask import Flask, render_template, request, redirect, url_for, session
from Store.store import Store

app = Flask(__name__)
app.secret_key = "change-me"

store = Store()
store.load_files()


def get_cart():
    return session.setdefault('cart', {})


@app.route('/')
def index():
    return render_template('index.html', products=store.collection.items())


@app.route('/add/<product_id>')
def add_to_cart(product_id):
    if product_id in store.collection:
        cart = get_cart()
        cart[product_id] = cart.get(product_id, 0) + 1
        session['cart'] = cart
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    cart_data = []
    total = 0
    cart = get_cart()
    for key, qty in cart.items():
        product = store.collection.get(key)
        if product:
            cart_data.append({'product': product, 'quantity': qty})
            total += product.price * qty
    return render_template('cart.html', items=cart_data, total=total)


@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        data = {
            'user_id': request.form.get('user_id'),
            'user_full_name': request.form.get('user_full_name'),
            'password': request.form.get('password'),
        }
        try:
            user = store.add_user(data)
            session['user_id'] = user.user_id
            session['user_name'] = user.user_full_name
            return redirect(url_for('index'))
        except Exception as e:
            error = str(e)
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        try:
            user = store.log(user_id, password)
            session['user_id'] = user.user_id
            session['user_name'] = user.user_full_name
            return redirect(url_for('index'))
        except Exception as e:
            error = str(e)
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
