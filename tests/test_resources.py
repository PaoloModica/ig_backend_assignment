from unittest import TestCase
import os
from custom_api_exception.customexception import CustomAPIException
import resources
from decimal import Decimal

class ResourcesTest(TestCase):
    """
    This class defines the tests for the resource function used by the application
    """

    def setUp(self):
        """
        Sets up the Test case.
        """
        pass

    # Validate_date_string tests - start
    def test_validate_date_string_None_string(self):
        """
        Tests 'validate_date_string' function of the Resource library.
        The test passes to the function a None string.
        :except: the function should return False
        """
        date_string = None
        outcome = resources.validate_date_string(date_string)
        self.assertIsNotNone(outcome)
        self.assertFalse(outcome)

    def test_validate_date_string_not_str(self):
        """
        Tests 'validate_date_string' function of the Resource library.
        The test passes to the function a value for the date parameter which is not a str (e.g. int).
        :except: the function should return False
        """
        date_string = 42
        outcome = resources.validate_date_string(date_string)
        self.assertIsNotNone(outcome)
        self.assertFalse(outcome)

    def test_validate_date_string_not_valid_str(self):
        """
        Tests 'validate_date_string' function of the Resource library.
        The test passes to the function as date parameter a string which is not well formatted (e.g. DD-MM-YYYY).
        :except: the function should return False
        """
        date_string = '09-10-2019'
        outcome = resources.validate_date_string(date_string)
        self.assertIsNotNone(outcome)
        self.assertFalse(outcome)

    def test_validate_date_string_valid_str(self):
        """
        Tests 'validate_date_string' function of the Resource library.
        The test passes to the function as date parameter a date string in YYYY-MM-DD format.
        :except: the function should return True
        """
        date_string = '2019-10-09'
        outcome = resources.validate_date_string(date_string)
        self.assertIsNotNone(outcome)
        self.assertTrue(outcome)

    # Validate_date_string tests - end

    # get_exchange_rates_dict tests - start

    def test_get_exchange_rates_dict_file_not_found(self):
        """
        Tests 'get_exchange_rates_dict' function of the Resource libraries.
        The tests tries to get the dict containing the updated exchange rates out of an unknown XML document.
        :except: the function should raise FileNotFound exception.
        """
        self.assertRaises(FileNotFoundError, resources.get_exchange_rates_dict)

    def test_get_exchange_rates_dict_wrongly_formatted_file(self):
        """
        Tests 'get_exchange_rates_dict' function of the Resource libraries.
        The tests tries to get the dict containing the updated exchange rates out of a wrongly formatted XML file.
        :except: the function should raise TypeError exception.
        """
        # First, create the wrongly formatted XML file
        xml_string = '<item>Here is an item</item>'
        with open('assets/exchange_rates.xml', 'w') as f:
            f.write(xml_string)
        f.close()
        # Then, call the function
        self.assertRaises(TypeError, resources.get_exchange_rates_dict)
        # removes the exchange rate document
        os.remove('assets/exchange_rates.xml')

    def test_get_exchange_rates_dict_correct_file(self):
        """
        Tests 'get_exchange_rates_dict' function of the Resource libraries.
        The tests tries to get the dict containing the updated exchange rates out of the XML file coming from ECB Europe.
        :except: the function should return a valid dict
        """
        # First, get the ECB correct XML file
        resources.get_updated_exchange_rates_document()

        # Then, call the function
        exchange_rates_dict = resources.get_exchange_rates_dict()

        self.assertIsNotNone(exchange_rates_dict)
        self.assertIsInstance(exchange_rates_dict, dict)
        self.assertTrue(all(isinstance(v, dict) is True for (k, v) in exchange_rates_dict.items()))
        self.assertTrue(all(all(isinstance(rv, Decimal) is True for rk, rv in v.items()) is True for (k, v)
                            in exchange_rates_dict.items()))

        # removes the exchange rate document
        os.remove('assets/exchange_rates.xml')

    # get_exchange_rates_dict tests - end
