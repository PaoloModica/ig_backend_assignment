import requests
import traceback
from xml.dom import minidom
from decimal import Decimal, ROUND_DOWN
from custom_api_exception.customexception import CustomAPIException
from datetime import datetime


# ToDo - To test
def get_conversion_factor(exchange_rates_dict, src_currency, dst_currency, date):
    """
    Opens the updated XML document containing the updated exchange rates,
    gets the EUR/SRC_CURR and EUR/DST_CURR exchange rates and computes the
    factor to be used to convert an monetary amount from the source currency
    to the destination one.
    :param exchange_rates_dict: dict containing all available exchange rates
    :type exchange_rates_dict: dict
    :param src_currency: original currency of the amount to convert.
    :type src_currency: str
    :param dst_currency: destination currency of the amount to convert.
    :type dst_currency: str
    :param date: date of the exchange rate to consider (YYYY-MM-DD format)
    :type date: str
    :return: conversion_factor: factor to be used to convert the amount
    """
    conversion_factor = None    # initializes the variable used to store the conversion factor
    try:
        # parameters validation section

        if isinstance(exchange_rates_dict, dict) is False:
            raise CustomAPIException('Internal Error.', 500)
        if all(isinstance(er, dict) for er in exchange_rates_dict):
            raise CustomAPIException('Internal Error.', 500)

        if type(date) is not str:
            raise CustomAPIException('Date must be a string.', 400)
        if validate_date_string(date) is False:
            raise CustomAPIException('Invalid date ' + str(date), 400)

        if type(src_currency) is not str:
            raise CustomAPIException('Source currency must be a string.', 400)
        if type(dst_currency) is not str:
            raise CustomAPIException('Destination currency must be a string.', 400)

        # retrieves the dict containing the exchange rate at the selected date
        selected_exchange_rates = exchange_rates_dict.get(date, None)
        # if there is no exchange rate available for the selected date
        if selected_exchange_rates is None:
            raise CustomAPIException(f'No exchange rate found for the selected date {date}.', 400)
        # gets the source currency exchange rate
        src_exchange_rate = selected_exchange_rates.get(src_currency, None)
        if src_exchange_rate is None:
            raise CustomAPIException(f'No exchange rate found for the currency {src_currency}.', 400)
        # gets the destination currency exchange rate
        dst_exchange_rate = selected_exchange_rates.get(dst_currency, None)
        if dst_exchange_rate is None:
            raise CustomAPIException(f'No exchange rate found for the currency {dst_currency}.', 400)
        conversion_factor = Decimal(dst_exchange_rate / src_exchange_rate)  # gets the conversion factor
    except Exception as e:
        raise e  # propagates the Exception

    return conversion_factor


# ToDo - To Test
def get_currency_converted_amount(exchange_rates_dict, amount, src_currency, dst_currency, date):
    """
    Converts the amount given in input from a specific source currency to a destination currency.
    The currency conversion exploits the conversion rate updated at the date given in input.
    :param exchange_rates_dict: dict containing all available exchange rates
    :type exchange_rates_dict: dict
    :param amount: amount to convert
    :type amount: Decimal
    :param src_currency: original currency of the amount to convert
    :type src_currency: str
    :param dst_currency:
    :type dst_currency: str
    :param date:
    :type date: str
    :return: converted_amount
    """
    converted_amount = None  # initializes the variable used ot store the value to return
    try:
        # gets the factor to be used to convert the amount in input to the destination factor
        conversion_factor = get_conversion_factor(exchange_rates_dict, src_currency, dst_currency, date)
        if conversion_factor is not None:
            # calculates the converted amount
            converted_amount = Decimal(Decimal(amount)*conversion_factor).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        elif conversion_factor is None:
            raise Exception('An error occurred while trying to convert currency for the desired amount')
    except Exception as e:
        raise e
    return converted_amount


def get_exchange_rates_dict():
    """
    Retrieves the list of the available exchange rates from the updated exchange rates document.
    :return: exchange_rates_dict
    """
    # initializes the variable used to store the dict containing all the available exchange rates
    exchange_rates_dict = None
    # initializes the variable containing the full name of the exchange rate document
    exchange_rates_document = 'assets/exchange_rates.xml'

    try:
        # parses the XML file containing the updated exchange rates
        exchange_rate_doc = minidom.parse(exchange_rates_document)
        # initializes the variable used to store the dict containing all the available exchange rates
        exchange_rates_dict = dict()
        # initializes the variable used to store the dict containing all the available exchange rates
        cube_nodes = exchange_rate_doc.getElementsByTagName('Cube')
        # for each sub-element in the main node
        for c in cube_nodes:
            # if the sub-element contains the 'time' attribute
            if 'time' in c.attributes:
                # initializes the dict of currency exchange rates updated at the date
                # defined by the node 'time' attribute
                exchange_rates_dict[c.attributes['time'].value] = dict()
                # for each exchange rate in the current sub-element
                for er in c.childNodes:
                    # if the exchange rate node contains the 'currency' and 'rate' attributes
                    if ('currency' in er.attributes) and ('rate' in er.attributes):
                        # sets the exchange rate value for the current exchange rate node
                        exchange_rates_dict[c.attributes['time'].value][er.attributes['currency'].value] = \
                            Decimal(er.attributes['rate'].value)
                    else:
                        raise TypeError('The XML document is wrongly formatted.')
                # sets the exchange rates for Euro
                exchange_rates_dict[c.attributes['time'].value]['EUR'] = Decimal(1.0)
        if len(list(exchange_rates_dict.keys())) == 0:
            raise TypeError('The XML document is wrongly formatted.')
    except Exception as e:
        raise e  # raises exception
    return exchange_rates_dict


def get_updated_exchange_rates_document():
    """
    Sends an HTTP GET request to ECB Europe to get the updated
    exchange rate XML document, with EURO as reference.
    The XML document is then saved inside an XML file.
    """
    try:
        # sends an HTTP GET request to ECB Europe to get the updated exchange rate XML file
        response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml')
        # if the response is valid
        if (response.status_code == 200) and (response.content is not None):
            with open('assets/exchange_rates.xml', 'w') as f:
                f.write(str(response.content, 'utf-8'))
            f.close()
    except Exception as e:
        traceback.print_exc()
        print(e)


def validate_date_string(date):
    """
    Checks if the date string given in input is a valid date string.
    :param date: date string
    :type date: str
    :return: is_valid
    """
    is_valid = False    # initializes the boolean flag used to indicate whether the date string in input is valid or not
    try:
        date_object = datetime.strptime(date, '%Y-%m-%d')   # converts the date string to a date object
        if date_object is not None:  # if date object is not None
            is_valid = True  # sets the flag
    except Exception as e:
        pass
    return is_valid  # returns the flag

