import requests
import traceback

def get_updated_exchange_rates():
    """
    Sends an HTTP GET request to ECB Europe to get the updated
    exchange rate XML document, with EURO as reference.
    The XML document is then saved inside an XML file.
    :return:
    """
    try:
        # sends an HTTP GET request to ECB Europe to get the updated exchange rate XML file
        response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml')
        # if the response is valid
        if (response.status_code == 200) and (response.content is not None):
            with open('assets/exchange_rates.xml', 'w') as f:
                f.write(str(response.content, 'utf-8'))
            f.close()
    except ConnectionError as ce:
        traceback.print_exc()
    except TimeoutError as te:
        traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        print(e)