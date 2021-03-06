from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
import orm

app = Flask(__name__)
CORS(app)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='microblog', template_mode='bootstrap3')

from views import blueprints
for bp in blueprints: 
    app.register_blueprint(bp)    
