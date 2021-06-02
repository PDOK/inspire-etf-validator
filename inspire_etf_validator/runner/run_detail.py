import sys
import logging

from inspire_etf_validator.constants import LOG_LINE_SEPARATOR
from inspire_etf_validator.domain.etf_validator import EtfValidatorClient
from inspire_etf_validator.domain.file_system import write_test_detail_file
from inspire_etf_validator.runner.waiter import wait_until_finished
from inspire_etf_validator.util.time_util import to_datetime, to_duration, time_now

logger = logging.getLogger(__name__)


def run_service_detail(
    result_path, endpoint_info, start_time_master, inspire_etf_endpoint, max_retry
):
    test_type = endpoint_info["pdokServiceType"].lower()
    test_endpoint = endpoint_info["serviceAccessPoint"]
    return __run_detail(
        result_path,
        endpoint_info,
        start_time_master,
        inspire_etf_endpoint,
        EtfValidatorClient.start_service_test,
        test_endpoint,
        test_type,
        max_retry
    )


def run_metadata_detail(
    result_path, endpoint_info, start_time_master, inspire_etf_endpoint, max_retry
):
    test_endpoint = endpoint_info["getRecordByIdUrl"].strip()
    test_type = endpoint_info["serviceCategory"]
    return __run_detail(
        result_path,
        endpoint_info,
        start_time_master,
        inspire_etf_endpoint,
        EtfValidatorClient.start_service_md_test,
        test_endpoint,
        test_type,
        max_retry
    )


def __run_detail(
    result_path,
    endpoint_info,
    start_time_master,
    inspire_etf_endpoint,
    testfunction,
    test_endpoint,
    test_type,
    max_retry
):

    result = {
        "start_time": None,
        "end_time": None,
        "error": None,
    }

    client = EtfValidatorClient(inspire_etf_endpoint, testfunction, max_retry)

    start_time = time_now()
    service_type = endpoint_info["pdokServiceType"].lower()
    label = endpoint_info["label"]
    file_name = (test_type if test_type is not None else "notype") + "_" + "".join(e for e in endpoint_info["label"] if e.isalnum())[:60]
    test_id = None
    test_result = None

    logger.info("Started test with label %s", label)
    logger.info(LOG_LINE_SEPARATOR)
    logger.info("Started test")
    logger.info("Start time: %s", to_datetime(start_time))
    logger.info("Test label: %s", label)
    logger.info("Test endpoint: %s", test_endpoint)
    logger.info(LOG_LINE_SEPARATOR)

    try:
        test_result = client.testfunction(client, label, test_type, test_endpoint)
        test_id = client.get_testrun_id(test_result)

        logger.info("Test id: %s", test_id)

        wait_until_finished(test_id, client)

        log = client.get_log(test_id)
        write_test_detail_file(
            result_path, start_time_master, test_id, "test_log", file_name, "log", log
        )

        test_result = client.get_result(test_id)
        write_test_detail_file(
            result_path,
            start_time_master,
            test_id,
            "test_result",
            file_name,
            "json",
            test_result,
        )

        test_html_report = client.get_html_report(test_id)
        write_test_detail_file(
            result_path,
            start_time_master,
            test_id,
            "test_report",
            file_name,
            "html",
            test_html_report,
        )

    # todo: Analyse results over time and filter out specific Exceptions
    except Exception:
        error = str(sys.exc_info())
        result["error"] = error
        logger.error(error)

    end_time = time_now()

    logger.info(LOG_LINE_SEPARATOR)
    logger.info("Stop test: %s", test_id)
    logger.info("End time: %s", to_datetime(end_time))
    logger.info("Duration: %s", to_duration(start_time, end_time))

    result["start_time"] = to_datetime(start_time)
    result["start_timestamp"] = start_time
    result["end_time"] = to_datetime(end_time)
    result["end_timestamp"] = end_time
    result["duration"] = to_duration(start_time, end_time)
    result["test_id"] = test_id
    result["test_result"] = (
        client.get_testrun_status(test_result)
        if test_result is not None
        else "TEST_RUN_FAIL"
    )
    result["validated_item"] = "service" if testfunction.__name__ == "start_service_test" else "metadata"
    result["test_endpoint"] = test_endpoint
    result["test_label"] = label
    result["service_name"] = endpoint_info["title"]
    result["test_service_type"] = service_type
    result["service_category"] = endpoint_info["serviceCategory"]
    return result, test_result
