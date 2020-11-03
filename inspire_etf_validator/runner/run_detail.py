import sys
import logging

from inspire_etf_validator.constants import LOG_LINE_SEPARATOR
from inspire_etf_validator.domain.dao_etf_validator import start_test, get_testrun_id, get_log, get_result, \
    get_html_report, get_testrun_status
from inspire_etf_validator.domain.dao_file_system import write_test_detail_file
from inspire_etf_validator.runner.waiter import wait_until_finished
from inspire_etf_validator.util.time_util import to_datetime, to_duration, time_now

logger = logging.getLogger(__name__)


def run_detail(result_path, endpoint_info, start_time_master):

    result = {
        "start_time": None,
        "end_time": None,
        "error": None,
    }

    start_time = time_now()
    service_type = endpoint_info["pdokServiceType"].lower()
    endpoint = endpoint_info["serviceAccessPoint"]
    label = endpoint_info["label"]
    file_name = ''.join(e for e in endpoint_info["label"] if e.isalnum())
    test_id = None
    test_result = None

    # logger.info("Started test with label %s", label)
    print(LOG_LINE_SEPARATOR)
    print("Started test")
    print("Start time:", to_datetime(start_time))
    print("Test label: ", label)
    print("Test endpoint: ", endpoint)
    print(LOG_LINE_SEPARATOR)

    try:
        test_result = start_test(label, service_type, endpoint)
        test_id = get_testrun_id(test_result)

        print("Test id: ", test_id)

        wait_until_finished(test_id)

        log = get_log(test_id)
        write_test_detail_file(result_path, start_time_master, test_id, "test_log", file_name, "log", log)

        test_result = get_result(test_id)
        write_test_detail_file(result_path, start_time_master, test_id, "test_result", file_name, "json", test_result)

        test_html_report = get_html_report(test_id)
        write_test_detail_file(result_path, start_time_master, test_id, "test_report", file_name, "html", test_html_report)

    except:
        error = str(sys.exc_info())
        result["error"] = error
        print(error)

    end_time = time_now()

    print(LOG_LINE_SEPARATOR)
    print("Stop test: ", test_id)
    print("End time: ", to_datetime(end_time))
    print("Duration: ", to_duration(start_time, end_time))

    result["start_time"] = to_datetime(start_time)
    result["start_timestamp"] = start_time
    result["end_time"] = to_datetime(end_time)
    result["end_timestamp"] = end_time
    result["duration"] = to_duration(start_time, end_time)
    result["test_id"] = test_id
    result["test_result"] = get_testrun_status(test_result) if test_result is not None else "TEST_RUN_FAIL"
    result["test_endpoint"] = endpoint
    result["test_label"] = label
    result["test_service_type"] = service_type
    return result, test_result
