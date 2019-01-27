from flask import Blueprint, render_template, request, session
from ..auth import login_required
import json
from .controllers import get_user_books, get_book_info
from .forms import CreateNote

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def dashboard():
    # think about putting json requests stuff here instead of user end
    return render_template('dashboard/dashboard.html', books=json.dumps(get_user_books(session.get('user_id'))))

@bp.route('/create')
@login_required
def dashboard_book_choice():
    return render_template('dashboard/bookchoice.html')

@bp.route('/create/<olid>', methods=['GET', 'POST'])
@login_required
def dashboard_create_note(olid):
    form = CreateNote()
    if form.validate_on_submit():
        print(form.text.data)
    book_info = get_book_info(olid)
    # we need to check if note was already created and redirect to note display
    return render_template('dashboard/createnote.html', book_info=book_info, form=form)
