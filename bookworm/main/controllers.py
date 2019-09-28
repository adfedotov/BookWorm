from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/about')
def about():
    return render_template('main/about.html')


@bp.errorhandler(404)
def page_not_found(e):
    print('asdasdasdasdasd')
    return render_template('404.html'), e
