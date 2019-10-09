Online currency converter

The application provides a Web API exposing a currency converting service.

ENDPOINTS:

- '/', '/help'

Returns an HTML page explaining how the currency converter application works

- '/api/convert'

The endpoint accept the following querystring parameters:

- amount: the amount to convert (e.g. 12.35);
- src_currency: ISO currency code for the source currency to convert (e.g. EUR, USD, GBP);
- dst_currency:ISO currency code for the destination currency (e.g. EUR, USD, GBP);
- reference_date: reference_date for the exchange rate, in YYYY-MM-DD format.

The endpoint returns a JSON inside the response, which contains the following attributes:
- amount: converted amount;
- currency: ISO currency code the amount refers to (e.g. EUR, GBP, USD).


