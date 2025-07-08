import time
from framework import HashLib


hash_lib = HashLib()

hash_lib.initialize()
operation_id = hash_lib.hash_directory("./testData")

while hash_lib.get_status(operation_id):
    time.sleep(0.1)

line_ptr = hash_lib.read_next_log_line()
result = line_ptr.value.decode("utf-8")
hash_lib.free(line_ptr)

hash_lib.terminate()

print(result)
