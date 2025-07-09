from dataclasses import dataclass
from dirs_path import DIRS_PATH


@dataclass
class FilesHash:
    file1_name = "file1.txt"
    file1_path = f"{DIRS_PATH.oneFileDir}/file1.txt"
    file1_hash = "8570DE03CE24E522B194D9093923F39F"

    file2_name = "file2.txt"
    file2_path = f"{DIRS_PATH.multipleFilesDir}/file2.txt"
    file2txt = "cbd024d843efc08cc4be00c40182f96e"


FILES_HASH = FilesHash()
