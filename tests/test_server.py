import unittest
from unittest import TestCase
from main import app
from resources import get_updated_exchange_rates_document
from decimal import Decimal, ROUND_DOWN
import os


class ServerTest(TestCase):
    """
    This class defines the tests for the server application.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up function which defines the set of instructions executed once this TestCase class is initialized
        """
        get_updated_exchange_rates_document()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down function which defines the set of instructions executed once this TestCase class is destroyed.
        """
        try:
            os.remove('assets/exchange_rates.xml')
        except Exception as e:
            pass

    def setUp(self):
        """
        Set up function which defines the set of instructions executed right before the execution of each test
        """
        self.ta = app.test_client()   # runs application test client
        self.api_address = 'http://127.0.0.1'  # sets the address of the API server application

    def tearDown(self):
        """
        Tear down function which defines the set of instructions executed right after the execution of each test
        """
        pass

    def test_get_index(self):
        """
        Tests index endpoint of the server application.
        :except:
            - response status code should be 200
            - response content should be not empty
            - response content should be of text/HTML type
        """
        response = self.ta.get(self.api_address+ '/')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html')
        self.assertIsNotNone(response.data)

    def test_get_help(self):
        """
        Tests '/help' endpoint of the server application.
        :except:
            - response status code should be 200
            - response content should be not empty
            - response content should be of text/HTML type
        """
        response = self.ta.get(self.api_address + '/help')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html')
        self.assertIsNotNone(response.data)

    def test_convert_no_amount_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint without passing the amount querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'src-currency': 'EUR',
            'dest-currency': 'USD',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('amount' in data['message'])

    def test_convert_none_amount_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a None value for the amount querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': None,
            'src-currency': 'EUR',
            'dest-currency': 'USD',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('amount' in data['message'])

    def test_convert_no_num_amount_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a non numeric value for the amount parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 'Something',
            'src-currency': 'EUR',
            'dest-currency': 'USD',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('amount' in data['message'])

    def test_convert_no_src_currency_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint without the src-currency parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'dest-currency': 'USD',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('src-currency' in data['message'])

    def test_convert_none_src_currency_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a None value for the src-currency parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': None,
            'dest-currency': 'USD',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('src-currency' in data['message'])

    def test_convert_no_str_src_currency_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a value for the src-currency parameter which is not a string.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 18,
            'dest-currency': 'USD',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsNotNone(data['message'])

    def test_convert_no_dest_currency_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint without the dest-currency parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('dest-currency' in data['message'])

    def test_convert_none_dest_currency_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a None value for the dest-currency parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': None,
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('dest-currency' in data['message'])

    def test_convert_no_str_dest_currency_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a value for the dest-currency parameter which is not a string.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': '18',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsNotNone(data['message'])

    def test_convert_no_reference_date_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint without passing a value for the reference-date querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': 'USD'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('reference-date' in data['message'])

    def test_convert_none_reference_date_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a None value for the reference-date querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': 'USD',
            'reference-date': None
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsInstance(data['message'], dict)
        self.assertTrue('reference-date' in data['message'])

    def test_convert_no_str_reference_date_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a not string value for the reference-date querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': 'USD',
            'reference-date': '24.6'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsNotNone(data['message'])

    def test_convert_wrong_format_reference_date_parameter(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing a wrongly formatted string for the reference-date querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': 'USD',
            'reference-date': '10-10-2019'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsNotNone(data['message'])

    def test_convert_unknown_src_currency(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing an unknown ISO code for the src-currenct querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'AAA',
            'dest-currency': 'USD',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsNotNone(data['message'])

    def test_convert_unknown_dest_currency(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing an unknown ISO code for the dest-currenct querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': 'AAA',
            'reference-date': '2019-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsNotNone(data['message'])

    def test_convert_unknown_future_reference_date(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing future date as value for the reference-date querystring parameter.
        :except: the API should return 400.
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': 'USD',
            'reference-date': '2020-10-10'
        }
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertTrue('message' in data)
        self.assertIsNotNone(data['message'])

    def test_convert_valid_parameters(self):
        """
        Tests 'api/convert' API endpoint of the server application.
        The test calls the API endpoint passing valid values for the querystring parameter.
        :except:
            - the API should return 200,
            - the response should be a JSON containing both 'amount' and 'currency' attributes
            - the amount should be equal to the expectations
        """
        params = {
            'amount': 42,
            'src-currency': 'EUR',
            'dest-currency': 'USD',
            'reference-date': '2019-10-10'
        }
        expected_result = Decimal(42*1.103).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        response = self.ta.get(self.api_address + '/api/convert', query_string=params)
        data = response.json
        self.assertIsNotNone(response)
        self.assertIsNotNone(data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertTrue('currency' in data)
        self.assertIsInstance(data['currency'], str)
        self.assertEqual(data['currency'], 'USD')
        self.assertTrue('amount' in data)
        self.assertIsInstance(data['amount'], float)
        self.assertEqual(data['amount'], float(expected_result))


if __name__ == '__main__':
    unittest.main()