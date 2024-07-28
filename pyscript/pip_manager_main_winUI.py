
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout

from pip_manager_main_win_ui import *
from ConsoleTextBrowser import *


class Manager_UI(Ui_MainWindow, QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.parameter_init()
        self.signal_connections()
        self.ui_init()

    def parameter_init(self):
        pass

    def signal_connections(self):
        self.pb_all_clear.clicked.connect(self.all_clear)

    def ui_init(self):
        layout = QHBoxLayout(self.frame_textbrowser)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.textbrowser = Console_TextBrowser()
        layout.addWidget(self.textbrowser)

    def all_clear(self):
        self.textbrowser.clear()
        self.le_package_path.clear()
        self.le_single_command.clear()
        self.cbb_install_env.clear()
        self.listWidget.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Manager_UI()
    exe.show()
    sys.exit(app.exec_())
