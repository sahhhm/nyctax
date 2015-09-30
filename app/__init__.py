from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import filters

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

#from filters.py
app.register_blueprint(filters.blueprint)

from app import views, models

admin = Admin(app, name='nyctax', template_mode='bootstrap3')
# Add administrative views here

admin.add_view(ModelView(models.Status, db.session))
admin.add_view(ModelView(models.Frequency, db.session))
admin.add_view(ModelView(models.Year, db.session))
admin.add_view(ModelView(models.Entry, db.session))
admin.add_view(ModelView(models.Level, db.session))
admin.add_view(ModelView(models.Medicare, db.session))
admin.add_view(ModelView(models.SocialSecurity, db.session))
admin.add_view(ModelView(models.Allowance, db.session))
admin.add_view(ModelView(models.Withholding, db.session))
