from inspire_etf_validator.runner.run_detail import run_detail


def run_master(endpoint_list):

    for endpoint_info in endpoint_list:
        run_detail(endpoint_info)
