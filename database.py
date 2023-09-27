from flask import Blueprint, request, jsonify
from extensions import db, app
from extensions import ma

database_app = Blueprint("database_app", __name__)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(10), nullable=False)

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'category')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@database_app.route('/product/add', methods=['POST'])
def addproduct():
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data or 'category' not in data:
            return jsonify({"error": "Invalid request data"}), 400
        name = data['name']
        existing_product = Product.query.filter_by(name=name).first()
        if existing_product:
            return jsonify({"error": "Product with this name already exists"}), 409
        price = data['price']
        category = data['category']

        if not isinstance(category, str):
            return jsonify({"error": "Invalid datatypes"}), 400
        new_product = Product(name=name, price=price, category=category)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"Message": "Your product has been added"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@database_app.route('/product', methods=['GET'])
def get_product():
    try:
        products = Product.query.all()
        result = products_schema.dump(products)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@database_app.route('/product/<int:id>', methods=['GET'])
def product_byid(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        data = product_schema.dump(product)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@database_app.route('/product/update/<id>', methods=['PUT'])
def update_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        data = request.get_json()
        if not data or 'name' not in data or 'price' not in data or 'category' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        product.name = data['name']
        product.price = data['price']
        product.category = data['category']

        db.session.commit()
        return jsonify({"message": "Product has been updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@database_app.route('/product/delete/<int:id>', methods=['DELETE'])
def deleteproduct_byid(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product has been deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
