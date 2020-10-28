import logging

from inspire_etf_validator.runner import run_master_sync
from inspire_etf_validator.domain.dao_ngr import get_all_ngr_records

logger = logging.getLogger(__name__)


def main(result_path, enable_caching):

    all_ngr_records = get_all_ngr_records(enable_caching)
    #run_master_sync.run_master(result_path, all_ngr_records[0:3])
    run_master_sync.run_master(result_path, all_ngr_records)
