import sys
import pytest
import time


sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from dirs_path import DIRS_PATH
from files_hash import FILES_HASH
from hash import HashWrapper, Hash
from utils import Utils
from ctypes import *


def test_init_then_terminate():
    wrapper = HashWrapper()

    wrapper.HashInit()

    terminate_result = wrapper.HashTerminate()
    assert (
        terminate_result == 0
    ), f"HashTerminate failed with error code: {wrapper.get_error_from_code(terminate_result)}"


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_hash_dir_then_stop():
    wrapper = HashWrapper()

    try:
        wrapper.HashInit()

        operation_id = c_size_t()
        wrapper.HashDirectory(DIRS_PATH.multipleFilesDir.encode("utf-8"), operation_id)

        stop_result = wrapper.HashStop(operation_id)
        assert stop_result == 0, f"HashStop failed with error code: {wrapper.get_error_from_code(stop_result)}"
    finally:
        Hash(wrapper).terminate()


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_hash_dir_then_terminate():
    wrapper = HashWrapper()

    try:
        wrapper.HashInit()

        operation_id = c_size_t()
        wrapper.HashDirectory(DIRS_PATH.multipleFilesDir.encode("utf-8"), operation_id)

        terminate_result = wrapper.HashTerminate()
        assert (
            terminate_result == 0
        ), f"HashTerminate failed with error code: {wrapper.get_error_from_code(terminate_result)}"
    finally:
        Hash(wrapper).terminate()


@pytest.mark.skip(reason="TODO: Define how to ignore the 'std::filesystem::__cxx11::filesystem_error' error")
def test_hash_dir_with_invalid_path():
    wrapper = HashWrapper()
    wrapper.HashInit()

    operation_id = c_size_t()
    try:
        result = wrapper.HashDirectory("invalid_path".encode("utf-8"), byref(operation_id))
    except:
        pass
    finally:
        assert result != 0, f"HashDirectory should fail with error code, got {result}"
        assert operation_id.value == 0

    Hash(wrapper).terminate()


@pytest.mark.skip(reason="BUG: MD5 Hash is calculated incorrectly")
def test_hash_one_file_dir():
    wrapper = HashWrapper()
    hash = Hash(wrapper)
    utils = Utils(wrapper)

    try:
        hash.initialize()

        result = utils.get_directory_hash(DIRS_PATH.oneFileDir)

        correct_result = utils.build_result(1, FILES_HASH.file1_path, FILES_HASH.file1_hash)

        assert (
            correct_result.lower() in result.lower()
        ), f"Result is incorrect\nExpected result above; Actual result below:\n{correct_result}\n{result}"
    finally:
        hash.terminate()


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_hash_empty_dir():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    try:
        hash.initialize()

        operation_id = c_size_t()
        result = wrapper.HashDirectory(DIRS_PATH.emptyDir.encode("utf-8"), byref(operation_id))

        assert result != 0, f"HashDirectory should fail with error code 1, got {result}"

        assert hash.get_running_status() == False, "Hash operation should not be running"
    finally:
        hash.terminate()


# TODO: Finish the test
@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_two_parallel_hashes():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    try:
        hash.initialize()

        operation_id1 = hash.hash_directory(DIRS_PATH.oneFileDir)
        operation_id2 = hash.hash_directory(DIRS_PATH.multipleFilesDir)

        assert operation_id1 > 0, "First operation ID should be greater than 0"
        assert operation_id2 == operation_id1 + 1, "Second operation ID should be greater than first operation ID"

        assert hash.get_running_status(operation_id1), "First operation should be running"
        assert hash.get_running_status(operation_id2), "Second operation should be running"

        while hash.get_running_status(operation_id1) and hash.get_running_status(operation_id2):
            time.sleep(0.1)

        line_ptr1 = hash.read_next_log_line()
        line_ptr2 = hash.read_next_log_line()

        print(f"First log line: {line_ptr1.value.decode('utf-8')}")
        print(f"Second log line: {line_ptr2.value.decode('utf-8')}")

        assert line_ptr1.value is not None, "First log line should not be None"
        assert line_ptr2.value is not None, "Second log line should not be None"
    finally:
        hash.terminate()


def test_multiple_files_dir_hash():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    try:
        hash.initialize()

        operation_id = hash.hash_directory(DIRS_PATH.multipleFilesDir)

        assert operation_id > 0, "Operation ID should be greater than 0"
        assert hash.get_running_status(operation_id), "Hash operation should be running"

        while hash.get_running_status(operation_id):
            time.sleep(0.1)

        line_ptr = hash.read_next_log_line()
        print(f"Log line: {line_ptr.value.decode('utf-8')}")
        assert line_ptr.value is not None, "Log line should not be None"
    finally:
        hash.terminate()
