import os
import sys
import json

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
