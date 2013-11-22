# -*- coding:utf-8 -*-

import os
import sys
import unittest

sys.path.append(os.curdir)

def suite():
    alltests = unittest.TestSuite()
    alltests.addTest(unittest.findTestCases(__import__('test_hello')))
    alltests.addTest(unittest.findTestCases(__import__('test_world')))
    return alltests


if __name__ == "__main__":
    from utknows import setup_utknows
    #from redis_backend import open_db, close_db
    from shelve_backend import open_db, close_db
    db = open_db()
    setup_utknows(db, root_dir=os.path.abspath(os.curdir))
    unittest.main(defaultTest="suite", buffer=True, exit=False)
    close_db(db)
