import logging

from inspire_etf_validator.constants import LOG_LINE_SEPARATOR
from inspire_etf_validator.domain.dao_file_system import get_run_master_result
from inspire_etf_validator.report.aggregate import aggregate_master, filter_status
from inspire_etf_validator.runner import run_master_sync
from inspire_etf_validator.domain.dao_ngr import get_all_ngr_records

logger = logging.getLogger(__name__)


def main(result_path, enable_caching, inspire_etf_endpoint):

    all_ngr_records = get_all_ngr_records(enable_caching)
    result, master_result_path = run_master_sync.run_master(
        result_path, all_ngr_records[0:10], inspire_etf_endpoint
    )
    # result, master_result_path = run_master_sync.run_master(
    #     result_path, all_ngr_records, inspire_etf_endpoint
    # )
    aggregate_list = aggregate_master(result)

    print(aggregate_list)


def generate_report(master_result_path):
    master_result = get_run_master_result(master_result_path)
    aggregate_list = aggregate_master(master_result)

    print(aggregate_list)

    test_run_with_exception = filter_status(master_result, "TEST_RUN_FAIL")

    for with_e7n in test_run_with_exception:
        print("id", with_e7n["test_id"])
        print("result", with_e7n["test_result"])
        print("duration", with_e7n["duration"])
        print("endpoint", with_e7n["test_endpoint"])
        print("Error:")
        print(LOG_LINE_SEPARATOR)
        print(with_e7n["error"])
        print(LOG_LINE_SEPARATOR)
        print(LOG_LINE_SEPARATOR)
