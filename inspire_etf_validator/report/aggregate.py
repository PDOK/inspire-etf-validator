from inspire_etf_validator.domain.dao_etf_validator import get_testrun_status


def aggregate_master(result_list):

    aggregate_list = []
    status_summary = {}
    for result in result_list:
        test_id = get_testrun_status(result)
        test_status = get_testrun_status(result)

        if test_status not in status_summary:
            status_summary[test_status] = 0

        status_summary[test_status] = status_summary[test_status] + 1

        aggregate_list.append({
            "id": test_id,
            "status": test_status
        })

    aggregate_result = {
        "total": len(result_list),
        "status_summary": status_summary,
        "list": aggregate_list
    }

    return aggregate_result
