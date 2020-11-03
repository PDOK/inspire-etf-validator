import json

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
        # todo: specefieke exception gebruiken
        raise Exception(f"Something went wrong starting the test, we got HTTP status {response.status_code}:\n {response.content}")

    result = json.loads(response.content)

    return result


def __get_test_id(type):

    if type not in TEST_ID_LIST:
        raise Exception(f"There is no test id for type `{type}`. Available test types are {', '.join(TEST_ID_LIST.keys())}.")

    return TEST_ID_LIST[type]


def is_status_complete(test_id):
    endpoint = __endpoint(f"TestRuns/{test_id}/progress")
    response = requests.get(endpoint)

    if response.status_code != 200:
        raise Exception(
            f"Something went wrong checking the status of test `{test_id}`, we got HTTP status {response.status_code}:\n {response.content}")

    result = json.loads(response.content)

    return result['val'] == result['max']


def get_result(test_id):
    endpoint = __endpoint(f"TestRuns/{test_id}")
    response = requests.get(endpoint)

    if response.status_code != 200:
        raise Exception(
            f"Something went wrong retrieving the result of test `{test_id}`, we got HTTP status {response.status_code}:\n {response.content}")

    result = json.loads(response.content)

    return result


def get_log(test_id):
    endpoint = __endpoint(f"TestRuns/{test_id}/log")
    response = requests.get(endpoint)

    if response.status_code != 200:
        raise Exception(
            f"Something went wrong retrieving the log of test `{test_id}`, we got HTTP status {response.status_code}:\n {response.content}")

    return response.content


def get_html_report(test_id):
    endpoint = __endpoint(f"TestRuns/{test_id}.html?download=false")
    response = requests.get(endpoint)

    if response.status_code != 200 and response.status_code != 202:
        raise Exception(
            f"Something went wrong retrieving the html report of test `{test_id}`, we got HTTP status {response.status_code}:\n {response.content}")

    return response.content


def get_testrun_id(test_result):
    return test_result["EtfItemCollection"]["testRuns"]["TestRun"]["id"]


def get_testrun_status(test_result):
    return test_result["EtfItemCollection"]["testRuns"]["TestRun"]["status"]
