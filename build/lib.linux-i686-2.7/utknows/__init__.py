# -*- coding:utf-8 -*-

import os
import sys
import trace
import cPickle

__version__ = "0.1.1"
_MTIME_TMP_CACHE = {}


def _get_file_mtime(filename):
    if not os.path.exists(filename):
        return None

    if filename in _MTIME_TMP_CACHE:
        return _MTIME_TMP_CACHE[filename]

    mtime = os.stat(filename).st_mtime
    _MTIME_TMP_CACHE[filename] = mtime
    return mtime


def _call_func(self, db, root_dir, db_prefix, *args, **kwargs):
    skip = True
    dbkey = db_prefix + self.id()
    test_result = args[0]
    dep_info = db.get(dbkey) or None

    if dep_info is None:
        skip = False
    else:
        for filename, mtime in cPickle.loads(dep_info).iteritems():
            if mtime != _get_file_mtime(filename):
                skip = False
                break

    if skip:
        test_result.addSkip(self, "utknows")
        return

    failures_count, errors_count = len(test_result.failures), len(test_result.errors)
    tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], trace=0, count=1)
    tracer.runctx('self.run(*args, **kwargs)', globals=globals(), locals=locals())
    if failures_count == len(test_result.failures) and errors_count == len(test_result.errors):
        deps = {filename:_get_file_mtime(filename) for filename, _ in tracer.results().counts.keys() if filename.startswith(root_dir)}
        db[dbkey] = cPickle.dumps(deps)


def setup_utknows(db, root_dir, db_prefix="utknows:"):
    unittest = __import__('unittest')
    if hasattr(unittest.TestCase, "__utknows_setup"):
        return

    def __new_call__(self, *args, **kwargs):
        _call_func(self, db, root_dir, db_prefix, *args, **kwargs)

    unittest.TestCase.__call__ = __new_call__
    unittest.TestCase.__utknows_setup = True
