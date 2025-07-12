from dataclasses import dataclass
from dirs_path import DIRS_PATH


@dataclass
class FilesDetails:
    __file1_name = "file_1.txt"
    file1_path = f"{DIRS_PATH.one_file_dir}/{__file1_name}"
    file1_hash = "8570DE03CE24E522B194D9093923F39F"

    __file2_name = "file_2.txt"
    file2_path = f"{DIRS_PATH.multiple_files_dir}/{__file2_name}"
    file2_hash = "CBD024D843EFC08CC4BE00C40182F96E"

    __file3_name = "file_3.txt"
    file3_path = f"{DIRS_PATH.multiple_files_dir}/{__file3_name}"
    file3_hash = "F93808AA6E9C27A4FF6CAF62F8BD74D2"

    __non_ascii_file_name = "测试文件.txt"
    non_ascii_file_path = f"{DIRS_PATH.non_ascii_files_dir}/{__non_ascii_file_name}"
    non_ascii_file_hash = "8683FD63023B55B239D3F13DE785328F"

    __long_non_ascii_path_file_name = "ファイル.txt"
    long_non_ascii_path_file_path = f"{DIRS_PATH.long_non_ascii_path_dir}/{__long_non_ascii_path_file_name}"
    long_non_ascii_path_file_hash = "8683FD63023B55B239D3F13DE785328F"


FILES_DETAILS = FilesDetails()
