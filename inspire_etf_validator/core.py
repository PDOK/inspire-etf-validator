import logging

from inspire_etf_validator.constants import LOG_LINE_SEPARATOR
from inspire_etf_validator.domain.file_system import get_run_master_result
from inspire_etf_validator.report.aggregate import aggregate_master, filter_status
from inspire_etf_validator.runner import run_master_sync
from inspire_etf_validator.domain.ngr import (
    get_all_ngr_records,
    get_filtered_ngr_entries, get_entry_by_endpoint,
)

logger = logging.getLogger(__name__)


def main(result_path, enable_caching, inspire_etf_endpoint, debug_mode, max_retry, single_endpoint):

    all_ngr_entries = get_all_ngr_records(result_path, enable_caching)

    ngr_entries = get_filtered_ngr_entries(all_ngr_entries, ["ATOM", "WFS", "WMS", "WMTS", "WCS"])

    if debug_mode:
        ngr_entries = ngr_entries[:3]

    if single_endpoint is not None:
        ngr_entries = get_entry_by_endpoint(all_ngr_entries, single_endpoint)
        if ngr_entries is None:
            logger.error(f"Endpoint {single_endpoint} not found in NGR records")

    result, master_result_path = run_master_sync.run_master(
        result_path, ngr_entries, inspire_etf_endpoint, max_retry
    )
    aggregate_list = aggregate_master(result)

    logger.info(aggregate_list)


def generate_report(master_result_path):
    master_result = get_run_master_result(master_result_path)
    aggregate_list = aggregate_master(master_result)

    logger.info(aggregate_list)

    test_run_with_exception = filter_status(master_result, "TEST_RUN_FAIL")

    for with_e7n in test_run_with_exception:
        logger.info("id", with_e7n["test_id"])
        logger.info("result", with_e7n["test_result"])
        logger.info("duration", with_e7n["duration"])
        logger.info("endpoint", with_e7n["test_endpoint"])
        logger.info("Error:")
        logger.info(LOG_LINE_SEPARATOR)
        logger.info(with_e7n["error"])
        logger.info(LOG_LINE_SEPARATOR)
        logger.info(LOG_LINE_SEPARATOR)
