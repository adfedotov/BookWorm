from flask import Blueprint, render_template, request, session
from ..auth import login_required
import json
from .controllers import get_user_books

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def dashboard():
    books = get_user_books(session.get('user_id'))
    print(books)
    return render_template('dashboard/dashboard.html', books=json.dumps(books))
