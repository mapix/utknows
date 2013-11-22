# -*- coding:utf-8 -*-

import os
import shelve

def open_db():
    return shelve.open(os.path.join(os.curdir, '.utknows'), writeback=True)

def close_db(db):
    db.sync()
    db.close()
