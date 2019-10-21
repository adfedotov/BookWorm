from flask import Blueprint, render_template, redirect, url_for, g, request
from ..auth.controllers import login_required
from ..auth.models import User
from .models import db, Note, GoodReadsAPI
from .forms import EditNote, EditProfile
from sqlalchemy.orm.exc import NoResultFound

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
@login_required
def dashboard():
    cards = []
    user_notes = Note.get_user_notes(g.user[0])
    for note in user_notes:
        card_info = GoodReadsAPI().get_book(note.bid)
        if len(card_info) == 0:
            continue
        card_info['last_update'] = note.last_update.strftime('%m/%d/%Y')
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
    db.session.delete(note)
    db.session.commit()

    return redirect(url_for('dashboard.dashboard'))


@bp.route('/profile/', methods=['GET', 'POST'])
@bp.route('/profile/<int:uid>', methods=['GET', 'POST'])
@login_required
def profile(uid=None):
    if not uid:
        uid = g.user[0]

    user = User.query.get(uid)
    
    if not user:
        return redirect(url_for('main.index'))
    
    own_profile = False
    if uid == g.user[0]:
        own_profile = True

    form = EditProfile()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        db.session.commit()
        return redirect(url_for('dashboard.profile'))

    print(f'Accessed profile id: {uid}')
    return render_template('dashboard/profile.html', user=user, own_profile=own_profile, form=form)

