import sys
import logging

from inspire_etf_validator.constants import LOG_LINE_SEPARATOR
from inspire_etf_validator.domain.etf_validator import EtfValidatorClient
from inspire_etf_validator.domain.file_system import write_test_detail_file
from inspire_etf_validator.runner.waiter import wait_until_finished
from inspire_etf_validator.util.time_util import to_datetime, to_duration, time_now

logger = logging.getLogger(__name__)


def run_detail(result_path, endpoint_info, start_time_master, inspire_etf_endpoint):

    result = {
        "start_time": None,
        "end_time": None,
        "error": None,
    }

    client = EtfValidatorClient(inspire_etf_endpoint)

    start_time = time_now()
    service_type = endpoint_info["pdokServiceType"].lower()
    endpoint = endpoint_info["serviceAccessPoint"]
    label = endpoint_info["label"]
    file_name = "".join(e for e in endpoint_info["label"] if e.isalnum())
    test_id = None
    test_result = None

    logger.info("Started test with label %s", label)
    logger.info(LOG_LINE_SEPARATOR)
    logger.info("Started test")
    logger.info("Start time: %s", to_datetime(start_time))
    logger.info("Test label: %s", label)
    logger.info("Test endpoint: %s", endpoint)
    logger.info(LOG_LINE_SEPARATOR)

    try:
        test_result = client.start_test(label, service_type, endpoint)
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
    result["test_endpoint"] = endpoint
    result["test_label"] = label
    result["test_service_type"] = service_type
    return result, test_result
