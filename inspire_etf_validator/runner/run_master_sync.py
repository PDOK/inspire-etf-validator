import logging
import pkg_resources

from inspire_etf_validator.constants import (
    LOG_LINE_SEPARATOR,
    INSPIRE_ETF_ENDPOINT,
    INSPIRE_ETF_API_VERSION,
    SC_NS_AS_IS,
    SC_NS_HARMONIZED,
)
from inspire_etf_validator.domain.etf_validator import EtfValidatorClient
from inspire_etf_validator.domain.file_system import (
    write_test_master_file,
    get_master_result_path,
)
from inspire_etf_validator.runner.run_detail import (
    run_service_detail,
    run_metadata_detail,
)

from inspire_etf_validator.util.time_util import time_now, to_datetime, to_duration

logger = logging.getLogger(__name__)


def run_master(result_path, ngr_entries, inspire_etf_endpoint):
    start_time = time_now()

    result_master = {
        "inspire_etf_endpoint": INSPIRE_ETF_ENDPOINT,
        "inspire_etf_api_version": INSPIRE_ETF_API_VERSION,
        "inspire_etf_py_version": pkg_resources.require("inspire-etf-validator")[
            0
        ].version,
        "inspire_etf_eu_version": None,
        "start_time": to_datetime(start_time),
        "start_timestamp": start_time,
        "end_time": None,
        "end_timestamp": None,
        "duration": None,
        "result": None,
    }

    write_test_master_file(result_path, "inspire_endpoints", start_time, ngr_entries)

    number_of_endpoints = len(ngr_entries)

    logger.info(LOG_LINE_SEPARATOR)
    logger.info(LOG_LINE_SEPARATOR)
    logger.info("Started testrun sync")
    logger.info("Start time: %s", to_datetime(start_time))
    logger.info("Number of endpoints: %s", number_of_endpoints)
    logger.info(LOG_LINE_SEPARATOR)
    logger.info(LOG_LINE_SEPARATOR)

    result_detail_list = []
    test_result_detail = None

    for index, ngr_entry in enumerate(ngr_entries):
        logger.info(f"Running tests for item {index+1} of {number_of_endpoints}")
        ## service validation
        logger.info(f"Running service validation for item {index+1} of {number_of_endpoints}")
        if ngr_entry["serviceCategory"] in [SC_NS_AS_IS, SC_NS_HARMONIZED]:
            result_detail, test_result_detail = run_service_detail(
                result_path, ngr_entry, start_time, inspire_etf_endpoint
            )
            result_detail["service_metadata_uuid"] = ngr_entry["service_metadata_uuid"]
            result_detail_list.append(result_detail)
        else:
            logger.info(f"Skipping service validation for item {index + 1} of {number_of_endpoints}")
        ## metadata validation
        result_detail, test_result_detail = run_metadata_detail(
            result_path, ngr_entry, start_time, inspire_etf_endpoint
        )
        result_detail["service_metadata_uuid"] = ngr_entry["service_metadata_uuid"]
        result_detail_list.append(result_detail)

    end_time = time_now()

    result_master["end_time"] = to_datetime(end_time)
    result_master["end_timestamp"] = end_time
    result_master["duration"] = to_duration(start_time, end_time)
    result_master["result"] = result_detail_list
    result_master[
        "inspire_etf_eu_version"
    ] = EtfValidatorClient.get_inspire_etf_eu_version(test_result_detail)

    write_test_master_file(result_path, "run_master_result", start_time, result_master)

    logger.info(LOG_LINE_SEPARATOR)
    logger.info(LOG_LINE_SEPARATOR)
    logger.info("Stop testrun sync")
    logger.info("End time: %s", to_datetime(end_time))
    logger.info("Duration: %s", to_duration(start_time, end_time))

    return result_master, get_master_result_path(result_path, start_time)
