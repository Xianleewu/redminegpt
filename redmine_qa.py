import os
from typing import List

class RedmineQAItem:
    def __init__(self) -> None:
        self.question = ""
        self.answer = ""

    def __str__(self) -> str:
        return f"{self.question}:{self.answer}"

class RedmineQALibrary:
    def __init__(self) -> None:
        self.qa_items: List[RedmineQAItem] = []
        self.maintainer: str = ""
        self.last_update: str = ""
        
    def __str__(self) -> str:
        return f"{self.maintainer}:{self.last_update}"

class RedmineQAManager:
    def __init__(self) -> None:
        self.qa_libraries: List[RedmineQALibrary] = []

    def add_qa_library(self, qa_library: RedmineQALibrary) -> None:
        self.qa_libraries.append(qa_library)

    def remove_qa_library(self, qa_library: RedmineQALibrary) -> None:
        self.qa_libraries.remove(qa_library)

    def load_qa_libraries_from_excel(self, file_path: str) -> None:
        with open(file_path, "r") as f:
            for line in f.readlines():
                qa_library = RedmineQALibrary()
                qa_library.maintainer = line.split(":")[0]
                qa_library.last_update = line.split(":")[1]
                self.qa_libraries.append(qa_library)

    def __str__(self) -> str:
        # print all qaa libraries
        for qa_library in self.qa_libraries:
            print(qa_library.maintainer)
            print(qa_library.last_update)
            print(qa_library.qa_items)