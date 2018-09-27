==============
ORM Benchmarks
==============

**Qualification criteria is:**

* Needs to support minimum 2 databases, e.g. sqlite + something-else
* Runs on Python3.6
* Actively developed
* Has ability to generate initial DDL off specified models
* Handle one-to-many relationships


Benchmarks:
===========

These benchmarks are not meant to be used as a direct comparison.
They suffer from co-operative back-off, and is a lot simpler than common real-world scenarios.

1) Single table
---------------

.. code::

    model Journal:
        timestamp: datetime → now()
        level: int(enum) → 10/20/30/40/50
        text: varchar(255) → A selection of text

A. Insert rows (naïve implementation)
B. Insert rows (transactioned)
C. Inster rows (batch)
D. Filter on level
E. Search in text
F. Aggregation
G. Cursor efficiency


2) Relational
-------------
TODO



ORMs:
=====

Django:
        https://www.djangoproject.com/

peewee:
        https://github.com/coleifer/peewee

Pony ORM:
        https://github.com/ponyorm/pony

        * Does not support bulk insert.

SQLAlchemy ORM:
        http://www.sqlalchemy.org/

SQLObject:
        https://github.com/sqlobject/sqlobject

        * Does not support 16-bit integer for ``level``, used 32-bit instead.
        * Does not support bulk insert.

Tortoise ORM:
        https://github.com/tortoise/tortoise-orm

        * Currently the only ``async`` ORM as part of this suite.
        * Does not support bulk insert.

Results (SQLite)
================

==================== ============== ============== ============== ============== ============== ==============
\                    Django         peewee         Pony ORM       SQLAlchemy ORM SQLObject      Tortoise ORM
==================== ============== ============== ============== ============== ============== ==============
Insert                      1103.21        1162.59        1824.69        1027.65        1388.52        1357.67
Insert: atomic              7528.52        6251.02       22635.28       11298.14        4836.22        3612.45
Insert: bulk               24251.32       15010.20              —       42748.38              —              —
Filter: match              58217.95       37746.84      232541.34       93751.77       23456.15      143977.91
Filter: contains           58496.86       37138.48      237618.71       88206.71       21451.85      138549.93
==================== ============== ============== ============== ============== ============== ==============


Performance of Tortoise
=======================

Perf issues identified
----------------------
* No bulk insert operations
* Transactioned inserts ``pypika`` CPU utilisation. Whilst improved still the slowest.
* ``tortoise.models.__init__`` → investigate something more efficient than if-elif-elif-elif

On ``pypika`` cpu utilisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Now that ``pypika`` has implemented a perf fix for deepcopy, we still want to see if we can avoid using it.

Adding a very naïve SQL cache results in::

  Tortoise ORM, A: Rows/sec:    1696.85
  Tortoise ORM, B: Rows/sec:    5703.24

Which is a significant speedup. Also there is a lot on unnesseccary work being done, in ``_prepare_insert_values()`` and ``_prepare_insert_columns()`` that can be cached as well, etc..
This will require letting SQL driver do the escaping for us (which would be preferred, as it would allow their own optimisations to happen). This would require a large restructure.
We would have to do a very similar change to allow bulk inserts to work.

On ``tortoise.models.__init__``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The ``__init__`` still has a very long elif chain, using a lookup could give us a significant speedup:
By doing a quick & dirty change to it I suspect we still have ~20% of a speedup to gain in ``test_d`` & ``test_e``::

  Tortoise ORM, D: Rows/sec:  170751.78
  Tortoise ORM, E: Rows/sec:  167254.27


Perf fixes applied
------------------

1) **``aiosqlite`` polling misalignment** *(sqlite specific)*

   (20-40% speedup for retrieval, **10-15X** speedup for insertion): https://github.com/jreese/aiosqlite/pull/12
2) **``pypika`` improved copy implementation** *(generic)*

   (53% speedup for insertion): https://github.com/kayak/pypika/issues/160
3) **``tortoise.models.__init__`` restructure** *(generic)*

   (25-30% speedup for retrieval) https://github.com/tortoise/tortoise-orm/pull/51
