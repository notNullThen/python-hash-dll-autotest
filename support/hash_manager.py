from ctypes import *
from hash_wrapper import HashWrapper


class HashManager:
    def __init__(self, hash_wrapper: HashWrapper):
        self._wrapper = hash_wrapper

    def initialize(self):
        print("Initializing the hash library...\n")
        result = self._wrapper.HashInit()
        self._check_for_error(result)

    def terminate(self):
        print("Terminating the hash library...\n")
        result = self._wrapper.HashTerminate()
        self._check_for_error(result)

    def hash_directory(self, directory):
        print(f"Hashing the contents of a '{directory}' directory...\n")
        operation_id = c_size_t()
        result = self._wrapper.HashDirectory(directory.encode("utf-8"), byref(operation_id))
        self._check_for_error(result)

        return operation_id.value

    def read_next_log_line_and_free(self):
        print("Reading the next log line from the hash operation...\n")

        line_ptr = c_char_p()

        next_log_line_result = self._wrapper.HashReadNextLogLine(byref(line_ptr))
        self._check_for_error(next_log_line_result)

        result = line_ptr.value

        self._wrapper.HashFree(line_ptr)

        return result

    def get_running_status(self, operation_id_value) -> bool:
        running = c_bool(True)
        result = self._wrapper.HashStatus(c_size_t(operation_id_value), byref(running))
        self._check_for_error(result)

        return running.value

    def stop(self, operation_id_value):
        print(f"Stopping the '{operation_id_value}' operation...\n")
        result = self._wrapper.HashStop(c_size_t(operation_id_value))
        self._check_for_error(result)

    def free(self, pointer: c_char_p):
        print(f"Cleaning up pointer memory...\n")

        self._wrapper.HashFree(pointer)

    def _check_for_error(self, code):
        if code == 0:
            return
        raise Exception(f"HASH ERROR: {self._wrapper.get_error_from_code(code)}")
