import time
import pytest
from ctypes import *
from dirs_path import DIRS_PATH
from files_hash import FILES_HASH
from utils import Utils


def test_init_then_terminate(hash_wrapper):
    terminate_result = hash_wrapper.HashTerminate()
    assert (
        terminate_result == 0
    ), f"HashTerminate failed with error code: {hash_wrapper.get_error_from_code(terminate_result)}"


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_hash_dir_then_stop(hash_wrapper):
    operation_id = c_size_t()
    hash_wrapper.HashDirectory(DIRS_PATH.multipleFilesDir.encode("utf-8"), byref(operation_id))

    stop_result = hash_wrapper.HashStop(operation_id)
    assert stop_result == 0, f"HashStop failed with error code: {hash_wrapper.get_error_from_code(stop_result)}"


def test_hash_dir_then_terminate(hash_wrapper):
    operation_id = c_size_t()
    hash_wrapper.HashDirectory(DIRS_PATH.multipleFilesDir.encode("utf-8"), byref(operation_id))

    time.sleep(1)
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


@pytest.mark.skip(reason="BUG: MD5 Hash is calculated incorrectly | BUG: Memory is being managed incorrectly")
def test_hash_one_file_dir(utils):
    actual_result = utils.get_directory_hash(DIRS_PATH.oneFileDir)
    expected_result = Utils.build_result(1, FILES_HASH.file1_path, FILES_HASH.file1_hash)
    assert (
        expected_result.lower() in actual_result.lower()
    ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result}\n{actual_result}"


@pytest.mark.skip(reason="BUG: Memory is being managed incorrectly")
def test_hash_empty_dir(hash_manager, hash_wrapper):
    operation_id = c_size_t()
    hash_wrapper.HashDirectory(DIRS_PATH.emptyDir.encode("utf-8"), byref(operation_id))

    while hash_manager.get_running_status(operation_id.value):
        time.sleep(0.1)

    line_ptr = c_char_p()
    result = hash_wrapper.HashReadNextLogLine(line_ptr)

    assert result != 0, f"HashDirectory should fail with error code 1, got {result}"
    assert not hash_manager.get_running_status(operation_id.value), "Hash operation should not be running"


@pytest.mark.skip(reason="BUG: Mixes results into one line if hashing 2 folders in parallel")
def test_two_parallel_hashes(hash_manager):
    operation_id1 = hash_manager.hash_directory(DIRS_PATH.oneFileDir)
    operation_id2 = hash_manager.hash_directory(DIRS_PATH.multipleFilesDir)

    assert operation_id1 > 0
    assert operation_id2 == operation_id1 + 1

    assert hash_manager.get_running_status(operation_id1)
    assert hash_manager.get_running_status(operation_id2)

    while hash_manager.get_running_status(operation_id1) or hash_manager.get_running_status(operation_id2):
        time.sleep(0.1)

    actual_result = hash_manager.read_next_log_line().decode("utf-8")
    expected_result_1 = Utils.build_result(1, FILES_HASH.file1_path, FILES_HASH.file1_hash)
    expected_result_2 = Utils.build_result(2, FILES_HASH.file2_path, FILES_HASH.file2_hash)
    expected_result = f"{expected_result_1}\n{expected_result_2}"

    assert (
        expected_result.lower() in actual_result.lower()
    ), f"First result is incorrect\nExpected result:\n{expected_result}\nActual result:\n{actual_result}\n"


def test_multiple_files_dir_hash(hash_manager):
    operation_id = hash_manager.hash_directory(DIRS_PATH.multipleFilesDir)
    assert operation_id > 0

    while hash_manager.get_running_status(operation_id):
        time.sleep(0.1)

    result = hash_manager.read_next_log_line()
    print(f"Log line: {result.decode('utf-8')}")
