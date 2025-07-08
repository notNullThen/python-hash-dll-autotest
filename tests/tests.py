import time
import pytest
from hash_wrapper import HashWrapper

hash_wrapper = HashWrapper()


def get_directory_hash(path: str):
    operation_id = hash_wrapper.hash_directory(path)

    while hash_wrapper.get_status(operation_id):
        time.sleep(0.1)
    line_ptr = hash_wrapper.read_next_log_line()

    return line_ptr


def test_memory_clean_up():
    hash_wrapper.initialize()

    operation_id = hash_wrapper.hash_directory("./testData")

    while hash_wrapper.get_status(operation_id):
        time.sleep(0.1)

    line_ptr = hash_wrapper.read_next_log_line()
    result_value = line_ptr.value

    print(result_value.decode("utf-8"))

    hash_wrapper.free(line_ptr)

    assert (
        line_ptr.value is None
    ), f'Memory was not freed up correctly! line_ptr.value is: "{line_ptr.value}"'

    hash_wrapper.terminate()


def test_multiple_hashes():
    directoryPath = "./testData"

    hash_wrapper.initialize()

    result = get_directory_hash(directoryPath).value

    print(result.decode("utf-8"))

    hash_wrapper.terminate()
