import unittest
import test.all_tests

import sys

# Be mindful of the pathing of the test suite.
sys.path.append('./code/machine_learning_model')

if __name__ == "__main__":
    testSuite = test.all_tests.create_test_suite()
    text_runner = unittest.TextTestRunner().run(testSuite)

