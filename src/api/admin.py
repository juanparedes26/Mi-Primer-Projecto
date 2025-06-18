from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import db  
from models import User

class UserAdmin(ModelView):
    column_list = ('id', 'email', 'name')  # Asegúrate de incluir 'id' aquí

def setup_admin(app):
    # set optional bootswatch theme
    app.config['SECRET_KEY'] = '1005872250' 
    app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'
    admin = Admin(app, name=' DATABASE', template_mode='bootstrap3')
 
    admin.add_view(UserAdmin(User, db.session))