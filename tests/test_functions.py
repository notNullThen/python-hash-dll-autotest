import sys
import pytest
import time

sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from ctypes import *
from dirs_path import DIRS_PATH


@pytest.mark.skip(reason="BUG: HashStop / HashTerminate - Freeze if the operation is not yet complete")
def test_HashDirectory(hash_manager):
    operation_id_value = hash_manager.hash_directory(DIRS_PATH.multiple_files_dir)
    assert operation_id_value > 0, "Operation ID should be greater than 0"


def test_HashReadNextLogLine(utils):
    result = utils.get_one_file_directory_hash(DIRS_PATH.multiple_files_dir)

    assert result is not None, "Log line should not be None"


def test_HashStatus(hash_manager):

    operation_id_value = hash_manager.hash_directory(DIRS_PATH.multiple_files_dir)
    assert operation_id_value > 0, "Operation ID should be greater than 0"

    status = hash_manager.get_running_status(operation_id_value)
    assert status is True, "Status should be True while operation is running"

    while hash_manager.get_running_status(operation_id_value):
        time.sleep(0.1)

    assert (
        hash_manager.get_running_status(operation_id_value) is False
    ), "Status should be False after operation is finished"


@pytest.mark.skip(reason="BUG: HashStop / HashTerminate - Freeze if the operation is not yet complete")
def test_HashStop(hash_manager):
    operation_id_value = hash_manager.hash_directory(DIRS_PATH.multiple_files_dir)
    assert operation_id_value > 0, "Operation ID should be greater than 0"

    status = hash_manager.get_running_status(operation_id_value)
    assert status is True, "Status should be False after stopping the operation"

    hash_manager.stop(operation_id_value)

    status = hash_manager.get_running_status(operation_id_value)
    assert status is False, "Status should be False after stopping the operation"


@pytest.mark.skip(reason="BUG: HashFree() does not clean memory up correctly")
def test_HashFree(hash_manager):
    operation_id_value = hash_manager.hash_directory(DIRS_PATH.multiple_files_dir)

    while hash_manager.get_running_status(operation_id_value):
        time.sleep(0.1)

    result = hash_manager.read_next_log_line_and_free()
    assert result is not None, "Log line pointer should not be None"

    hash_manager.free(result)

    assert result is None, f'Memory was not freed up correctly! line_ptr.value is: "{result}"'
