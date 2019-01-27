from flask import Blueprint, render_template, request, session, g
from ..auth import login_required
import json
from .controllers import get_user_books, get_book_info, note_exists, save_note
from .forms import CreateNote

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def dashboard():
    books = []
    book_list = get_user_books(session.get('user_id'))
    for olid in book_list:
        book_info = get_book_info(olid[0])
        books.append([olid, book_info['title'], book_info['authors'][0]['name'], book_info['cover']['medium']])
    # think about putting json requests stuff here instead of user end
    return render_template('dashboard/dashboard.html', books=books)

@bp.route('/create')
@login_required
def dashboard_book_choice():
    return render_template('dashboard/bookchoice.html')

@bp.route('/create/<olid>', methods=['GET', 'POST'])
@login_required
def dashboard_create_note(olid):
    if note_exists(g.user[0], olid):
        return 'Note Exists'
    else:
        print('Note doesn\'t exist')

    form = CreateNote()
    if form.validate_on_submit():
        print(form.text.data)
        save_note(g.user[0], olid, form.text.data)
        return 'Saved' + form.text.data
    book_info = get_book_info(olid)
    # we need to check if note was already created and redirect to note display
    return render_template('dashboard/createnote.html', book_info=book_info, form=form)
