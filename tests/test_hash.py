import os
import tempfile
import shutil
import hashlib
import ctypes
from ctypes import *
import time


# Load the shared library
lib_path = os.path.abspath("./bin/linux/libhash.so")
lib = ctypes.CDLL(lib_path)

# Define return types and argtypes
lib.HashInit.restype = c_uint32
lib.HashTerminate.restype = c_uint32
lib.HashDirectory.argtypes = [c_char_p, POINTER(c_size_t)]
lib.HashDirectory.restype = c_uint32
lib.HashStatus.argtypes = [c_size_t, POINTER(c_bool)]
lib.HashStatus.restype = c_uint32
lib.HashReadNextLogLine.argtypes = [POINTER(c_char_p)]
lib.HashReadNextLogLine.restype = c_uint32
lib.HashFree.argtypes = [c_void_p]
lib.HashStop.argtypes = [c_size_t]
lib.HashStop.restype = c_uint32

# Allocate space for the operation ID
op_id = c_size_t()

lib.HashInit()

# Start the hashing operation
result = lib.HashDirectory(b"./testData", byref(op_id))
assert result == 0

# Wait a little for the async operation to complete
running = c_bool(True)
while running.value:
    lib.HashStatus(op_id.value, byref(running))
    time.sleep(0.1)

# Read a log line (if any)
line_ptr = c_char_p()
read_result = lib.HashReadNextLogLine(byref(line_ptr))

if read_result == 0:
    hash_line = line_ptr.value.decode("utf-8")
    print("✅ Hash line:", hash_line)
    lib.HashFree(line_ptr)
else:
    print("⚠️ No result or error (code =", read_result, ")")

lib.HashTerminate()
