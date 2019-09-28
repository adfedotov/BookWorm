from flask import Blueprint, render_template, redirect, flash, url_for, session, g
from .models import User, db
from .forms import RegisterForm, LoginForm
from sqlalchemy.orm.exc import NoResultFound
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        if len(User.query.filter_by(email=form.email.data).all()) == 0:
            user = User(form.first_name.data, form.last_name.data, form.email.data)
            user.set_pass(form.password.data)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.login'))
        else:
            error = 'User with this email already exists'

    if error:
        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).one()
        except NoResultFound as e:
            error = 'User doesn\'t exist'
        else:
            if user.check_pass(form.password.data):
                session['user_id'] = user.uid
                return redirect(url_for('main.index'))
            else:
                error = 'Incorrect password'
    if error:
        flash(error)

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


@bp.before_app_request
def logedin_user():
    """
    When user connects, check if there is user_id in session. If there is one, we check if it's
    in the database and put uid, first name, last name into g, which is a global for the time of connection.
    """
    user_id = session.get('user_id')
    if user_id is not None:
        # g.user holds user_id, first_name, last_name
        user = User.query.get(user_id)
        if user:
            g.user = [user.uid, user.first_name, user.last_name]
    else:
        g.user = None


def login_required(view):
    """
    This decorator checks whether user is logged in. Returns normal view if yes, redirect to login page if not

    :param view:
    """
    @functools.wraps(view)
    def wrap(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrap
