import time

from inspire_etf_validator.constants import SLEEP_TIME_IN_SECONDS
from inspire_etf_validator.domain.dao_etf_validator import is_status_complete


def wait_until_finished(id, max_waiting_time_in_seconds=300):
    start_time = time.time()
    is_waiting = True

    while is_waiting:
        print("check if done")
        if is_status_complete(id):
            is_waiting = False

        time.sleep(SLEEP_TIME_IN_SECONDS)

        if (start_time - time.time()) > max_waiting_time_in_seconds:
            is_waiting = False
