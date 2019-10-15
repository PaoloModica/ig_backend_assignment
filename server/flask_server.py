from flask import Flask, make_response
from flask_restful import Resource, Api, reqparse
from traceback import print_exc
from server.resources import get_updated_exchange_rates_document, get_exchange_rates_dict, get_currency_converted_amount
import traceback
from decimal import Decimal

from custom_api_exception.customexception import CustomAPIException

"""
Initializes Flask application and Flask-RESTful API.
"""
app = Flask(__name__)
api = Api(app)


class IndexResource(Resource):
    """
    Defines the base API Resource for the web application.
    """
    def get(self):
        """
        Returns the index of the web application.
        """
        to_return = 'Currency Converter Index'    # initializes the string to return
        response = None  # initializes the variable used for the response
        try:
            with open('assets/currency_converter_help.html', 'r') as f:
                to_return = f.read()    # sets the string to return in the response.
            f.close()   # closes the file
        except Exception as e:
            # prints the exception
            print_exc()
            print(e)
        response = make_response(to_return, 200)
        response.content_type = 'text/html'
        return response


class ConvertResource(Resource):
    """
    Defines the API Resource which handles currency converting requests.
    """
    def __init__(self):
        # gets the dict containing the latest updated exchange rates
        self.exchange_rates_dict = get_exchange_rates_dict()
        """
        Initializes the request parser and all the arguments
        amount: amount to convert
        src_curr: original currency of the amount in input
        dst_curr: destination currency of the amount to convert
        date: date to take as reference to get the exchange rate
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('amount', type=float, required=True)
        self.parser.add_argument('src-currency', type=str, required=True)
        self.parser.add_argument('dest-currency', type=str, required=True)
        self.parser.add_argument('reference-date', type=str, required=True)

    def get(self):
        """
        Gets an amount to convert, the source currency, the destination currency and the date to use as reference for
        the exchange rate an return the converted amount, together with the requested destination currency.
        """
        try:
            to_return = None  # initializes the dict to return
            request_args = self.parser.parse_args()
            converted_amount = get_currency_converted_amount(self.exchange_rates_dict, Decimal(request_args['amount']),
                                                             request_args['src-currency'], request_args['dest-currency'],
                                                             request_args['reference-date'])
            to_return = dict(amount=float(converted_amount), currency=request_args['dest-currency'])
            return to_return, 200
        except CustomAPIException as cae:
            return cae.to_dict(), cae.status_code


api.add_resource(IndexResource, '/', '/help')
api.add_resource(ConvertResource, '/api/convert')


def init_server():
    """
    This method initializes the application before server runs.
    """
    try:
        get_updated_exchange_rates_document()  # gets updated exchange rate XML file
    except Exception as e:
        print(e)
        traceback.print_exc()

