from ..db import get_db
import json
import requests
import datetime

def get_user_books(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
    '''
    SELECT olid FROM notes
    WHERE user_id = (%s)
    ORDER BY last_update DESC
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
    cur.execute(
    '''
    INSERT INTO notes (user_id, olid, note, last_update)
    VALUES (%s, %s, %s, %s)
    ''', (user_id, olid, note, dt)
    )
    conn.commit()

def update_note(user_id, olid, note):
    conn = get_db()
    cur = conn.cursor()
    dt = datetime.datetime.now()
    cur.execute(
    '''
    UPDATE notes
    SET note = (%s), last_update = (%s)
    WHERE user_id = (%s) AND olid = (%s)
    ''', (note, dt, user_id, olid)
    )
    conn.commit()

def delete_note(user_id, olid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
    '''
    DELETE FROM notes
    WHERE user_id = (%s) AND olid = (%s)
    ''', (user_id, olid)
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

def get_note(user_id, olid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
    '''
    SELECT note FROM notes
    WHERE user_id = (%s) AND olid = (%s)
    ''', (user_id, olid)
    )
    return cur.fetchone()[0]
