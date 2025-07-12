from hash_manager import HashManager
import time


class Utils:
    def __init__(self, manager: HashManager):
        self.manager = manager

    def get_one_file_directory_hash(self, directoryPath: str):
        operation_id_value = self.manager.hash_directory(directoryPath)

        assert operation_id_value > 0

        self.sleep_till_operation_done(operation_id_value)

        result = self.manager.read_next_log_line_and_free()

        return result.decode("utf-8")

    def sleep_till_operation_done(self, operation_id_value: int):
        while self.manager.get_running_status(operation_id_value):
            time.sleep(0.1)

    @staticmethod
    def build_result(operation_id: int, file_path: str, file_hash: str):
        return f"{operation_id} {file_path} {file_hash}"
