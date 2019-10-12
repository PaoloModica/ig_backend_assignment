import re
from flask import Flask, make_response, jsonify
from flask_restful import Resource, Api, reqparse
from traceback import print_exc
from resources import get_updated_exchange_rates_document, get_exchange_rates_dict, get_currency_converted_amount
import traceback

from custom_api_exception.customexception import CustomAPIException

exchange_rates_document = 'assets/exchange_rates.xml'   # initializes the full path name of the exchange rates XML file
exchange_rates_dict = None  # initializes the variable which will contain the latest updated exchange rates

"""
Initializes Flask application and Flask-RESTful API.
"""
app = Flask(__name__)
api = Api(app)

"""
Initializes the request parser and all the arguments
amount: amount to convert
src_curr: original currency of the amount in input
dst_curr: destination currency of the amount to convert
date: date to take as reference to get the exchange rate
"""
parser = reqparse.RequestParser()
parser.add_argument('amount', type=float, required=True)
parser.add_argument('src-currency', type=str, required=True)
parser.add_argument('dest-currency', type=str, required=True)
parser.add_argument('reference-date', type=str, required=True)


# ToDo - To test
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


# ToDo - To test
class ConvertResource(Resource):
    """
    Defines the API Resource which handles currency converting requests.
    """
    def get(self):
        """
        Gets an amount to convert, the source currency, the destination currency and the date to use as reference for
        the exchange rate an return the converted amount, together with the requested destination currency.
        """
        global exchange_rates_dict
        try:
            to_return = None  # initializes the dict to return
            request_args = parser.parse_args()
            converted_amount = get_currency_converted_amount(exchange_rates_dict, request_args['amount'],
                                                             request_args['src-currency'], request_args['dest-currency'],
                                                             request_args['reference-date'])
            to_return = dict(amount=float(converted_amount), currency=request_args['dst-curr'])
            return to_return, 200
        except CustomAPIException as cae:
            return cae.to_dict(), cae.status_code


api.add_resource(IndexResource, '/', '/help')
api.add_resource(ConvertResource, '/api/convert')


def init_server():
    """
    This method initializes the application before server runs.
    """
    global exchange_rates_document, exchange_rates_dict
    try:
        get_updated_exchange_rates_document(exchange_rates_document)  # gets updated exchange rate XML file
        exchange_rates_dict = get_exchange_rates_dict(exchange_rates_document)  # gets the dict containing the latest updated exchange rates
    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == '__main__':
    init_server()
    app.run(debug=False)