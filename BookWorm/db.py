import psycopg2

from flask import current_app, g

def get_db():
    """
    Establish connection to database and store it in g unique for each connection
    """

    if 'db' not in g:
        g.db = psycopg2.connect("dbname=bookworm user=postgres password=pass")
    return g.db

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()
