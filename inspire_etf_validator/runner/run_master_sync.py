from inspire_etf_validator.constants import LOG_LINE_SEPARATOR
from inspire_etf_validator.runner.run_detail import run_detail
from inspire_etf_validator.util.time_util import time_now, to_datetime, to_duration


def run_master(result_path, endpoint_list):
    start_time = time_now()

    result_master = {
        "start_time": to_datetime(start_time),
        "end_time": None,
        "duration": None,
        "result": None
    }

    print(LOG_LINE_SEPARATOR)
    print(LOG_LINE_SEPARATOR)
    print("Started testrun sync")
    print("Start time:", to_datetime(start_time))
    print("Number of endpoints:", len(endpoint_list))
    print(LOG_LINE_SEPARATOR)
    print(LOG_LINE_SEPARATOR)

    result_detail_list = []

    for endpoint_info in endpoint_list:
        result_detail = run_detail(result_path, endpoint_info, start_time)
        result_detail_list.append(result_detail)

    end_time = time_now()

    result_master["end_time"] = to_datetime(end_time)
    result_master["duration"] = to_duration(start_time, end_time)
    result_master["result"] = result_detail_list

    print(LOG_LINE_SEPARATOR)
    print(LOG_LINE_SEPARATOR)
    print("Stop testrun sync")
    print("End time: ", to_datetime(end_time))
    print("Duration: ", to_duration(start_time, end_time))

    return result_master
