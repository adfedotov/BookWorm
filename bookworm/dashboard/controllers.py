from flask import Blueprint, render_template, redirect, flash, url_for, g
from ..auth.controllers import login_required
from .models import db, Note, GoodReadsAPI
from .forms import EditNote

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
@login_required
def dashboard():
    cards = []
    user_notes = Note.get_user_notes(g.user[0])
    for note in user_notes:
        card_info = GoodReadsAPI().get_book(note.bid)
        card_info['last_update'] = note.last_update.strftime('%m/%d/%Y')  # TODO: Logic
        card_info['bid'] = note.bid
        cards.append(card_info)
    return render_template('dashboard/dashboard.html', cards=cards)


@bp.route('/search')
@bp.route('/search/<query>')
@login_required
def book_search(query=None):
    if query:
        books = GoodReadsAPI().book_search(query)
        return render_template('dashboard/search.html', books=books, query=query)

    return render_template('dashboard/search.html', books=None, query=None)


@bp.route('/view/<bid>', methods=['GET', 'POST'])
@login_required
def note_view(bid):
    note = Note.get_note(g.user[0], bid)
    if note is None:
        return 'Note doesn\t exist'

    book = GoodReadsAPI().get_book(bid)
    return render_template('dashboard/view.html', book=book, note=note, bid=bid)


@bp.route('/edit/<bid>', methods=['GET', 'POST'])
@login_required
def note_edit(bid):
    note = Note.get_note(g.user[0], bid)
    if note is None:
        note = Note(g.user[0], bid)
        note.set_note('')
        note.update_date()
        db.session.add(note)
        db.session.commit()

    form = EditNote()
    if form.validate_on_submit():
        note.set_note(form.text.data)
        note.update_date()
        db.session.commit()
        return redirect(url_for('dashboard.note_view', bid=bid))
    book = GoodReadsAPI().get_book(bid)
    return render_template('dashboard/edit.html', book=book, form=form,
                           note=note, bid=bid)


@bp.route('/delete/<bid>')
@login_required
def note_delete(bid):
    note = Note.get_note(g.user[0], bid)
    if note is None:
        return '404'

    db.session.remove(note)
    db.commit()

    return redirect(url_for('dashboard.dashboard'))
