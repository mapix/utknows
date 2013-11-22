# -*- coding:utf-8 -*-

import redis

def open_db():
    return redis.Redis(host='localhost', port=6379, db=0)

def close_db(db):
    db.client_kill('localhost:6379')
