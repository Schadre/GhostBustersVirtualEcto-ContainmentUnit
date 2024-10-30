import sqlalchemy as sa 
import sqlalchemy as so 
from app import app, db
from app.models import Ghosts, Ghostbusters

@app.shell_context_processor
def make_shell_context():
    return {'sa':sa, 'so':so, 'db':db, 'Ghosts':Ghosts, 'Ghostbusters':Ghostbusters}