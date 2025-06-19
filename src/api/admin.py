from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import db  
from models import User, Order, OrderItem, Product, CartItem , Favorite

class UserAdmin(ModelView):
    column_list = ('id', 'name', 'email', 'is_admin', 'created_at')

class OrderAdmin(ModelView):
    column_list = ('id', 'user_id', 'user.email', 'created_at', 'status', 'total_price')

class OrderItemAdmin(ModelView):
    column_list = ('id', 'order_id', 'order.user.email', 'product_id', 'product.name', 'quantity', 'unit_price', 'talla')

class ProductAdmin(ModelView):
    column_list = ('id', 'name', 'description', 'price', 'stock', 'image_url')

class CartItemAdmin(ModelView):
    column_list = ('id', 'user_id', 'user.email', 'product_id', 'product.name', 'quantity', 'talla', 'created_at')
class FavoriteAdmin(ModelView):
    column_list = ('id', 'user_id', 'user.email', 'product_id', 'product.name')

def setup_admin(app):
    app.config['SECRET_KEY'] = 'pon_aqui_tu_secret_key_segura'
    app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'
    admin = Admin(app, name='DATABASE', template_mode='bootstrap3')

    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(OrderAdmin(Order, db.session))
    admin.add_view(OrderItemAdmin(OrderItem, db.session))
    admin.add_view(ProductAdmin(Product, db.session))
    admin.add_view(CartItemAdmin(CartItem, db.session)) 
    admin.add_view(FavoriteAdmin(Favorite, db.session)) # Agregar vista para el modelo User