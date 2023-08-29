from flask import Flask, request, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager, current_user
from flask_admin.menu import MenuLink
from app.config import Config
import logging
import sys

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


login = LoginManager(app)
login.login_view = 'login'


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            # if current_user.has_subproduct_permission('GET_META'):
            #     return current_user.is_authenticated
            # else:
            #     return False
            return True
        except AttributeError:
            return self.inaccessible_callback(name='')

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for('home'))


class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for("index")


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_link(MainIndexLink(name="Main Page"))

from app import routes, models