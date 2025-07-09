import ctypes
import os
from ctypes import *
from hash_wrapper import HashWrapper


class Hash:
    def __init__(self, hash_wrapper: HashWrapper):
        self.wrapper = hash_wrapper

    def initialize(self):
        print("Initializing the hash library...\n")
        result = self.wrapper.HashInit()
        self._check_for_error(result)

    def terminate(self):
        print("Terminating the hash library...\n")
        result = self.wrapper.HashTerminate()
        self._check_for_error(result)

    def hash_directory(self, directory):
        print(f"Hashing the contents of a '{directory}' directory...\n")
        operation_id = c_size_t()
        result = self.wrapper.HashDirectory(
            directory.encode("utf-8"), byref(operation_id)
        )
        self._check_for_error(result)

        return operation_id.value

    def read_next_log_line(self):
        print("Reading the next log line from the hash operation...\n")

        line_ptr = c_char_p()
        result = self.wrapper.HashReadNextLogLine(byref(line_ptr))
        self._check_for_error(result)

        return line_ptr

    def get_status(self, operation_id) -> bool:
        running = c_bool(True)
        result = self.wrapper.HashStatus(c_size_t(operation_id), byref(running))
        self._check_for_error(result)

        return running.value

    def stop(self, operation_id):
        print(f"Stopping the '{operation_id}' operation...\n")
        result = self.wrapper.HashStop(c_size_t(operation_id))
        self._check_for_error(result)

    def free(self, pointer):
        print(f"Cleaning up pointer memory...\n")

        self.wrapper.HashFree(pointer)

    def _check_for_error(self, code):
        if code == 0:
            return
        raise Exception(self.wrapper.get_error_from_code(code))
