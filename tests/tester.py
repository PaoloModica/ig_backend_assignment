import unittest
from test_server import ServerTest
from test_resources import ResourcesTest

if __name__ == '__main__':
    # initializes the Test Suite Runner, setting it up to return verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    # initializes the Test Suite regarding the resource functions used by the main server application
    suite_resources = unittest.TestLoader().loadTestsFromTestCase(ResourcesTest)
    runner.run(suite_resources)  # runs the Test Suite related to resource functions
    # initializes the Test Suite related to the main server application
    suite_server = unittest.TestLoader().loadTestsFromTestCase(ServerTest)
    runner.run(suite_server)    # runs the Test Suite relates to the main server application
