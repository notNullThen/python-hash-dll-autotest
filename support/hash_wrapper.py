import ctypes
import os
from ctypes import *


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

    ERROR_MAP = {
        0: "0: Success",
        1: "1: Unknown error",
        2: "2: Standard exception encountered",
        3: "3: Memory allocation failed",
        4: "4: Reading an empty log",
        5: "5: Invalid argument passed to a function",
        6: "6: Empty argument passed to a function",
        7: "7: Library is not initialized",
        8: "8: Library is already initialized",
    }

    def HashInit(self):
        return self.lib.HashInit()

    def HashTerminate(self):
        return self.lib.HashTerminate()

    def HashDirectory(self, directory: bytes, operation_id):
        return self.lib.HashDirectory(directory, operation_id)

    def HashStatus(self, operation_id, running: c_bool):
        return self.lib.HashStatus(operation_id, running)

    def HashReadNextLogLine(self, line_ptr):
        return self.lib.HashReadNextLogLine(line_ptr)

    def HashFree(self, pointer):
        return self.lib.HashFree(pointer)

    def HashStop(self, operation_id):
        return self.lib.HashStop(operation_id)

    def get_error_from_code(self, code):
        return self.ERROR_MAP.get(code, f"Unknown error code: {code}")
