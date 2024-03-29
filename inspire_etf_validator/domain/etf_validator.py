import json
import logging
import re
import time

import requests
from urllib.parse import urljoin

from inspire_etf_validator.constants import (
    INSPIRE_ETF_API_VERSION,
    SERVICE_TEST_IDS,
    METADATA_TEST_IDS,
    USER_AGENT,
    PDOK_EMAIL,
    SLEEP_TIME_IN_SECONDS,
)

logger = logging.getLogger(__name__)


class EtfValidatorClient:
    headers = {"User-Agent": USER_AGENT, "From": PDOK_EMAIL}

    def __init__(self, inspire_etf_endpoint, testfunction, max_retry):
        self.inspire_etf_endpoint = inspire_etf_endpoint
        self.testfunction = testfunction
        self.max_retry = max_retry

    def __endpoint(self, path):
        endpoint = self.inspire_etf_endpoint
        endpoint = urljoin(self.__fix_url(endpoint), INSPIRE_ETF_API_VERSION)
        endpoint = urljoin(self.__fix_url(endpoint), path)
        return endpoint

    @staticmethod
    def __fix_url(url):
        return url.rstrip("/") + "/"

    def start_service_test(self, label, test_type, service_endpoint):
        test_type_id = self.__get_test_id(test_type, SERVICE_TEST_IDS)
        body = {
            "label": label,
            "executableTestSuiteIds": [test_type_id],
            "arguments": {"testRunTags": label},
            "testObject": {"resources": {"serviceEndpoint": service_endpoint}},
        }
        return self.__start_test(body)

    def start_service_md_test(self, label, md_test_type, metadata_url):
        test_type_id = self.__get_test_id(md_test_type, METADATA_TEST_IDS)
        body = {
            "label": label,
            "executableTestSuiteIds": [test_type_id],
            "arguments": {"testRunTags": label},
            "testObject": {"resources": {"data": metadata_url}},
        }
        return self.__start_test(body)

    FILTER_RESOURCE_EXCEPTION = "The system has currently insufficient resources to process this request"
    sleep_time = SLEEP_TIME_IN_SECONDS
    retry_count = 0

    def __start_test(self, body):
        endpoint = self.__endpoint("TestRuns")

        response = requests.post(endpoint, json=body, headers=self.headers)

        if response.status_code != 201:

            if self.FILTER_RESOURCE_EXCEPTION in str(response.content):
                if self.retry_count > self.max_retry:
                    raise EtfValidatorClientException(
                        f"ETF validator does not have sufficient resources, tried {self.retry_count} times, we got HTTP status {response.status_code}:\n {response.content}"
                    )

                print(f"Test start failed, retry in {self.sleep_time} seconds")
                time.sleep(self.sleep_time)

                self.sleep_time = self.sleep_time * 2
                self.retry_count += 1

                return self.__start_test(body)
            else:
                raise EtfValidatorClientException(
                    f"Something went wrong starting the test, we got HTTP status {response.status_code}:\n {response.content}"
                )

        result = json.loads(response.content)

        return result

    @staticmethod
    def __get_test_id(test_type, test_ids_dictonary):

        if test_type not in test_ids_dictonary:
            raise EtfValidatorClientException(
                f"There is no test id for type `{test_type}`. Available test types are {', '.join(test_ids_dictonary.keys())}."
            )

        return test_ids_dictonary[test_type]

    def is_status_complete(self, test_id):
        endpoint = self.__endpoint(f"TestRuns/{test_id}/progress")
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code != 200:
            raise EtfValidatorClientException(
                f"Something went wrong checking the status of test `{test_id}`, we got HTTP status {response.status_code}:\n {response.content}"
            )

        result = json.loads(response.content)

        return result["val"] == result["max"]

    def get_result(self, test_id):
        endpoint = self.__endpoint(f"TestRuns/{test_id}")
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code != 200:
            raise EtfValidatorClientException(
                f"Something went wrong retrieving the result of test `{test_id}`, we got HTTP status {response.status_code}:\n {response.content}"
            )

        result = json.loads(response.content)

        return result

    def get_log(self, test_id):
        endpoint = self.__endpoint(f"TestRuns/{test_id}/log")
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code != 200:
            raise EtfValidatorClientException(
                f"Something went wrong retrieving the log of test `{test_id}`, we got HTTP status {response.status_code}:\n {response.content}"
            )

        return response.content

    def get_html_report(self, test_id):
        endpoint = self.__endpoint(f"TestRuns/{test_id}.html?download=false")
        response = requests.get(endpoint, headers=self.headers)

        if response.status_code != 200 and response.status_code != 202:
            raise EtfValidatorClientException(
                f"Something went wrong retrieving the html report of test `{test_id}`, we got HTTP status {response.status_code}:\n {response.content}"
            )

        return response.content

    @staticmethod
    def get_testrun_id(test_result):
        return test_result["EtfItemCollection"]["testRuns"]["TestRun"]["id"]

    @staticmethod
    def get_testrun_status(test_result):
        return test_result["EtfItemCollection"]["testRuns"]["TestRun"]["status"]

    @staticmethod
    def get_inspire_etf_eu_version(test_result):
        # Notice -> this way we get the inspire etf version mentioned on the EU github page dynamically (in a hacky way)
        # Source: https://github.com/inspire-eu-validation/community/releases

        version = "?"

        try:
            url = test_result["EtfItemCollection"]["referencedItems"][
                "translationTemplateBundles"
            ]["TranslationTemplateBundle"]["source"]
            reg = re.search(r"ets-repository-([1-9]\d{3}\.?\d*)", url)
            version = reg.group(1)
        except (KeyError, AttributeError, IndexError, TypeError):
            logger.error("Could not find Inspire ETF EU version")

        return version


class EtfValidatorClientException(Exception):
    pass
