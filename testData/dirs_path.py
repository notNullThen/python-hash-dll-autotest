from dataclasses import dataclass


@dataclass
class DirsPath:
    emptyDir = "./testData/emptyDir"
    oneFileDir = "./testData/oneFileDir"
    multipleFilesDir = "./testData/multipleFilesDir"


DIRS_PATH = DirsPath()
