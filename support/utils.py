from hash import Hash
from hash_wrapper import HashWrapper
import time


class Utils:
    def __init__(self, wrapper: HashWrapper):
        self.wrapper = wrapper
        self.hash = Hash(wrapper)

    def get_directory_hash(self, directoryPath: str):
        operation_id_value = self.hash.hash_directory(directoryPath)

        while self.hash.get_running_status(operation_id_value):
            time.sleep(0.1)

        line_ptr = self.hash.read_next_log_line()
        return line_ptr.value.decode("utf-8")
