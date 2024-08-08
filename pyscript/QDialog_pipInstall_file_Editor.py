

from PyQt5.QtGui import QCloseEvent, QKeySequence
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

from language_manager import *


class pipInstall_Editor(QDialog):
    def __init__(self, parent, file_path) -> None:
        super().__init__(parent)
        self.file_path = file_path
        self.language: Language_Manager = parent.language
        self.__parameter_init()
        self.__signal_connections()
        self.__ui_init()
        self.show()

    def __parameter_init(self):
        self.text_edit = QTextEdit(self)
        self.__flag_text_changed = False

    def __signal_connections(self):
        self.text_edit.textChanged.connect(self.__text_changed)

    def __ui_init(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(800, 600)
        self.setWindowTitle(self.file_path)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.Window)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.text_edit.setStyleSheet('''
                                        font: 18px '黑体';
                                        color: rgb(19, 24, 66);
                                        background-color: rgb(251, 246, 226);
                                        border: None;
                                    ''')
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout.addWidget(self.text_edit)
        self.__open_file()

    def __open_file(self):
        text_list = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for content in file.readlines():
                text_list.append(content.strip())
        self.text_edit.setText('\n'.join(text_list))

    def __save_file(self):
        text = self.text_edit.toPlainText()
        if '''# 注释符为'#', 无行间释符, 只有行内注释符\n''' not in text:
            text = "# 注释符为'#', 无行间释符, 只有行内注释符\n# 例如: numpy   # numpy 是一个科学计算的第三方包\n\n# The comment symbol is '#', no interline comment symbol, only intraline comment symbol\n# For example: numpy # numpy is a third-party package for scientific computing\n\n" + text

        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        self.__flag_text_changed = False

    def __text_changed(self):
        self.__flag_text_changed = True

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.text_edit.document().isModified() and self.__flag_text_changed:
            reply = QMessageBox.question(
                self,
                self.language.save_confirm,
                self.language.file_save_hint,
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            if reply == QMessageBox.Save:
                self.__save_file()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Save):
            self.__save_file()
