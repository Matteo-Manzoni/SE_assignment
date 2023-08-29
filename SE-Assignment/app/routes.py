from app import app, login, admin, db
from flask import render_template, flash, redirect, url_for, request, session, \
    g, current_app, abort, jsonify
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from app.forms import *
from app.models import users_tbl, meals_tbl, DbUser, user_meals
import sys
import os
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from shutil import copyfile

@login.user_loader
def load_user(id):
    user = users_tbl.query.get(int(id))
    if user:
        return DbUser(user)
    else:
        return None

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html', title='home', page='home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # checks if the user is authenticated , if they are it redirects the user
    # to the index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    # checks the form validation, if the user does not validate it returns
    # them to the login page and tells them invalid password or username
    if form.validate_on_submit():
        check_user = users_tbl.query.filter_by(email=form.email.data).first()
        user = DbUser(check_user)

        if check_user is None or not user.check_password(form.password.data):
            app.logger.warning('User fail to validate')
            flash('Invalid username or password')

            return redirect(url_for('login'))
        if not user.active:

            db.session.commit()

        # logs in the user sets them as active and directs them to the page
        # they tried to access if not it directs them to the index page
        if form.remember_me.data:
            login_user(user, remember=True)
        else:
            login_user(user, remember=False)

        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In',
                           form=form, page='login')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Logs user out
    """
    logout_user()
    flash('You have logged out')

    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = users_tbl(name=form.name.data, email=form.email.data,date_of_birth=form.date_of_birth.data, user_type="STANDARD")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    form = QuestionnaireForm()

    if form.validate_on_submit():
        cur_id = current_user.get_id()
        cooking_time_list = [30]
        if form.cooking_time.data == "60 or less":
            cooking_time_list.append(60)
        if form.meal_constraints.data == "None":
            suitable_meals = meals_tbl.query.filter(meals_tbl.cooking_time.in_(cooking_time_list)).all()

        else:
            suitable_meals = meals_tbl.query.filter(meals_tbl.cooking_time.in_(cooking_time_list)).filter_by(meal_type=str(form.meal_constraints.data)).all()

        user_meals.query.filter_by(user_id=cur_id).delete()
        for meal in suitable_meals:
            new_user_meal = user_meals(user_id=cur_id, meal_id=meal.id)
            db.session.add(new_user_meal)
            db.session.commit()

        return redirect(url_for('meal_planner'))
    return render_template('preferences.html', form=form, title='Preferences')


@app.route('/meals', methods=['GET', 'POST'])
@login_required
def meal_browser():
    meals = meals_tbl.query.all()

    return render_template("meal plans.html", meals=meals, title='Meal browser', page="meals")


@app.route('/meal_plan', methods=['GET', 'POST'])
@login_required
def meal_planner():
    user_meals_query = user_meals.query.filter_by(user_id=current_user.get_id()).all()
    if user_meals_query:
        meal_id_list = []
        for meal in user_meals_query:
            meal_id_list.append(meal.meal_id)

        meals = meals_tbl.query.filter(meals_tbl.id.in_(meal_id_list)).all()
    else:
        flash("You must generate a meal plan before accessing this page, you can do so on this page")
        return redirect(url_for("preferences"))
    return render_template("meal plans.html", meals=meals, title='Meal planner', page="meal planner")


@app.route('/user_details/<user>', methods=['GET','POST'])
@login_required
def get_user_details(user):
    """
    fetches the details of an user to fill in form data when updating that user
    """
    if user and user == current_user._user.email:
        cur_user = users_tbl.query.filter_by(id=user).first()

        UserObj = {}

        UserObj['user_name'] = cur_user.name
        UserObj['user_email'] = cur_user.email
        UserObj['user_date_of_birth'] = cur_user.date_of_birth.strftime("%Y-%m-%d")

        return jsonify(UserObj)
    else:
        return "None"


@app.route("/update_details", methods=['Get', 'POST'])
@login_required
def update_details():

    form = UpdateUser()
    if current_user.is_authenticated:
        form.user_name.data = current_user._user.name
        form.user_email.data = current_user._user.email
        if not form.user_date_of_birth.data:
            form.user_date_of_birth.data = current_user._user.date_of_birth
        if form.validate_on_submit():
            cur_user = users_tbl.query.filter_by(id=current_user._user.id).first()
            cur_user.name = form.user_name.data
            if form.user_new_email.data:
                cur_user.email = form.user_new_email.data
            if form.user_new_name.data:
                cur_user.name = form.user_new_name.data

            cur_user.date_of_birth = form.user_date_of_birth.data
            db.session.commit()
            flash("User details have been updated")
            return redirect(url_for("index"))



        return render_template('edit_details.html', form=form, page='Update details')




