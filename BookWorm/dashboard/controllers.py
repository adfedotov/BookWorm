from ..db import get_db
import json
import requests

def get_user_books(user_id):
    conn = get_db()
    cur = conn.cursor()
    # No need to filter results for now
    cur.execute(
    '''
    SELECT note_id, isbn FROM notes
    WHERE user_id = (%s)
    ''', (user_id,)
    )
    return cur.fetchall()

def get_book_info(olid):
    book_code = 'OLID:' + olid
    response = requests.get(f'https://openlibrary.org/api/books?bibkeys={book_code}&jscmd=data&format=json').json()
    return response[book_code]
