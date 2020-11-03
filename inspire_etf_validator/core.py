import logging

from inspire_etf_validator.domain.dao_file_system import get_result_master_list
from inspire_etf_validator.report.aggregate import aggregate_master
from inspire_etf_validator.runner import run_master_sync
from inspire_etf_validator.domain.dao_ngr import get_all_ngr_records
from os.path import join

logger = logging.getLogger(__name__)


def main(result_path, enable_caching):

    all_ngr_records = get_all_ngr_records(enable_caching)
    result = run_master_sync.run_master(result_path, all_ngr_records[0:9])
    # result = run_master_sync.run_master(result_path, all_ngr_records)

    master_result_path = join(result_path, result["result_path"])

    # generate_report(master_result_path)


def generate_report(master_result_path):
    result_list = get_result_master_list(master_result_path)
    aggregate_list = aggregate_master(result_list)

    print(aggregate_list)
