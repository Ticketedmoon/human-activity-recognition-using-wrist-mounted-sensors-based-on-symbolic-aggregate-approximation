import glob
import unittest
import sys

# Path is viewed from where run_tests.py is
sys.path.append('./code/')

from logger_module.Logger import Logger

def create_test_suite():
    test_file_strings = glob.glob('test/test_*.py')
    # test_file_strings = glob.glob('test/test_server_connect.py')
    module_strings = ['test.'+str[5:len(str)-3] for str in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) \
              for name in module_strings]
    testSuite = unittest.TestSuite(suites)
    return testSuite