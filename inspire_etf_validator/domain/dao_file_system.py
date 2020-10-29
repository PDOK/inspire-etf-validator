import glob
import os
import sys
import json
from os import listdir
from os.path import join, isdir

from inspire_etf_validator.util.time_util import to_filename_datetime


def write_test_file(result_path, run_on, test_id, test_file_description, label_file_name, extension, content):
    write_mode = "w"
    filename = f"{test_file_description}_{label_file_name}.{extension}"
    filepath = os.path.join(result_path, to_filename_datetime(run_on), test_id)
    filepath_name = os.path.join(filepath, filename)

    if type(content) is dict:
        content = json.dumps(content, indent=4)

    if type(content) is bytes:
        write_mode = "wb"

    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        f = open(filepath_name, write_mode)
        f.write(content)
    except:
        print("Error writing test output file:", sys.exc_info())
        raise
    else:
        f.close()


def get_result_master_list(path):
    test_detail_path_list = [f for f in listdir(path) if isdir(join(path, f))]

    test_result_list = []
    for test_detail_path in test_detail_path_list:
        search_path = join(path, test_detail_path)

        test_detail_file = glob.glob(f"{search_path}/test_result_*.json")

        if len(test_detail_file) > 0:
            test_detail = get_result_detail(test_detail_file[0])
            test_result_list.append(test_detail)
        else:
            test_result_list.append(
                {
                    "EtfItemCollection": {
                        "version": None,
                        "returnedItems": 0,
                        "ref": None,
                        "testRuns": {
                            "TestRun": {
                                "id": test_detail_path,
                                "status": "FAILED"
                            }
                        }
                    }
                }
            )

    return test_result_list


def get_result_detail(path):

    try:
        f = open(path, "r")
        test_detail_file_json = f.read()
        test_detail = json.loads(test_detail_file_json)
    except:
        print(f"Error reading test detail file at: {path}\n", sys.exc_info())
        raise
    else:
        f.close()

    return test_detail
