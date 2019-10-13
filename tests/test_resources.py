import unittest
from unittest import TestCase
import os
import datetime
from custom_api_exception.customexception import CustomAPIException
import resources
from decimal import Decimal, ROUND_DOWN


class ResourcesTest(TestCase):
    """
    This class defines the tests for the resource function used by the application
    """

    def setUp(self):
        """
        Sets up function defining the set of instructions which are executed right before
        the execution of each test.
        """
        pass

    def tearDown(self):
        """
        Tear down function defining the set of instructions which are executed right after
        the execution of each test.
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

    # get_conversion_factor tests - start

    def test_get_conversion_factor_None_exchange_rates_dict(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a None value for the exchange rate dict.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = None
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_exchange_rates_dict_not_dict(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a not dict value for the exchange_rate_dict parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = [dict(EUR=Decimal(1.0))]
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_exchange_rates_dict_not_valid_dict(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a dict for the exchange_rates_dict parameter which contains both dict and
        non-dict values.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': [dict(EUR=Decimal(1.0), GBP=Decimal(0.89))]
        }
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_exchange_rates_dict_key_not_str(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a dict for the exchange_rates_dict parameter which contains both dict values.
        One of those dict as a key which is not a string.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': {'EUR': Decimal(1.0), 42: Decimal(0.89)}
        }
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_exchange_rates_dict_value_incorrect(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a dict for the exchange_rates_dict parameter which contains both dict values.
        One of those dict misses has an incorrect value for rate parameter (e.g. int instead of str).
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP='0.89')
        }
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_None_date(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a None value for the date parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = None
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_date_not_str(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a datetime value for the date parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = datetime.datetime.today()
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_date_not_well_formatted_str(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a str value for the date parameter.
        The date string is not formatted using 'YYYY-MM-DD' format.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '10-10-2019'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_None_src_currency(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function None value for the src_currency parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        src_currency = None
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_src_currency_not_Decimal(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a src_currency parameter whose value is not a string.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(currency='EUR', rate=Decimal(1.0)),
            '2019-10-10': dict(currency='GBP', rate=Decimal(0.89))
        }
        src_currency = 42
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_None_dest_currency(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function None value for the dest_currency parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(currency='EUR', rate=Decimal(1.0)),
            '2019-10-10': dict(currency='GBP', rate=Decimal(0.89))
        }
        src_currency = 'EUR'
        dest_currency = None
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_dest_currency_not_string(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function a dest_currency parameter whose value is not a string.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(currency='EUR', rate=Decimal(1.0)),
            '2019-10-10': dict(currency='GBP', rate=Decimal(0.89))
        }
        src_currency = 'EUR'
        dest_currency = 43
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_no_exchange_rate_for_selected_date(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function correct values for all the parameters.
        No exchange rate dict is available for the selected date.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-14'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_no_rate_found_for_selected_src_currency(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function correct values for all the parameters.
        No exchange rate is found for the selected source currency.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        src_currency = 'USD'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_no_rate_found_for_selected_dest_currency(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function correct values for all the parameters.
        No exchange rate is found for the selected destination currency.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        src_currency = 'EUR'
        dest_currency = 'USD'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_conversion_factor, exchange_rate_dict,
                          src_currency, dest_currency, date)

    def test_get_conversion_factor_complete_correct(self):
        """
        Tests 'get_conversion_factor' function of the Resource library.
        The test passes to the function correct values for all the parameters.
        The dict contains valid exchange rates for the selected date and for the selected source and destination
        currencies.
        :except:
            - the function should return the requested conversion factor.
            - The conversion factor should be a Decimal number.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        conversion_factor = resources.get_conversion_factor(exchange_rate_dict, src_currency, dest_currency, date)
        self.assertIsNotNone(conversion_factor)
        self.assertIsInstance(conversion_factor, Decimal)
        self.assertGreater(conversion_factor, 0)

    # get_conversion_factor tests - end

    # get_currency_converted_amount tests - start

    def test_get_currency_converted_amount_None_exchange_rates_dict(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a None value for the exchange rate dict.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = None
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_exchange_rates_dict_not_dict(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a not dict value for the exchange_rate_dict parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = [dict(EUR=Decimal(1.0))]
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_exchange_rates_dict_not_valid_dict(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a dict for the exchange_rates_dict parameter which contains both dict and
        non-dict values.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': [dict(EUR=Decimal(1.0), GBP=Decimal(0.89))]
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_exchange_rates_dict_key_not_str(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a dict for the exchange_rates_dict parameter which contains both dict values.
        One of those dict as a key which is not a string.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': {'EUR': Decimal(1.0), 42: Decimal(0.89)}
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_exchange_rates_dict_value_incorrect(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a dict for the exchange_rates_dict parameter which contains both dict values.
        One of those dict misses has an incorrect value for rate parameter (e.g. int instead of str).
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP='0.89')
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_None_amount(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a None value for the amount parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = None
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = None
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_amount_not_decimal(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a value for the amount parameter which is not a Decimal number.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = 0.50
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = None
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_None_date(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a None value for the date parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = None
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_date_not_str(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a datetime value for the date parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = datetime.datetime.today()
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_date_not_well_formatted_str(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a str value for the date parameter.
        The date string is not formatted using 'YYYY-MM-DD' format.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '10-10-2019'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_None_src_currency(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function None value for the src_currency parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = None
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_src_currency_not_Decimal(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a src_currency parameter whose value is not a string.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(currency='EUR', rate=Decimal(1.0)),
            '2019-10-10': dict(currency='GBP', rate=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 42
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_None_dest_currency(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function None value for the dest_currency parameter.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(currency='EUR', rate=Decimal(1.0)),
            '2019-10-10': dict(currency='GBP', rate=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = None
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_dest_currency_not_string(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function a dest_currency parameter whose value is not a string.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(currency='EUR', rate=Decimal(1.0)),
            '2019-10-10': dict(currency='GBP', rate=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 43
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_no_exchange_rate_for_selected_date(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function correct values for all the parameters.
        No exchange rate dict is available for the selected date.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-14'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_no_rate_found_for_selected_src_currency(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function correct values for all the parameters.
        No exchange rate is found for the selected source currency.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'USD'
        dest_currency = 'GBP'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_no_rate_found_for_selected_dest_currency(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function correct values for all the parameters.
        No exchange rate is found for the selected destination currency.
        :except: the function should raise a CustomAPIException.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'USD'
        date = '2019-10-10'
        self.assertRaises(CustomAPIException, resources.get_currency_converted_amount, exchange_rate_dict, amount,
                          src_currency, dest_currency, date)

    def test_get_currency_converted_amount_complete_correct(self):
        """
        Tests 'get_currency_converted_amount' function of the Resource library.
        The test passes to the function correct values for all the parameters.
        The dict contains valid exchange rates for the selected date and for the selected source and destination
        currencies.
        :except:
            - the function should return the requested converted amount.
            - The converted amount should be a Decimal number.
        """
        exchange_rate_dict = {
            '2019-10-09': dict(EUR=Decimal(1.0), GBP=Decimal(0.89)),
            '2019-10-10': dict(EUR=Decimal(1.0), GBP=Decimal(0.89))
        }
        amount = Decimal(10.0)
        src_currency = 'EUR'
        dest_currency = 'GBP'
        date = '2019-10-10'
        converted_amount = resources.get_currency_converted_amount(exchange_rate_dict, amount, src_currency,
                                                                   dest_currency, date)
        self.assertIsNotNone(converted_amount)
        self.assertIsInstance(converted_amount, Decimal)
        self.assertEqual(converted_amount, Decimal(8.9).quantize(Decimal('.01'), rounding=ROUND_DOWN))

    # get_currency_converted_amount tests - end


if __name__ == '__main__':
    unittest.main()
