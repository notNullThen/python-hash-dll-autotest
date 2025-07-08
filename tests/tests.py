import time
from tests.hash_wrapper import HashWrapper


hash_wrapper = HashWrapper()

hash_wrapper.initialize()
operation_id = hash_wrapper.hash_directory("./testData")

while hash_wrapper.get_status(operation_id):
    time.sleep(0.1)

line_ptr = hash_wrapper.read_next_log_line()
result = line_ptr.value.decode("utf-8")
hash_wrapper.free(line_ptr)

hash_wrapper.terminate()

print(result)
