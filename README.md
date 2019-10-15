## Online currency converter

### Project Overview

**Language**

Python v3.6

**Framework**

Flask, Flask-RESTful, UnitTest for Testing.

**Description**

The application provides a Web API exposing a currency converting service.

If the computer running the application has Internet connection, the server downloads from the Web the updated 
list of the available exchange rates.

If there is no Internet connection, the currency converter uses the list of exchange rates provided by a local
XML file.

#### Endpoints:

- `'/', '/help'`

Returns an HTML page explaining how the currency converter application works.

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

### Run the project

#### Run in your system
##### System Requirements
- `python v3.6`
- `pip`
- `virtualenv`
##### Procedure
- Clone or download this GitHub repository to a folder in your system;
- Open a Terminal
- change directory to the currency converter project folder;
- Set up a new Python virtual environment:
    
    `virtualenv venv`
    
- Activate the virtual environment created before:
    
    `source venv/bin/activate`
    
- Install application requirements in the virtual environment:
    
    `pip install --upgrade -r requirements.txt`

- Run the application:

    `python main.py`

- Check the server out with cURL or your favourite browser:

   `curl http://0.0.0.0:8080/api/convert?amount=14.0&src-currency=EUR&dest-currency=USD&reference-date=2019-10-10`    

#### Run with Docker
##### System Requirements
- `Docker`
##### Procedure
- Pull `currency converter` application server image: 

    `docker pull pwm91/currency_converter`

- Run `currency converter` image: 
    - If you want to detach your console from the Docker service running the image:
    
       `docker run -d -p 8080:8080 pwm91/currency_converter:latest`
    
    - If you want to check server console while image is running:
    
       `docker run -p 8080:8080 pwm91/currency_converter:latest`
       
- Check the server out with cURL or your favourite browser:

    `curl http://0.0.0.0:8080/api/convert?amount=14.0&src-currency=EUR&dest-currency=USD&reference-date=2019-10-10`

### Run tests

#### Run in your system
##### System Requirements
- `python v3.6`
- `pip`
- `virtualenv`
##### Procedure
- Clone or download this GitHub repository to a folder in your system;
- Open a Terminal
- change directory to the currency converter project folder;
- Set up a new Python virtual environment:
    
    `virtualenv venv`
    
- Activate the virtual environment created before:
    
    `source venv/bin/activate`
    
- Install application requirements in the virtual environment:
    
    `pip install --upgrade -r requirements.txt`

- Run the tester:
    
    `python tester.py`

#### Run with Docker
##### System Requirements
- `Docker`
##### Procedure
- Pull `currency converter tester` image:
  `docker pull pwm91/currency_converter_tester`
- Run `currency converter tester` image:     
  `docker run -p 8080:8080 pwm91/currency_converter_tester:latest`