import re
from flask import Flask, make_response, render_template
from flask_restful import Resource, Api, reqparse
from traceback import print_exc
from resources import get_updated_exchange_rates

date_re = re.compile('([12]\d{3}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))')
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
parser.add_argument('src-curr', type=str, required=True)
parser.add_argument('dst-curr', type=str, required=True)
parser.add_argument('date', type=str, required=True)


class IndexResource(Resource):
    """
    Defines the base API Resource for the web application.
    """
    def get(self):
        """
        Returns the index of the web application.
        """
        to_return = 'Currency Converter Index'    # initializes the string to return
        response = None # initializes the variable used for the response
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
    def get(self):
        """
        Gets an amount to convert, the source currency, the destination currency and the date to use as reference for
        the exchange rate an return the converted amount, together with the requested destination currency.
        """
        to_return = None  # initializes the dict to return
        request_args = parser.parse_args()
        # to_return = dict(amount=0.0, currency=dst_curr)
        return to_return


api.add_resource(IndexResource, '/', '/help')
api.add_resource(ConvertResource, '/api/convert')

if __name__ == '__main__':
    get_updated_exchange_rates()    # gets updated exchange rate XML file
    app.run(debug=False)