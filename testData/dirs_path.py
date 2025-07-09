from dataclasses import dataclass


@dataclass
class DirsPath:
    emptyDir = "./testData/emptyFolder"
    oneFileDir = "./testData/oneFileFolder"
    multipleFilesDir = "./testData/multipleFilesFolder"


DIRS_PATH = DirsPath()
