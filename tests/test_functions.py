import sys
import pytest
import time

sys.path.insert(0, "./support")
sys.path.insert(0, "./testData")

from hash_manager import HashWrapper, HashManager
from ctypes import *
from utils import Utils
from dirs_path import DIRS_PATH


def test_HashInit():
    wrapper = HashWrapper()
    hash_manager = HashManager(wrapper)

    hash_manager.initialize()


def test_HashTerminate():
    wrapper = HashWrapper()
    manager = HashManager(wrapper)

    manager.initialize()
    manager.terminate()


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_HashDirectory():
    wrapper = HashWrapper()
    manager = HashManager(wrapper)

    try:
        manager.initialize()

        operation_id_value = manager.hash_directory(DIRS_PATH.multipleFilesDir)
        assert operation_id_value > 0, "Operation ID should be greater than 0"
    finally:
        manager.terminate()


def test_HashReadNextLogLine():
    wrapper = HashWrapper()
    manager = HashManager(wrapper)
    utils = Utils(wrapper)

    try:
        manager.initialize()

        result = utils.get_directory_hash(DIRS_PATH.multipleFilesDir)

        assert result is not None, "Log line should not be None"
    finally:
        manager.terminate()


def test_HashStatus():
    wrapper = HashWrapper()
    manager = HashManager(wrapper)

    try:
        manager.initialize()

        operation_id_value = manager.hash_directory(DIRS_PATH.multipleFilesDir)
        assert operation_id_value > 0, "Operation ID should be greater than 0"

        status = manager.get_running_status(operation_id_value)
        assert status is True, "Status should be True while operation is running"

        while manager.get_running_status(operation_id_value):
            time.sleep(0.1)

        assert (
            manager.get_running_status(operation_id_value) is False
        ), "Status should be False after operation is finished"
    finally:
        manager.terminate()


@pytest.mark.skip(reason="BUG: HashStop() and HashTerminate() freeze if operation is not finished")
def test_HashStop():
    wrapper = HashWrapper()
    manager = HashManager(wrapper)

    try:
        manager.initialize()

        operation_id_value = manager.hash_directory(DIRS_PATH.multipleFilesDir)
        assert operation_id_value > 0, "Operation ID should be greater than 0"

        status = manager.get_running_status(operation_id_value)
        assert status is True, "Status should be False after stopping the operation"

        manager.stop(operation_id_value)

        status = manager.get_running_status(operation_id_value)
        assert status is False, "Status should be False after stopping the operation"
    finally:
        manager.terminate()


@pytest.mark.skip(reason="BUG: HashFree() does not clean memory up correctly")
def test_HashFree():
    wrapper = HashWrapper()
    manager = HashManager(wrapper)

    try:
        manager.initialize()

        operation_id_value = manager.hash_directory(DIRS_PATH.multipleFilesDir)

        while manager.get_running_status(operation_id_value):
            time.sleep(0.1)

        line_ptr = manager.read_next_log_line()
        assert line_ptr is not None, "Log line pointer should not be None"

        manager.free(line_ptr)

        assert line_ptr.value is None, f'Memory was not freed up correctly! line_ptr.value is: "{line_ptr.value}"'
    finally:
        manager.terminate()
