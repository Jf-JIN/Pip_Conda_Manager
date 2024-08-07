

from QThread_Conda_Env import *
from ConsoleTextBrowser import *
from QThread_Virtual_Environment_Manager import *


from PyQt5.QtWidgets import QDialog, QComboBox, QVBoxLayout, QLineEdit, QFrame, QLabel, QMessageBox, QSpacerItem, QFileDialog
from PyQt5.QtCore import Qt

import os
from pathlib import Path


class Env_Manual_Add(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.__parameter_init()
        self.__ui_init()
        self.__signal_connections()
        self.show()

    def __parameter_init(self):
        self.__env = None
        self.__env_path = None
        self.__root_dir = Path.home()

    def __signal_connections(self):
        self.pb_add.clicked.connect(self.__on_add_clicked)
        self.pb_cancel.clicked.connect(self.reject)
        self.pb_env_path.clicked.connect(self.__view_path)

    def __ui_init(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('手动添加环境')
        self.resize(400, 100)
        self.setFixedHeight(100)
        self.setMinimumWidth(300)
        self.le_env_path = QLineEdit()
        self.le_env_path.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cbb_env = QComboBox()
        self.cbb_env.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pb_env_path = QPushButton('浏览')
        self.le_env_path.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pb_add = QPushButton('添加')
        self.pb_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pb_cancel = QPushButton('取消')
        self.pb_cancel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        frame = QFrame()
        layout = QVBoxLayout(self)
        layout_input = QVBoxLayout(frame)
        layout_cbb = QHBoxLayout()
        layout_le = QHBoxLayout()
        layout_pb = QHBoxLayout()
        for i in [layout, layout_input, layout_cbb, layout_le, layout_pb]:
            i.setContentsMargins(0, 0, 0, 0)
            i.setSpacing(6)
        layout.setContentsMargins(5, 5, 5, 5)
        layout_cbb.addWidget(QLabel('环境类型'))
        layout_cbb.addWidget(self.cbb_env)
        layout_le.addWidget(QLabel('Python路径'))
        layout_le.addWidget(self.le_env_path, stretch=100)
        layout_le.addWidget(self.pb_env_path)
        layout_pb.addItem(QSpacerItem(100, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
        layout_pb.addWidget(self.pb_add)
        layout_pb.addWidget(self.pb_cancel)
        layout_input.addLayout(layout_cbb)
        layout_input.addLayout(layout_le)
        layout.addWidget(frame, stretch=100)
        layout.addLayout(layout_pb)
        self.cbb_env.addItem('venv')
        self.cbb_env.addItem('virtualenv')
        self.cbb_env.addItem('pipenv')
        self.cbb_env.addItem('poetry')
        self.cbb_env.addItem('pyenv')
        self.cbb_env.addItem('venvwrapper')
        self.cbb_env.addItem('Pipx')
        self.cbb_env.addItem('Hatch')
        self.cbb_env.addItem('Pex')
        self.cbb_env.addItem('Nox')
        self.cbb_env.setCurrentIndex(-1)
        self.setStyleSheet(self.__set_style_sheet())

    def __get_env(self):
        env = self.cbb_env.currentText()
        env_path = self.le_env_path.text()
        if not env or env == '':
            QMessageBox.information(None, '提示', '请选择环境类型')
        if not env_path or env_path == '':
            QMessageBox.information(None, '提示', '请输入 Python 解释器路径')
        return env, env_path

    def __on_add_clicked(self):
        env, env_path = self.__get_env()
        if os.path.basename(env_path) != 'python.exe':
            QMessageBox.information(None, '提示', '请检查 Python 解释器路径, 请输入 python.exe 路径')
            return
        if env and env_path:
            self.__env = env
            self.__env_path = env_path
            self.accept()

    def get_input(self):
        if self.result() == QDialog.Accepted:
            return self.__env, self.__env_path
        return None, None

    def __view_path(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, '添加 python 解释器路径', str(self.__root_dir), 'Python 解释器 (python.exe)', options=options)
        if file_path:
            self.le_env_path.setText(str(file_path))

    def __set_style_sheet(self):
        return '''
                    QDialog{
                        color: rgb(236, 206, 174);
                        background-color: rgb(19, 24, 66);
                    }
                    QLabel{
                        color: rgb(236, 206, 174);
                        font: 18px  '黑体';
                    }

                    QPushButton{
                        border: 0px solid;
                        border-radius: 10px;
                        font: 18px  '黑体';
                        color: rgb(19, 24, 66);
                        background-color: rgb(230, 131, 105);
                        border: 1px solid;
                        border-radius: 10px;
                        max-height: 50px;
                        min-height:25px;
                        max-width: 150px;
                        min-width: 60px;
                    }

                    QPushButton:hover{
                        font-weight: bold;
                        padding-bottom: 4px;
                        color: rgb(251, 246, 226);
                        background-color: rgb(222, 105, 69);
                    }

                    QLineEdit{
                        border: 0px solid;
                        border-radius: 10px;
                        background-color: rgb(236, 206, 174);
                        font: 18px  '黑体';
                        max-height: 40px;
                        color: rgb(19, 24, 66);
                        padding-left:5px;
                        padding-right:5px;
                    }

                    QComboBox{
                        max-height: 40px;
                        font: 18px  '黑体';
                        color: rgb(19, 24, 66);
                        border: 0px solid;
                        border-radius: 10px;
                        background-color: rgb(236, 206, 174);
                    }

                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        border-left-width: 1px;
                        border-left-style: solid;
                        border-top-right-radius: 3px;
                        border-bottom-right-radius: 3px;
                    }

                    QComboBox QAbstractItemView {
                        font: 18px  '黑体';
                        color: rgb(236, 206, 174);
                        background-color: rgb(19, 24, 66);
                        border: None;
                        selection-background-color: rgb(230, 131, 105);
                        selection-color: rgb(19, 24, 66);
                        padding: 5px;
                    }

                    QMessageBox QPushButton {
                        min-width: 60px;
                    }

                    QMessageBox QPushButton:hover{
                        padding: 0px;
                    }
                    '''
