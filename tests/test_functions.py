import sys
import pytest
import time

sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from hash import HashWrapper, Hash
from ctypes import *
from utils import Utils
from dirsPath import DIRS_PATH


def test_HashInit():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    hash.initialize()


def test_HashTerminate():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    hash.initialize()
    hash.terminate()


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_HashDirectory():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    try:
        hash.initialize()

        operation_id_value = hash.hash_directory(DIRS_PATH.multipleFilesDir)
        assert operation_id_value > 0, "Operation ID should be greater than 0"
    finally:
        hash.terminate()


def test_HashReadNextLogLine():
    wrapper = HashWrapper()
    hash = Hash(wrapper)
    utils = Utils(wrapper)

    try:
        hash.initialize()

        result = utils.get_directory_hash(DIRS_PATH.multipleFilesDir)

        assert result is not None, "Log line should not be None"
    finally:
        hash.terminate()


def test_HashStatus():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    try:
        hash.initialize()

        operation_id_value = hash.hash_directory(DIRS_PATH.multipleFilesDir)
        assert operation_id_value > 0, "Operation ID should be greater than 0"

        status = hash.get_running_status(operation_id_value)
        assert status is True, "Status should be True while operation is running"

        while hash.get_running_status(operation_id_value):
            time.sleep(0.1)

        assert (
            hash.get_running_status(operation_id_value) is False
        ), "Status should be False after operation is finished"
    finally:
        hash.terminate()


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_HashStop():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    try:
        hash.initialize()

        operation_id_value = hash.hash_directory(DIRS_PATH.multipleFilesDir)
        assert operation_id_value > 0, "Operation ID should be greater than 0"

        status = hash.get_running_status(operation_id_value)
        assert status is True, "Status should be False after stopping the operation"

        hash.stop(operation_id_value)

        status = hash.get_running_status(operation_id_value)
        assert status is False, "Status should be False after stopping the operation"
    finally:
        hash.terminate()


@pytest.mark.skip(reason="BUG: HashFree() does not clean memory up correctly")
def test_HashFree():
    wrapper = HashWrapper()
    hash = Hash(wrapper)

    try:
        hash.initialize()

        operation_id_value = hash.hash_directory(DIRS_PATH.multipleFilesDir)

        while hash.get_running_status(operation_id_value):
            time.sleep(0.1)

        line_ptr = hash.read_next_log_line()
        assert line_ptr is not None, "Log line pointer should not be None"

        hash.free(line_ptr)

        assert line_ptr.value is None, f'Memory was not freed up correctly! line_ptr.value is: "{line_ptr.value}"'
    finally:
        hash.terminate()
