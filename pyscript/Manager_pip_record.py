
import os
import json
import copy
from Manager_language import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject


class Manager_Pip_Record(QObject):
    def __init__(self, parent_obj, folder_path) -> None:
        self.language: Language_Manager = parent_obj.language
        self.folder_path = folder_path
        self.record_path = os.path.join(self.folder_path, '.pip_record')
        self.__record = {}
        self.__check_file()

    def write(self, text: dict) -> None:
        with open(self.record_path, 'w', encoding='utf-8') as file:
            json.dump(text, file, ensure_ascii=True, indent=4)

    @property
    def record(self):
        return copy.deepcopy(self.__record)

    def __read(self):
        try:
            with open(self.record_path, 'r', encoding='utf-8') as file:
                self.__record: dict = json.load(file)
        except:
            QMessageBox.warning(None, self.language.warning, self.language.error_pip_record_read)

    def __check_file(self) -> None:
        if not os.path.exists(self.record_path):
            text: dict = {}
            self.write(text)
            self.__record = {}
        else:
            self.__read()
