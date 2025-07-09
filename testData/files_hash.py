from dataclasses import dataclass
from dirs_path import DIRS_PATH


@dataclass
class FilesHash:
    file1_name = "file1.txt"
    file1_path = f"{DIRS_PATH.oneFileDir}/file1.txt"
    file1_hash = "8570DE03CE24E522B194D9093923F39F"

    file2_name = "file2.txt"
    file2_path = f"{DIRS_PATH.multipleFilesDir}/file2.txt"
    file2_hash = "CBD024D843EFC08CC4BE00C40182F96E"

    file3_name = "file3.txt"
    file3_path = f"{DIRS_PATH.multipleFilesDir}/file3.txt"
    file3_hash = "F93808AA6E9C27A4FF6CAF62F8BD74D2"


FILES_HASH = FilesHash()
