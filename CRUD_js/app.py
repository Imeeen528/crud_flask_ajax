from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Product %r>' % self.name


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/products/new', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        product = Product(name=name, price=price, description=description)
        db.session.add(product)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product created'})
    return render_template('create.html')


@app.route('/products/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product updated'})
    return render_template('edit.html', product=product)


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Product deleted'})


if __name__ == '__main__':
    app.run(debug=True)
