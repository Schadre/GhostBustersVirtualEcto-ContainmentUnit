from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from functools import wraps 
from app import app 
from app.forms import LoginForm
from app.models import UserRole, Ghostbusters, Ghosts

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            print("User not authenticated")
            flash("Admin access required. Please log in.", "warning")
            return redirect(url_for('adminlogin'))

        if getattr(current_user, 'role', None) != UserRole.ADMIN:
            flash('Admin access required')
            return redirect(url_for('adminlogin'))
        print("Access granted to admin")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@app.route('/VirtualEcto-ContainmentUnit')
def VirtualEctoContainmentUnit():
    ghosts = Ghosts.query.all() 
    return render_template('/VirtualEcto-ContainmentUnit.html', ghosts=ghosts)

@app.route('/ghost_detail')
def ghost_detail():
    ghost = Ghosts.query.all()
    return render_template('/ghost_detail.html', ghost=ghost)

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    form = LoginForm()
    if form.validate_on_submit():
        user = Ghostbusters.query.filter_by(username=form.username.data).first()
        if user and user.role == UserRole.ADMIN:
            login_user(user, remember=form.remember_me.data)
            flash('Login successful')
            return redirect(url_for('add_ghost'))
        else:
            flash("Invalid credentials or not an admin")
    return render_template('adminlogin.html', form=form)

@app.route('/add_ghost')
@admin_required
def add_ghost():
    return render_template('/add_ghost.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return "Welcome to the Admin Dashboard"
    
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    error_code = error.code
    error_message = error.description
    return render_template('Error.html', error_code=error_code, error_message=error_message), error_code