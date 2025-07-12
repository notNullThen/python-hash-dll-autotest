from dataclasses import dataclass
from dirs_path import DIRS_PATH


@dataclass
class FilesDetails:
    file1_name = "file_1.txt"
    file1_path = f"{DIRS_PATH.one_file_dir}/file_1.txt"
    file1_hash = "8570DE03CE24E522B194D9093923F39F"

    file2_name = "file_2.txt"
    file2_path = f"{DIRS_PATH.multiple_files_dir}/file_2.txt"
    file2_hash = "CBD024D843EFC08CC4BE00C40182F96E"

    file3_name = "file_3.txt"
    file3_path = f"{DIRS_PATH.multiple_files_dir}/file_3.txt"
    file3_hash = "F93808AA6E9C27A4FF6CAF62F8BD74D2"


FILES_DETAILS = FilesDetails()
