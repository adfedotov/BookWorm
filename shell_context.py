from bookworm import db, create_app
from bookworm.auth.models import User
from bookworm.dashboard.models import Note

app = create_app('config.DevelopmentConfig')


@app.shell_context_processor
def create():
    """
    Allows access to variables when running in shell context
    """
    return dict(app=app, db=db, User=User, Note=Note)
