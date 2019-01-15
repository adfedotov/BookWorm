from flask import Blueprint, render_template, request, session, url_for, redirect, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegisterForm, LoginForm
from .controllers import register_user, check_registered, check_password, get_userid, get_user
from ..db import close_db
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        if not check_registered(form.email.data):
            register_user(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            return redirect(url_for('auth.login'))
        else:
            error = "User with this email has already been registered"
            flash(error)
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if check_registered(form.email.data):
            if check_password(form.email.data, form.password.data):
                session.clear()
                session['user_id'] = get_userid(form.email.data)
                return redirect(url_for('main.index'))
            else:
                error = "Incorrect Password"
                flash(error)
        else:
            error = "Incorrect Email"
            flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    close_db()
    return redirect(url_for('main.index'))

@bp.before_app_request
def loggedin_user():
    user_id = session.get('user_id')
    if user_id is not None:
        # g.user holds user_id, first_name, last_name. g.user[i] to access
        g.user = get_user(user_id)
    else:
        g.user = None

def login_required(view):
    '''This decorator checks whether user is logged in. Returns normal view if yes, redirect to login page if no'''
    @functools.wraps(view)
    def wrap(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrap
