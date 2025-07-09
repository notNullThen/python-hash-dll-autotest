from hash_manager import HashManager
from hash_wrapper import HashWrapper
import time


class Utils:
    def __init__(self, wrapper: HashWrapper):
        self.wrapper = wrapper
        self.manager = HashManager(wrapper)

    def get_directory_hash(self, directoryPath: str):
        operation_id_value = self.manager.hash_directory(directoryPath)

        assert operation_id_value > 0, "Operation ID should be greater than 0"

        while self.manager.get_running_status(operation_id_value):
            time.sleep(0.1)

        result = self.manager.read_next_log_line()
        return result.decode("utf-8")

    @staticmethod
    def build_result(operation_id: int, file_path: str, file_hash: str):
        return f"{operation_id} {file_path} {file_hash}"
