from dataclasses import dataclass


@dataclass
class DirsPath:
    empty_dir = "./testData/empty_dir"
    one_file_dir = "./testData/one_file_dir"
    multiple_files_dir = "./testData/multiple_files_dir"
    non_ascii_files_dir = "./testData/non_ascii_file_name"
    long_non_ascii_path_dir = "./testData/long_non_ascii_path_dir"


DIRS_PATH = DirsPath()
