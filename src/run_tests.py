import unittest
import test.all_tests
import nose
import sys
import os
import coverage

# Be mindful of the pathing of the test suite.
sys.path.append('./code/')

from logger_module.Logger import Logger

if __name__ == "__main__":
    # Pass in --nose for nose tests
    if len(sys.argv) > 1 and sys.argv[1] == "--nose":
        nose.run(argv=[os.path.abspath(__file__), "--verbosity=3", "--nocapture", "--cover-package=phased", "./"])
    # Else run normal python unit tests
    else:
        testSuite = test.all_tests.create_test_suite()
        text_runner = unittest.TextTestRunner().run(testSuite)