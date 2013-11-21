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
    # utkonws
    from utknows import setup_utknows
    from redis_backend import create_redis_db
    setup_utknows(create_redis_db(), root_dir=os.curdir)
    unittest.main(defaultTest="suite", buffer=True)
