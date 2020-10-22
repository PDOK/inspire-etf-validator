import requests
from urllib.parse import urljoin

from inspire_etf_validator.constants import INSPIRE_ETF_ENDPOINT, INSPIRE_ETF_API_VERSION, TEST_ID_LIST


def __endpoint(path):
    endpoint = INSPIRE_ETF_ENDPOINT
    endpoint = urljoin(__fix_url(endpoint), INSPIRE_ETF_API_VERSION)
    endpoint = urljoin(__fix_url(endpoint), path)
    return endpoint


def __fix_url(url):
    return url.rstrip('/') + '/'


def test():
    endpoint = __endpoint('status')

    x = requests.get(endpoint)

    print(x.text)


def start_test(label, type, service_endpoint):
    endpoint = __endpoint('TestRuns')

    type = __get_test_id(type)
    body = {
        "label": label,
        "executableTestSuiteIds": [type],
        "arguments": {
            "testRunTags": label
        },
        "testObject": {
            "resources": {
                "serviceEndpoint": service_endpoint
            }
        }
    }

    response = requests.post(endpoint, json=body)

    if response.status_code != 201:
        raise Exception(f"Something went wrong starting the test, we got {response.status_code} HTTP status:\n {response}")

    return response


def __get_test_id(type):

    if type not in TEST_ID_LIST:
        raise Exception(f"There is no test id for type `{type}`. Available test types are {', '.join(TEST_ID_LIST.keys())}.")

    return TEST_ID_LIST[type]

def check_status():
    endpoint = __endpoint('status')


def get_result():
    endpoint = __endpoint('status')
