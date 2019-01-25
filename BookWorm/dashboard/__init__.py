from flask import Blueprint, render_template, request, session
from ..auth import login_required
import json
from .controllers import get_user_books
from .forms import CreateNote

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html', books=json.dumps(get_user_books(session.get('user_id'))))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def dsahboard_create():
    form = CreateNote()
    if form.validate_on_submit():
        pass
    return render_template('dashboard/create.html', form=form)
