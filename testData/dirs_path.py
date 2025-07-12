from dataclasses import dataclass


@dataclass
class DirsPath:
    empty_dir = "./testData/emptyDir"
    one_file_dir = "./testData/oneFileDir"
    multiple_files_dir = "./testData/multipleFilesDir"


DIRS_PATH = DirsPath()
