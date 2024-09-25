from flask import render_template, redirect, url_for, flash
from . import app, db  # Import app and db from the current package
from .forms import RegistrationForm, LoginForm, GratitudeEntryForm
from .models import User, GratitudeEntry
from flask_login import login_user, logout_user, login_required, current_user

# Route for the home page
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return render_template('landing_page.html')  # Public-facing page


# Route for registering new users
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Route for logging in users
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

# Route for logging out users
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# Route for user dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    entries = GratitudeEntry.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', entries=entries)

# Route for adding a new gratitude entry
@app.route("/new_entry", methods=['GET', 'POST'])
@login_required
def new_entry():
    form = GratitudeEntryForm()
    if form.validate_on_submit():
        entry = GratitudeEntry(content=form.content.data, user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()
        flash('Your gratitude entry has been added!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html', form=form)
