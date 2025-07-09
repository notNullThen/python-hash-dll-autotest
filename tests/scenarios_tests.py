import sys

sys.path.insert(0, "./support")

import pytest
from hash import HashWrapper, Hash
from ctypes import *


directoryPath = "./testData"


def test_hash_init():
    wrapper = HashWrapper()

    try:
        init_result = wrapper.HashInit()

        assert (
            init_result == 0
        ), f"HashInit failed with error code: {wrapper.get_error_from_code(init_result)}"
    finally:
        Hash(wrapper).terminate()


def test_init_then_terminate():
    wrapper = HashWrapper()

    wrapper.HashInit()

    terminate_result = wrapper.HashTerminate()
    assert (
        terminate_result == 0
    ), f"HashTerminate failed with error code: {wrapper.get_error_from_code(terminate_result)}"


@pytest.mark.skip(
    reason="BUG: HashStop() and HashTerminate() freeze the program if operation is not finished"
)
def test_hash_dir_then_stop():
    wrapper = HashWrapper()

    try:
        wrapper.HashInit()

        operation_id = c_size_t()
        wrapper.HashDirectory(directoryPath.encode("utf-8"), operation_id)

        stop_result = wrapper.HashStop(operation_id)
        assert (
            stop_result == 0
        ), f"HashStop failed with error code: {wrapper.get_error_from_code(stop_result)}"
    finally:
        Hash(wrapper).terminate()


@pytest.mark.skip(
    reason="BUG: HashStop() and HashTerminate() freeze the program if operation is not finished"
)
def test_hash_dir_then_terminate():
    wrapper = HashWrapper()

    try:
        wrapper.HashInit()

        operation_id = c_size_t()
        wrapper.HashDirectory(directoryPath.encode("utf-8"), operation_id)

        terminate_result = wrapper.HashTerminate()
        assert (
            terminate_result == 0
        ), f"HashTerminate failed with error code: {wrapper.get_error_from_code(terminate_result)}"
    finally:
        Hash(wrapper).terminate()
