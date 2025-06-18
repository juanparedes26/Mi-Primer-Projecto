
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import db  
from models import User

def setup_admin(app):
    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    # Add administrative views here
    admin.add_view(ModelView(User, db.session))