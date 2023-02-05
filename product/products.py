from flask import Blueprint, render_template
from ecommerce.models import Product

products_bp = Blueprint('products_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')

@products_bp.route('/')
def list():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@products_bp.route('/view/<int:product_id>')
def view(product_id):
    product = Product.query.get(product_id)
    return render_template('products/view.html', product=product)
