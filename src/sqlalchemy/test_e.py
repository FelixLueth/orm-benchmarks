import os
import time
from random import randrange

from models import Journal, engine
from sqlalchemy.orm import sessionmaker

LEVEL_CHOICE = [10, 20, 30, 40, 50]
iters = int(os.environ.get('ITERATIONS', '1000')) // 2


Session = sessionmaker(bind=engine)

start = time.time()
session = Session()
count = 0

for _ in range(iters):
    for level in LEVEL_CHOICE:
        res = list(session.query(Journal).filter(Journal.level == level).limit(20).offset(randrange(int(iters/10))))
        count += len(res)

now = time.time()

print(f'SQLAlchemy ORM, E: Rows/sec: {count / (now - start): 10.2f}')
