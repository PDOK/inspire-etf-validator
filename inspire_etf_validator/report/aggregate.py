def aggregate_master(master):

    status_summary = {}
    status_summary_per_service = {}
    for detail in master["result"]:

        test_status = detail["test_result"]
        test_service_type = detail["test_service_type"]

        if test_status not in status_summary:
            status_summary[test_status] = 0

        if test_service_type not in status_summary_per_service:
            status_summary_per_service[test_service_type] = {}

        if test_status not in status_summary_per_service[test_service_type]:
            status_summary_per_service[test_service_type][test_status] = 0

        status_summary[test_status] += 1
        status_summary_per_service[test_service_type][test_status] += 1

    summary = {
        "status_summary": status_summary,
        "status_summary_per_service": status_summary_per_service,
    }

    return summary


def filter_status(master, status):

    filtered_list = []
    for detail in master["result"]:
        test_status = detail["test_result"]

        if test_status == status:
            filtered_list.append(detail)

    return filtered_list
