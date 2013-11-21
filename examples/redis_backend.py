# -*- coding:utf-8 -*-

def create_redis_db(host='localhost', port=6379, db=0):
    import redis
    return redis.Redis(host=host, port=port, db=db)
