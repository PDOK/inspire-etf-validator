import logging
import os
import sys
import json
from os.path import join

from inspire_etf_validator.constants import DETAIL_OUTPUT_PATH, RUN_MASTER_RESULT_PATH
from inspire_etf_validator.util.time_util import to_filename_datetime

logger = logging.getLogger(__name__)


def write_test_detail_file(
    result_path,
    run_on,
    test_id,
    test_file_description,
    label_file_name,
    extension,
    content,
):
    write_mode = "w"
    separator = "_"
    label_file_name = separator + label_file_name if label_file_name else ""
    filename = f"{test_file_description}{label_file_name}.{extension}"
    filepath = join(
        get_master_result_path(result_path, run_on), DETAIL_OUTPUT_PATH, test_id
    )
    filepath_name = join(filepath, filename)

    if type(content) is dict:
        content = json.dumps(content, indent=4)

    if type(content) is bytes:
        write_mode = "wb"

    __ensure_directory_exists(filepath)
    write_file(filepath_name, content, write_mode)


def write_test_master_file(result_path, filename, run_on, content):
    write_mode = "w"
    filename = f"{filename}.json"
    filepath = get_master_result_path(result_path, run_on)
    filepath_name = join(filepath, filename)

    content = json.dumps(content, indent=4)

    __ensure_directory_exists(filepath)
    write_file(filepath_name, content, write_mode)


def __ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_file(filepath_name, content, write_mode="w"):
    try:
        f = open(filepath_name, write_mode)
        f.write(content)
    except:
        logger.info("Error writing test output file:", sys.exc_info())
        raise
    else:
        f.close()


def get_master_result_path(result_path, run_on):
    return join(result_path, to_filename_datetime(run_on))


def get_run_master_result(path):
    path = join(path, RUN_MASTER_RESULT_PATH)
    return __json_file_to_dict(path)


def get_result_detail(path):
    return __json_file_to_dict(path)


def __json_file_to_dict(path):

    try:
        f = open(path, "r")
        test_detail_file_json = f.read()
        result = json.loads(test_detail_file_json)
    except:
        logger.info(f"Error reading test result file at: {path}\n")
        raise
    else:
        f.close()

    return result
