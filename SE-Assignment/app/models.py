from app import db, admin
import sqlalchemy as sqa
from flask_admin.contrib.sqla.form import QuerySelectField, \
    QuerySelectMultipleField
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from werkzeug.security import generate_password_hash,  check_password_hash
from sqlalchemy.orm import relationship, object_session
from wtforms import Form
import os
import sys


class users_tbl(db.Model):

    __table__ = db.Model.metadata.tables['users']

    def set_password(self, password):
        self.password = generate_password_hash(password)


class DbUser(object):
    """Wraps User object for Flask-Login and added functionality for permissions and dynamic forms"""

    def __init__(self, user):
        self._user = user
        self.active = False

    def get_id(self):
        return self._user.id

    def is_active(self):
        return self.active

    def is_anonymous(self):

        return False

    def is_authenticated(self):
        return True

    def has_admin(self):
        if self._user.user_type == "ADMIN":
            return True

    def check_password(self, password):
        return check_password_hash(self._user.password, password)

    def __repr__(self):
        return '<User {}, email {}>'.format(self._user.name, self._user.email)


class meals_tbl(db.Model):

    __table__ = db.Model.metadata.tables['meals']


class user_meals(db.Model):

    __table__ = db.Model.metadata.tables['user_meals']


class MyModelView(ModelView):
    # only gives admins permission to access certain pages
    can_delete = True
    can_edit = True
    column_display_pk = True
    column_hide_backrefs = False
    can_search = True
    can_export = True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('index'))

    def is_accessible(self):
        try:
            if current_user.get_role() == "Manager" or current_user.get_role() == "Technician":
                return current_user.is_authenticated
            else:
                return False
        except AttributeError:
            return self.inaccessible_callback(name='')


class MyModelAdminView(ModelView):
    # only gives admins permission to access certain pages

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('index'))

    def is_accessible(self):
        try:
            return True
        except AttributeError:
            return self.inaccessible_callback(name='')

admin.add_view(MyModelView(users_tbl, db.session))
admin.add_view(MyModelView(meals_tbl, db.session))
admin.add_view(MyModelView(user_meals, db.session))



