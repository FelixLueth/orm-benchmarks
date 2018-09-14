from pony.orm import *
from datetime import datetime

db = Database()

class Journal(db.Entity):
    timestamp = Required(datetime, default=datetime.now)
    level = Required(int, size=16)
    text = Required(str, max_len=255)

db.bind(provider='sqlite', filename='db.sqlite3', create_db=True)
db.generate_mapping(create_tables=True)

