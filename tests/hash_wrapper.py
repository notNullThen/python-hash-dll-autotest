import ctypes
import os
from ctypes import *


ERROR_MAP = {
    1: "Unknown error",
    2: "Standard exception encountered",
    3: "Memory allocation failed",
    4: "Reading an empty log",
    5: "Invalid argument passed to a function",
    6: "Empty argument passed to a function",
    7: "Library is not initialized",
    8: "Library is already initialized",
}


class HashWrapper:
    def __init__(self):
        lib_path = os.path.abspath("./bin/linux/libhash.so")
        self.lib = ctypes.CDLL(lib_path)
        self._setup_prototypes()

    def _setup_prototypes(self):
        self.lib.HashInit.restype = c_uint32
        self.lib.HashTerminate.restype = c_uint32
        self.lib.HashDirectory.argtypes = [c_char_p, POINTER(c_size_t)]
        self.lib.HashDirectory.restype = c_uint32
        self.lib.HashStatus.argtypes = [c_size_t, POINTER(c_bool)]
        self.lib.HashStatus.restype = c_uint32
        self.lib.HashReadNextLogLine.argtypes = [POINTER(c_char_p)]
        self.lib.HashReadNextLogLine.restype = c_uint32
        self.lib.HashFree.argtypes = [c_void_p]
        self.lib.HashStop.argtypes = [c_size_t]
        self.lib.HashStop.restype = c_uint32

    def initialize(self):
        print("Initializing the hash library...")
        result = self.lib.HashInit()
        self._check_for_error(result)

    def terminate(self):
        print("Terminating the hash library...")
        result = self.lib.HashTerminate()
        self._check_for_error(result)

    def hash_directory(self, directory):
        print(f"Hashing the contents of a '{directory}' directory...")
        operation_id = c_size_t()
        result = self.lib.HashDirectory(directory.encode("utf-8"), byref(operation_id))
        self._check_for_error(result)

        return operation_id.value

    def read_next_log_line(self):
        print("Reading the next log line from the hash operation...")

        line_ptr = c_char_p()
        result = self.lib.HashReadNextLogLine(byref(line_ptr))
        self._check_for_error(result)

        return line_ptr

    def get_status(self, operation_id) -> bool:
        print("Checking the status of a hashing operation...")

        running = c_bool(True)
        result = self.lib.HashStatus(c_size_t(operation_id), byref(running))
        self._check_for_error(result)

        return running.value

    def stop(self, operation_id):
        print(f"Stopping the '{operation_id}' operation...")
        result = self.lib.HashStop(c_size_t(operation_id))
        self._check_for_error(result)

    def free(self, pointer):
        print("Releasing memory allocated by functions...")

        self.lib.HashFree(pointer)

    def _check_for_error(self, code):
        if code == 0:
            return
        raise Exception(ERROR_MAP.get(code, f"Unknown error code: {code}"))
