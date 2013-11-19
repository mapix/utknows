# -*- coding:utf-8 -*-

import os
import sys
import trace
import cPickle

_mtime_tmp_cache = {}
def get_file_mtime(fn):
    if fn in _mtime_tmp_cache:
        return _mtime_tmp_cache[fn]
    if not os.path.exists(fn):
        return None
    mtime = os.stat(fn).st_mtime
    _mtime_tmp_cache[fn] = mtime
    return mtime

def utknows_skip_func(test, read_db, write_db, prefix, base, *args, **kwds):
    skip = True
    dbkey = prefix + test.id()
    test_result = args[0]
    dep_info = read_db.get(dbkey) if read_db else None
    if dep_info is None:
        skip = False
    else:
        for fn, mtime in cPickle.loads(dep_info).iteritems():
            if mtime != get_file_mtime(fn):
                skip = False
                break
    if skip:
        test_result.addSkip(test, "utknows")
    else:
        failures_count, errors_count = len(test_result.failures), len(test_result.errors)
        tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], trace=0, count=1)
        tracer.runctx('test.run(*args, **kwds)', globals=globals(), locals=locals())
        if failures_count == len(test_result.failures) and errors_count == len(test_result.errors):
            r = {fn:get_file_mtime(fn) for fn, _ in tracer.results().counts.keys() if fn.startswith(base)}
            if write_db:
                write_db.set(dbkey, cPickle.dumps(r))

def patch_case(wt_func, read_db, write_db, prefix, base):
    import unittest
    if hasattr(unittest.TestCase, "__patched_case"):
        return
    def new_func(self, *args, **kwds):
        wt_func(self, read_db, write_db, prefix, base, *args, **kwds)
    unittest.TestCase.__call__ = new_func
    unittest.TestCase.__patched_case = 1

def create_redis_db(host='localhost', port=6379, db=0):
    import redis
    return redis.Redis(host=host, port=port, db=db)

if __name__ == '__main__':
    read_db = write_db = create_redis_db()
    patch_case(utknows_skip_func, read_db, write_db, prefix="utknows:", base=os.path.abspath(os.curdir))

