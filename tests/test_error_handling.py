from ctypes import *
from hash_wrapper import HashWrapper

# Error codes for the hash library
# 1: Unknown error
# 2: Standard exception encountered
# 3: Memory allocation failed
# 4: Reading an empty log
# ✅ 5: Invalid argument passed to a function
# ✅ 6: Empty argument passed to a function
# 7: Library is not initialized
# 8: Library is already initialized


def assert_error(expected_error: int, actual_error: int, function_name: str, hash_wrapper: HashWrapper):
    assert (
        actual_error == expected_error or actual_error == expected_error
    ), f"Error code of '{function_name}' shoud be '{hash_wrapper.get_error_from_code(expected_error)}'\nbut was: '{hash_wrapper.get_error_from_code(actual_error)}'"


def test_invalid_argument_passed_to_a_function(hash_wrapper_no_types):
    wrapper = hash_wrapper_no_types

    def assert_error(function_name: str, error_code, hash_wrapper: HashWrapper):
        assert (
            error_code == 5 or error_code == 6
        ), f"Error code of '{function_name}' shoud be '{hash_wrapper.get_error_from_code(5)}' or '{hash_wrapper.get_error_from_code(6)}'\nbut was: '{hash_wrapper.get_error_from_code(error_code)}'"

    Directory_result = wrapper.HashDirectory(None, None)
    Free_result = wrapper.HashFree(None)
    ReadNextLogLine_result = wrapper.HashReadNextLogLine(None)
    Status_result = wrapper.lib.HashStatus(None, None)
    Stop_result = wrapper.HashStop(None)

    assert_error("HashDirectory", Directory_result, wrapper)
    # TODO: Unskip line below when "HashFree does not return valid error code" bug is fixed
    # assert_error("HashFree", Free_result, wrapper)
    assert_error("HashReadNextLogLine", ReadNextLogLine_result, wrapper)
    assert_error("HashStatus", Status_result, wrapper)
    assert_error("HashStop", Stop_result, wrapper)


def test_library_is_not_initialized(hash_wrapper_no_types):
    wrapper = hash_wrapper_no_types
    assert wrapper.HashTerminate() == 0, "Termination was not successful"

    HashDirectory_result = wrapper.HashDirectory(None, None)
    HashFree_result = wrapper.HashFree(None)
    HashReadNextLogLine_result = wrapper.HashReadNextLogLine(None)
    HashStatus_result = wrapper.HashStatus(None, None)
    HashStop_result = wrapper.HashStop(c_size_t(1))
    HashTerminate_result = wrapper.HashTerminate()

    assert_error(7, HashDirectory_result, "HashDirectory", wrapper)
    # TODO: Unskip line below when "HashFree does not return valid error code" bug is fixed
    # assert_error(7, HashFree_result, "HashFree", wrapper)
    assert_error(7, HashReadNextLogLine_result, "HashReadNextLogLine", wrapper)
    assert_error(7, HashStatus_result, "HashStatus", wrapper)
    assert_error(7, HashStop_result, "HashStop", wrapper)
    assert_error(7, HashTerminate_result, "HashTerminate", wrapper)
