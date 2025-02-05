from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User
# to secure a password so that it is never stored in plain text
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  #means from __init__.py import db

#we needed the usermixin in models so we can use flasks current user attricute
from flask_login import login_user, login_required, logout_user, current_user
 
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"Email: {email}, Password: {password}") # debugging line

        #what you do when you are looking for a specific entry to the database
        user = User.query.filter_by(email=email).first() # returns the first result

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category ='success ')
                login_user(user, remember=True) #the remember is so that user does not have to login every single time unless server restrats
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password.', category ='error')
        else:
            flash('email does not exist', category = 'error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required # makes sure we cannot access this page unless user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters', category='error')
        else:
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
            print(f"Generated Hash: {hashed_password}")
            new_user = User(email=email, firstName=firstName, password = hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created', category = "success")
            return redirect(url_for('views.home'))

        
    return render_template("sign_up.html", user=current_user)
