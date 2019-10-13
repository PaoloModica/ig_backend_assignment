import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()  # initializes the test loader
    start_dir = 'tests'  # initializes the path where application tests are placed
    suite = loader.discover(start_dir)  # initializes unittest Test Suite

    runner = unittest.TextTestRunner()  # initializes unittest Test Suite runner
    runner.run(suite)   # runs test suite
