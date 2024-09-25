from flask import render_template, redirect, url_for, flash, request
from . import app, db  # Import app and db from the current package
from .forms import RegistrationForm, LoginForm, GratitudeEntryForm
from .models import User, GratitudeEntry
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        entries = GratitudeEntry.query.all()
        return render_template('index.html', entries=entries)


# Route for registering new users
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Create a RegistrationForm similar to LoginForm
    if form.validate_on_submit():
        new_user = User(email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Route for logging in users
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Make sure this is your form for login
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):  # Ensure you have a verify_password method
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')  # Get the 'next' parameter
            return redirect(next_page or url_for('dashboard'))  # Redirect to the next page or dashboard
        else:
            flash('Login failed. Check your email and password.', 'danger')
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

