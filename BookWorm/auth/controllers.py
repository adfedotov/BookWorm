from ..db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

def register_user(f_name, l_name, email, password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
    '''
    INSERT INTO users (email, first_name, last_name, password)
    VALUES (%s, %s, %s, %s)
    ''', (email, f_name, l_name, generate_password_hash(password),)
    )
    conn.commit()

def check_registered(email):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT email FROM users WHERE email ILIKE (%s)', (email,))
    if cur.fetchone() is None:
        return False
    else:
        return True

def check_password(email, password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT password FROM users WHERE email ILIKE (%s)', (email,))
    return check_password_hash(cur.fetchone()[0], password)

def get_userid(email):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users WHERE email ILIKE (%s)', (email,))
    return cur.fetchone()

def get_user(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id, first_name, last_name FROM users WHERE user_id = %s', (user_id,))
    return cur.fetchone()
