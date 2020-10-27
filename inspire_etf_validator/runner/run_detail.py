from inspire_etf_validator.domain.dao_etf_validator import start_test, get_testrun_id, get_log
from inspire_etf_validator.runner.waiter import wait_until_finished


def run_detail(endpoint_info):
    type = endpoint_info["pdokServiceType"].lower()
    endpoint = endpoint_info["serviceAccessPoint"]
    label = endpoint_info["label"]

    result = start_test(label, type, endpoint)
    id = get_testrun_id(result)

    print("testid")
    print(id)

    wait_until_finished(id)

    log = get_log(id)
    print(log)
