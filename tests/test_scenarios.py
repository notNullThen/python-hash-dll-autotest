import sys
import pytest
import time


sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from dirs_path import DIRS_PATH
from files_hash import FILES_HASH
from hash_manager import HashWrapper, HashManager
from utils import Utils
from ctypes import *

wrapper = HashWrapper()
manager = HashManager(wrapper)
utils = Utils(wrapper)


def test_init_then_terminate():
    wrapper.HashInit()

    terminate_result = wrapper.HashTerminate()
    assert (
        terminate_result == 0
    ), f"HashTerminate failed with error code: {wrapper.get_error_from_code(terminate_result)}"


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_hash_dir_then_stop():
    try:
        wrapper.HashInit()

        operation_id = c_size_t()
        wrapper.HashDirectory(DIRS_PATH.multipleFilesDir.encode("utf-8"), operation_id)

        stop_result = wrapper.HashStop(operation_id)
        assert stop_result == 0, f"HashStop failed with error code: {wrapper.get_error_from_code(stop_result)}"
    finally:
        manager.terminate()


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_hash_dir_then_terminate():
    try:
        wrapper.HashInit()

        operation_id = c_size_t()
        wrapper.HashDirectory(DIRS_PATH.multipleFilesDir.encode("utf-8"), operation_id)

        terminate_result = wrapper.HashTerminate()
        assert (
            terminate_result == 0
        ), f"HashTerminate failed with error code: {wrapper.get_error_from_code(terminate_result)}"
    finally:
        manager.terminate()


@pytest.mark.skip(reason="TODO: Define how to ignore the 'std::filesystem::__cxx11::filesystem_error' error")
def test_hash_dir_with_invalid_path():
    wrapper.HashInit()

    operation_id = c_size_t()
    try:
        result = wrapper.HashDirectory("invalid_path".encode("utf-8"), byref(operation_id))
    except:
        pass
    finally:
        assert result != 0, f"HashDirectory should fail with error code, got {result}"
        assert operation_id.value == 0


@pytest.mark.skip(reason="BUG: MD5 Hash is calculated incorrectly | BUG: Memory is being managed incorrectly")
def test_hash_one_file_dir():
    try:
        manager.initialize()

        actual_result = utils.get_directory_hash(DIRS_PATH.oneFileDir)

        expected_result = Utils.build_result(1, FILES_HASH.file1_path, FILES_HASH.file1_hash)

        assert (
            expected_result.lower() in actual_result.lower()
        ), f"Result is incorrect\nExpected result above; Actual result below:\n{expected_result}\n{actual_result}"
    finally:
        manager.terminate()


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_hash_empty_dir():
    try:
        manager.initialize()

        operation_id = c_size_t()
        result = wrapper.HashDirectory(DIRS_PATH.emptyDir.encode("utf-8"), byref(operation_id))

        assert result != 0, f"HashDirectory should fail with error code 1, got {result}"

        assert manager.get_running_status() == False, "Hash operation should not be running"
    finally:
        manager.terminate()


@pytest.mark.skip(reason="BUG: Mixes resutls into one line if hash 2 folders paralelly")
def test_two_parallel_hashes():
    try:
        manager.initialize()

        operation_id1 = manager.hash_directory(DIRS_PATH.oneFileDir)
        operation_id2 = manager.hash_directory(DIRS_PATH.multipleFilesDir)

        assert operation_id1 > 0, "First operation ID should be greater than 0"
        assert operation_id2 == operation_id1 + 1, "Second operation ID should be greater than first operation ID"

        assert manager.get_running_status(operation_id1), "First operation should be running"
        assert manager.get_running_status(operation_id2), "Second operation should be running"

        while manager.get_running_status(operation_id1) and manager.get_running_status(operation_id2):
            time.sleep(0.1)

        actual_result = manager.read_next_log_line()

        expected_result_1 = Utils.build_result(1, FILES_HASH.file1_path, FILES_HASH.file1_hash)
        expected_result_2 = Utils.build_result(2, FILES_HASH.file2_path, FILES_HASH.file2_hash)
        expected_result = f"{expected_result_1}\n{expected_result_2}"

        assert (
            expected_result_1.lower() in actual_result.decode("utf-8").lower()
        ), f"First result is incorrect\nExpected result:\n{expected_result}\nActual result:\n{actual_result.decode('utf-8')}"

    finally:
        pass
        # TODO: Uncomment after the "HashStop() and HashTerminate() freeze if operation is not finished" bug is fixed
        # manager.terminate()


# TODO: Finish the test
def test_multiple_files_dir_hash():
    try:
        manager.initialize()

        operation_id = manager.hash_directory(DIRS_PATH.multipleFilesDir)

        assert operation_id > 0, "Operation ID should be greater than 0"
        assert manager.get_running_status(operation_id), "Hash operation should be running"

        while manager.get_running_status(operation_id):
            time.sleep(0.1)

        result = manager.read_next_log_line()
        print(f"Log line: {result.decode('utf-8')}")
    finally:
        manager.terminate()
