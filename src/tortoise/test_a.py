import os
import time
from random import choice

from models import Journal

LEVEL_CHOICE = [10, 20, 30, 40, 50]
count = int(os.environ.get('ITERATIONS', '1000'))


async def runtest(loopstr):
    start = now = time.time()
    for i in range(count):
        await Journal.create(
            level=choice(LEVEL_CHOICE),
            text=f'Insert from A, item {i}'
        )
    now = time.time()

    print(f'Tortoise ORM{loopstr}, A: Rows/sec: {count / (now - start): 10.2f}')
