from dataclasses import dataclass


@dataclass
class DirsPath:
    emptyDir: str = "./testData/emptyFolder"
    oneFileDir: str = "./testData/oneFileFolder"
    multipleFilesDir: str = "./testData/multipleFilesFolder"


DIRS_PATH = DirsPath()
