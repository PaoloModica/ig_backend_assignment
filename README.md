### Online currency converter

#### Project Overview

**Language**

Python v3.6

**Framework**

Flask, Flask-RESTful, UnitTest for Testing.

**Description**

The application provides a Web API exposing a currency converting service.

##### Endpoints:

- `'/', '/help'`

Returns an HTML page explaining how the currency converter application works

- `'/api/convert'`

The endpoint accept the following querystring parameters:

- `amount`: the amount to convert (e.g. 12.35);
- `src-currency`: ISO currency code for the source currency to convert (e.g. EUR, USD, GBP);
- `dest-currency`: ISO currency code for the destination currency (e.g. EUR, USD, GBP);
- `reference-date`: reference_date for the exchange rate, in YYYY-MM-DD format.

Request example

http://0.0.0.0:8080/api/convert?amount=14.0&src-currency=EUR&dest-currency=USD&reference-date=2019-10-10

The endpoint returns a JSON inside the response, which contains the following attributes:
- `amount`: converted amount;
- `currency`: ISO currency code the amount refers to (e.g. EUR, GBP, USD).

Response example

{"amount": 15.44, "currency": "USD"}

#### Run the project

##### Run with Docker
- Pull `currency converter` application server image: 

    `docker pull pwm91/currency_converter`

- Run `currency converter` image: 
    - If you want to detach your console from the Docker service running the image:
    
       `docker run -d -p 8080:8080 pwm91/currency_converter:latest`
    
    - If you want to check server console while image is running:
    
       `docker run -p 8080:8080 pwm91/currency_converter:latest`
       
- Check the server out with cURL or your favourite browser:

    `curl http://0.0.0.0:8080/api/convert?amount=14.0&src-currency=EUR&dest-currency=USD&reference-date=2019-10-10`

#### Run the tests

- Pull `currency converter tester` image:
  `docker pull pwm91/currency_converter_tester`
- Run `currency converter tester` image:     
  `docker run -p 8080:8080 pwm91/currency_converter_tester:latest`