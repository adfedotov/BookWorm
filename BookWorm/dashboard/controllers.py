from ..db import get_db
import json
import requests
import datetime

def get_user_books(user_id):
    conn = get_db()
    cur = conn.cursor()
    # No need to filter results for now
    cur.execute(
    '''
    SELECT olid FROM notes
    WHERE user_id = (%s)
    ''', (user_id,)
    )
    return cur.fetchall()

def get_book_info(olid):
    book_code = 'OLID:' + olid
    response = requests.get(f'https://openlibrary.org/api/books?bibkeys={book_code}&jscmd=data&format=json').json()
    return response[book_code]

def save_note(user_id, olid, note):
    conn = get_db()
    cur = conn.cursor()
    dt = datetime.datetime.now()
    print(dt, type(dt))
    cur.execute(
    '''
    INSERT INTO notes (user_id, olid, note, last_update)
    VALUES (%s, %s, %s, %s)
    ''', (user_id, olid, note, dt)
    )
    conn.commit()

def note_exists(user_id, olid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
    '''
    SELECT note_id FROM notes
    WHERE user_id = (%s) AND olid = (%s)
    ''', (user_id, olid)
    )
    if cur.fetchone() is None:
        return False
    else:
        return True
