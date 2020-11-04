import time

from inspire_etf_validator.constants import SLEEP_TIME_IN_SECONDS
from inspire_etf_validator.util.time_util import time_now


def wait_until_finished(id, client, max_waiting_time_in_seconds=300):
    start_time = time_now()
    is_waiting = True

    print("Check if test run is complete")
    print("waiting", end="")
    times = 0

    while is_waiting:

        print("\b" * 20, end="")

        waited_seconds = int(time_now() - start_time)
        print(f"waiting ({waited_seconds}) ", "." * times, end="", sep="")

        times = times + 1
        time.sleep(0.5)

        if times > 5:
            times = 0

        if waited_seconds % SLEEP_TIME_IN_SECONDS == 0:
            if client.is_status_complete(id):
                is_waiting = False

        if (time_now() - start_time) > max_waiting_time_in_seconds:
            is_waiting = False

    print("\nTest complete")
