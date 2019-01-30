from flask import Blueprint, render_template, request, session, g, redirect, url_for
from ..auth import login_required
import json
from .controllers import get_user_books, get_book_info, note_exists, save_note, get_note, update_note, delete_note
from .forms import CreateNote, UpdateNote

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def dashboard():
    books = []
    book_list = get_user_books(session.get('user_id'))
    for olid in book_list:
        book_info = get_book_info(olid[0])
        books.append([olid[0], book_info['title'], book_info['authors'][0]['name'], book_info['cover']['medium']])
    return render_template('dashboard/dashboard.html', books=books)

@bp.route('/create')
@login_required
def book_choice():
    return render_template('dashboard/bookchoice.html')

@bp.route('/create/<olid>', methods=['GET', 'POST'])
@login_required
def note_create(olid):
    if note_exists(g.user[0], olid):
        return redirect(url_for('dashboard.note_view', olid=olid))
    form = CreateNote()
    if form.validate_on_submit():
        save_note(g.user[0], olid, form.text.data)
        return redirect(url_for('dashboard.note_view', olid=olid))
    book_info = get_book_info(olid)
    return render_template('dashboard/createnote.html', book_info=book_info, form=form)

@bp.route('view/<olid>')
@login_required
def note_view(olid):
    if not note_exists(g.user[0], olid):
        return 'Note doesn\t exist'
    book_info = get_book_info(olid)
    return render_template('dashboard/view.html', book_info=book_info, note=get_note(g.user[0], olid), olid=olid)

@bp.route('/edit/<olid>', methods=['GET', 'POST'])
@login_required
def note_edit(olid):
    if not note_exists(g.user[0], olid):
        return abort(404)
    form = UpdateNote()
    if form.validate_on_submit():
        update_note(g.user[0], olid, form.text.data)
        return redirect(url_for('dashboard.note_view', olid=olid))
    book_info = get_book_info(olid)
    return render_template('dashboard/edit.html', book_info=book_info, form=form, note=get_note(g.user[0], olid), olid=olid)

@bp.route('/delete/<olid>')
@login_required
def note_delete(olid):
    if not note_exists(g.user[0], olid):
        return abort(404)
    delete_note(g.user[0], olid)
    return redirect(url_for('dashboard.dashboard'))
