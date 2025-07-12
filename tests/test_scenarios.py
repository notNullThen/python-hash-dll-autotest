import time
import pytest
from ctypes import *
from dirs_path import DIRS_PATH
from files_details import FILES_DETAILS
from utils import Utils


def test_init_then_terminate(hash_wrapper):
    terminate_result = hash_wrapper.HashTerminate()
    assert (
        terminate_result == 0
    ), f"HashTerminate failed with error code: {hash_wrapper.get_error_from_code(terminate_result)}"


@pytest.mark.skip(reason="BUG: HashStop / HashTerminate - Freeze if the operation is not yet complete")
def test_hash_dir_then_stop(hash_manager):
    operation_id_value = hash_manager.hash_directory(DIRS_PATH.multiple_files_dir)

    hash_manager.stop(operation_id_value)


def test_hash_dir_then_terminate(hash_wrapper):
    operation_id = c_size_t()
    hash_wrapper.HashDirectory(DIRS_PATH.multiple_files_dir.encode("utf-8"), byref(operation_id))

    time.sleep(0.5)
    terminate_result = hash_wrapper.HashTerminate()
    assert (
        terminate_result == 0
    ), f"HashTerminate failed with error code: {hash_wrapper.get_error_from_code(terminate_result)}"


@pytest.mark.skip(reason="TODO: Define how to ignore the 'std::filesystem::__cxx11::filesystem_error' error")
def test_hash_dir_with_invalid_path(hash_wrapper):
    operation_id = c_size_t()
    try:
        result = hash_wrapper.HashDirectory("invalid_path".encode("utf-8"), byref(operation_id))
    except Exception:
        result = -1  # fallback in case ctypes throws

    assert result != 0, f"HashDirectory should fail with error code, got {result}"
    assert operation_id.value == 0


@pytest.mark.skip(reason="BUG: Incorrect MD5 hash calculation")
def test_hash_one_file_dir(utils):
    actual_result = utils.get_one_file_directory_hash(DIRS_PATH.one_file_dir)
    expected_result = Utils.build_result(1, FILES_DETAILS.file1_path, FILES_DETAILS.file1_hash)
    assert (
        expected_result.lower() in actual_result.lower()
    ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result}\n{actual_result}"


@pytest.mark.skip(reason="BUG: Incorrect MD5 hash calculation")
def test_hash_multiple_files_and_one_file_dirs(utils, hash_manager):
    operation_id_value = hash_manager.hash_directory(DIRS_PATH.multiple_files_dir)

    while hash_manager.get_running_status(operation_id_value):
        time.sleep(0.1)

    hash_manager.read_next_log_line_and_free()
    hash_manager.read_next_log_line_and_free()
    actual_result = utils.get_one_file_directory_hash(DIRS_PATH.one_file_dir)
    expected_result = Utils.build_result(2, FILES_DETAILS.file1_path, FILES_DETAILS.file1_hash)

    assert (
        actual_result.lower() == expected_result.lower()
    ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result}\n{actual_result}"


@pytest.mark.skip(reason="Can run only separately because of memory bugs")
def test_hash_empty_dir(hash_manager, hash_wrapper):
    operation_id = c_size_t()
    hash_wrapper.HashDirectory(DIRS_PATH.empty_dir.encode("utf-8"), byref(operation_id))

    while hash_manager.get_running_status(operation_id.value):
        time.sleep(0.1)

    line_ptr = c_char_p()
    result = hash_wrapper.HashReadNextLogLine(line_ptr)

    assert result != 0, f"HashDirectory should fail with error code 1, got {result}"
    assert not hash_manager.get_running_status(operation_id.value), "Hash operation should not be running"


@pytest.mark.skip(
    reason="BUG: Log lines are mixed when hashing two folders in parallel | BUG: Memory can be mixed up when running several separate processes"
)
def test_two_parallel_hashes(hash_manager):
    operation_id1 = hash_manager.hash_directory(DIRS_PATH.one_file_dir)
    operation_id2 = hash_manager.hash_directory(DIRS_PATH.one_file_dir)

    assert hash_manager.get_running_status(operation_id1)
    assert hash_manager.get_running_status(operation_id2)

    assert operation_id1 > 0
    assert operation_id2 == operation_id1 + 1

    while hash_manager.get_running_status(operation_id1) and hash_manager.get_running_status(operation_id2):
        time.sleep(0.1)

    actual_result_1 = hash_manager.read_next_log_line_and_free().decode("utf-8")
    actual_result_2 = hash_manager.read_next_log_line_and_free().decode("utf-8")
    expected_result_1 = Utils.build_result(1, FILES_DETAILS.file1_path, FILES_DETAILS.file1_hash)
    expected_result_2 = Utils.build_result(2, FILES_DETAILS.file1_path, FILES_DETAILS.file1_hash)

    assert (
        expected_result_1.lower() in actual_result_1.lower()
    ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result_1}\n{actual_result_1}"
    assert (
        expected_result_2.lower() in actual_result_2.lower()
    ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result_2}\n{actual_result_2}"


@pytest.mark.skip(reason="BUG: Incorrect MD5 hash calculation")
def test_multiple_files_dir_hash(hash_manager):
    operation_id = hash_manager.hash_directory(DIRS_PATH.multiple_files_dir)
    assert operation_id > 0

    while hash_manager.get_running_status(operation_id):
        time.sleep(0.1)

    actual_result_1 = hash_manager.read_next_log_line_and_free().decode("utf-8")
    actual_result_2 = hash_manager.read_next_log_line_and_free().decode("utf-8")

    expected_result_1 = Utils.build_result(1, FILES_DETAILS.file2_path, FILES_DETAILS.file2_hash)
    expected_result_2 = Utils.build_result(2, FILES_DETAILS.file3_path, FILES_DETAILS.file3_hash)

    assert (
        expected_result_1.lower() in actual_result_1.lower()
    ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result_1}\n{actual_result_1}"
    assert (
        expected_result_2.lower() in actual_result_2.lower()
    ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result_2}\n{actual_result_2}"


@pytest.mark.skip(reason="BUG: Incorrect MD5 hash calculation")
def test_non_ascii_file_dir_hash(utils):
    actual_result = utils.get_one_file_directory_hash(DIRS_PATH.non_ascii_files_dir)
    expected_result = Utils.build_result(1, FILES_DETAILS.non_ascii_file_path, FILES_DETAILS.non_ascii_file_hash)

    assert (
        actual_result.lower() == expected_result.lower()
    ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result}\n{actual_result}"


# TODO: 100MB+ files directory hash test
# Note: Could not upload the 100MB+ file in GitHub repository
