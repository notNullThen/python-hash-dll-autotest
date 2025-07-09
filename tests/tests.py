import time
from support.hash import Hash

directoryPath = "./testData"
hash = Hash()


def test_memory_clean_up():
    operation_id = None

    try:
        hash.initialize()

        operation_id = hash.hash_directory(directoryPath)

        while hash.get_status(operation_id):
            time.sleep(0.1)

        line_ptr = hash.read_next_log_line()
        result_value = line_ptr.value

        print(result_value.decode("utf-8"))

        hash.free(line_ptr)

        assert (
            line_ptr.value is None
        ), f'Memory was not freed up correctly! line_ptr.value is: "{line_ptr.value}"'
    finally:
        hash.stop(operation_id)
        hash.terminate()


def test_multiple_hashes():
    try:
        hash.initialize()

        operation_id = hash.hash_directory(directoryPath)

        while hash.get_status(operation_id):
            time.sleep(0.1)

        line_ptr = hash.read_next_log_line()
        result_value = line_ptr.value

        print(result_value.decode("utf-8"))
    finally:
        hash.stop(operation_id)
        hash.terminate()
