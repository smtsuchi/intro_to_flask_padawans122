from flask import render_template, request, redirect, url_for, flash
from app import app
from .forms import LoginForm, SignUpForm
from .models import User, db
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
## AUTHENTICATION

@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            
            # find user from the db
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('ig.home_page'))
                else:
                    flash('Incorrect username/password.', 'danger')
            else:
                flash('Incorrect username.', 'danger')
        else:
            flash('An error has occurred. Please submit a valid form', 'danger')           
            
    return render_template('login.html', form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            #add user to database
            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()
            flash('Successfully created user.', 'success')
            return redirect(url_for('login_page'))
        flash('An error has occurred. Please submit a valid form', 'danger')

    return render_template('signup.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

