import pytest
from dirs_path import DIRS_PATH
from ctypes import *
from hash_wrapper import HashWrapper


def assert_error(expected_error: int, actual_error: int, function_name: str, hash_wrapper: HashWrapper):
    assert (
        actual_error == expected_error
    ), f"Error code of {function_name} shoud be '{hash_wrapper.get_error_from_code(expected_error)}'\nbut was: '{hash_wrapper.get_error_from_code(actual_error)}'"


# ✅ 4: Reading an empty log
@pytest.mark.skip(
    reason='BUG: HashReadNextLogLine returns "1: Unknown error" error instead of "4: Reading an empty log"'
)
def test_reading_an_empty_log(hash_wrapper, hash_manager):
    hash_manager.hash_directory(DIRS_PATH.empty_dir)

    line_ptr = c_char_p()
    HashReadNextLogLine_result = hash_wrapper.HashReadNextLogLine(line_ptr)

    assert_error(4, HashReadNextLogLine_result, "HashReadNextLogLine()", hash_wrapper)


# ✅ 5: Invalid argument passed to a function
# ✅ 6: Empty argument passed to a function
def test_invalid_argument_passed_to_a_function(hash_wrapper_no_types):
    wrapper = hash_wrapper_no_types

    def assert_error(function_name: str, error_code, hash_wrapper: HashWrapper):
        assert (
            error_code == 5 or error_code == 6
        ), f"Error code of {function_name} shoud be '{hash_wrapper.get_error_from_code(5)}' or '{hash_wrapper.get_error_from_code(6)}'\nbut was: '{hash_wrapper.get_error_from_code(error_code)}'"

    Directory_result = wrapper.HashDirectory(None, None)
    Free_result = wrapper.HashFree(None)
    ReadNextLogLine_result = wrapper.HashReadNextLogLine(None)
    Status_result = wrapper.lib.HashStatus(None, None)
    Stop_result = wrapper.HashStop(None)

    assert_error("HashDirectory()", Directory_result, wrapper)
    # TODO: Unskip line below when "HashFree does not return valid error code" bug is fixed
    # assert_error("HashFree()", Free_result, wrapper)
    assert_error("HashReadNextLogLine()", ReadNextLogLine_result, wrapper)
    assert_error("HashStatus()", Status_result, wrapper)
    assert_error("HashStop()", Stop_result, wrapper)


# ✅ 7: Library is not initialized
def test_library_is_not_initialized(hash_wrapper_no_types):
    wrapper = hash_wrapper_no_types

    assert wrapper.HashTerminate() == 0, "Termination was not successful"

    HashDirectory_result = wrapper.HashDirectory(None, None)
    HashFree_result = wrapper.HashFree(None)
    HashReadNextLogLine_result = wrapper.HashReadNextLogLine(None)
    HashStatus_result = wrapper.HashStatus(None, None)
    HashStop_result = wrapper.HashStop(c_size_t(1))
    HashTerminate_result = wrapper.HashTerminate()

    assert_error(7, HashDirectory_result, "HashDirectory()", wrapper)
    # TODO: Unskip line below when "HashFree does not return valid error code" bug is fixed
    # assert_error(7, HashFree_result, "HashFree()", wrapper)
    assert_error(7, HashReadNextLogLine_result, "HashReadNextLogLine()", wrapper)
    assert_error(7, HashStatus_result, "HashStatus()", wrapper)
    # TODO: Unskip line below when "HashStop does not return valid error code when Hash is not initialized or terminated" bug is fixed
    # assert_error(7, HashStop_result, "HashStop()", wrapper)
    assert_error(7, HashTerminate_result, "HashTerminate()", wrapper)


# ✅ 8: Library is already initialized
@pytest.mark.skip(reason="BUG: HashInit does not return error code when the library is already initialized")
def test_library_is_already_initialized(hash_wrapper):
    hash_wrapper

    HashInit_result = hash_wrapper.HashInit()

    assert_error(8, HashInit_result, "HashInit()", hash_wrapper)
