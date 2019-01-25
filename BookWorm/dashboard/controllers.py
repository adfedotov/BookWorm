from ..db import get_db

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
