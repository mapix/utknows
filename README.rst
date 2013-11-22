=======
utknows
=======

**utknows** is a unittest patch that can automaticly ``skip`` test case
based on dependence info calculated by ``trace``.

Installing
==========

You can install **utknows** through ``pip`` or ``easy-install``::

    pip install utknows

Or you can download the `latest development version`_, which may
contain new features.

Using utknows
================

**utknows** should be used before ``unittest.main`` in invoked like this::

    from utknows import setup_utknows
    setup_utknows(db, db_prefix="utknows", root_dir=os.path.abspath(os.curdir))
    unittest.main(******, exit=False)
    # some resource release, etc db.close()

The ``db`` is a persistence database instance, and implementate ``__getitem__``  and ``__setitem__`` method.
The ``root_dir`` is the tracing base of dependence used by trace.
The ``db_prefix`` is the key prefix in ``db``.

When the first time tests runs, it calculate all the dependence info of every testcase::

    luoweifeng@luoweifeng-douban:~/workspace/utknows/examples$ python alltests.py
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.031s
    OK

After that, the case will be skipped when the dependence info is satisfacted::

     luoweifeng@luoweifeng-douban:~/workspace/utknows/examples$ python alltests.py
     ssssss
     ----------------------------------------------------------------------
     Ran 0 tests in 0.003s

     OK (skipped=6)

Case will be rerun when you modify any file it depends::

    luoweifeng@luoweifeng-douban:~/workspace/utknows/examples$ touch test_hello.py
    luoweifeng@luoweifeng-douban:~/workspace/utknows/examples$ python alltests.py 
    ...sss
    ----------------------------------------------------------------------
    Ran 3 tests in 0.003s

    OK (skipped=3)

The ``s`` output here stand for ``skip``.

Eamples
========

Using ``redis`` as backend::

    import redis

    def open_db():
        return redis.Redis(host='localhost', port=6379, db=0)

    def close_db(db):
        db.client_kill('localhost:6379')

    from utknows import setup_utknows
    db = open_db()
    setup_utknows(db, root_dir=os.path.abspath(os.curdir))
    unittest.main(defaultTest="suite", buffer=True, exit=False)
    close_db(db)


Using ``dbm`` as backend::

    import os
    import shelve

    def open_db():
        return shelve.open(os.path.join(os.curdir, '.utknows'), writeback=True)

    def close_db(db):
        db.sync()
        db.close()

    from utknows import setup_utknows
    db = open_db()
    setup_utknows(db, root_dir=os.path.abspath(os.curdir))
    unittest.main(defaultTest="suite", buffer=True, exit=False)
    close_db(db)


License
========

**utknows** is copyright 2013 mapix and Contributors, and is made
available under BSD-style license; see LICENSE for details.

.. _`latest development version`: https://github.com/mapix/utknows/tarball/master#egg=utknows
