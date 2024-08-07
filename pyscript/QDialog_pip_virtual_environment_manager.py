
from QThread_Conda_Env import *
from ConsoleTextBrowser import *
from QThread_Virtual_Environment_Manager import *


from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QDialog, QTreeWidget, QComboBox, QVBoxLayout, QTreeWidgetItem, QLineEdit, QFrame, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QEventLoop

import shutil
import os


class Virtual_Environment_Manager(QDialog):
    def __init__(self, parent, env_dict) -> None:
        super().__init__(parent)
        self.env_dict: dict = env_dict
        self.__parameter_init()
        self.__ui_init()
        self.__signal_connections()
        self.show()

    def __parameter_init(self):
        pass

    def __signal_connections(self):
        self.pb_create_env.clicked.connect(self.create_new_env)
        # self.pb_export_env
        self.pb_remove_env.clicked.connect(self.remove_env)
        self.pb_update_env.clicked.connect(self.update_env)

    def __ui_init(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle('虚拟环境管理')
        self.resize(800, 600)
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setColumnWidth(0, 200)
        self.tree_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combo_box = QComboBox(self)
        self.combo_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.le_env_name = QLineEdit()
        self.le_py_version = QLineEdit()
        for i in [self.le_env_name, self.le_py_version]:
            i.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            i.setCursor(QCursor(Qt.IBeamCursor))
        self.lb_env_name = QLabel('新环境名')
        self.lb_py_version = QLabel('Python版本')
        self.text_browser = Console_TextBrowser(default_font_family='黑体', default_font_size=16)
        self.text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pb_create_env = QPushButton('新建环境')
        self.pb_export_env = QPushButton('导出环境')
        self.pb_update_env = QPushButton('更新环境')
        self.pb_remove_env = QPushButton('删除环境')
        for i in [self.pb_create_env, self.pb_export_env, self.pb_update_env, self.pb_remove_env]:
            i.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            i.setCursor(QCursor(Qt.PointingHandCursor))
        frame_edit = QFrame()
        self.frame_pb = QFrame()
        self.frame_pb.setMaximumHeight(54)
        self.frame_pb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_main = QHBoxLayout(self)
        layout_edit = QVBoxLayout(frame_edit)
        layout_create = QHBoxLayout()
        layout_pb = QHBoxLayout(self.frame_pb)
        for i in [layout_main, layout_edit, layout_pb]:
            i.setContentsMargins(0, 0, 0, 0)
            i.setSpacing(10)
        layout_main.setContentsMargins(5, 5, 5, 5)
        layout_pb.addWidget(self.pb_create_env)
        # layout_pb.addWidget(self.pb_update_env)
        # layout_pb.addWidget(self.pb_export_env)
        layout_pb.addWidget(self.pb_remove_env)
        layout_create.addWidget(self.lb_env_name)
        layout_create.addWidget(self.le_env_name)
        layout_create.addWidget(self.lb_py_version)
        layout_create.addWidget(self.le_py_version)
        layout_edit.addWidget(self.tree_widget)
        layout_edit.addWidget(self.combo_box)
        layout_edit.addLayout(layout_create)
        layout_edit.addWidget(self.frame_pb)
        layout_main.addWidget(self.text_browser, stretch=80)
        layout_main.addWidget(frame_edit, stretch=100)
        self.setStyleSheet(self.set_style_sheet())
        self.tree_display()
        self.combo_display()

    def tree_display(self):
        self.tree_widget.clear()
        for env_name, env_list in self.env_dict.items():
            if env_name == 'python':
                continue
            for env_item_list in env_list:
                item = QTreeWidgetItem(self.tree_widget)
                name = f'({env_name})'
                item.setText(0, name + env_item_list[0])
                item.setText(1, env_item_list[1])
                voll_tip_text = f'{name} {env_item_list[0]}   {env_item_list[1]}'
                item.setToolTip(0, voll_tip_text)
                item.setToolTip(1, voll_tip_text)

    def tree_update(self):
        self.env_dict['conda'] = self.get_conda_environment_list()
        self.tree_display()

    def get_conda_environment_list(self):
        '''
        获取 Conda 中的虚拟环境
        '''
        conda_env_list = []

        def set_conda_env_list(conda_env):
            nonlocal conda_env_list
            if conda_env:
                conda_env_list[:] = conda_env
                for i in conda_env_list:
                    temp_path = os.path.join(i[1], 'python.exe')
                    if os.path.exists(temp_path):
                        i[1] = temp_path
                    else:
                        i[1] = ''
                loop.quit()
        if shutil.which("conda"):
            get_conda_env_thread = QThread_Conda_Get_Env_List(self)
            get_conda_env_thread.signal_conda_env_list.connect(set_conda_env_list)
            get_conda_env_thread.start()
            loop = QEventLoop()
            loop.exec_()
            return conda_env_list
        else:
            return None

    def combo_display(self):
        for env_name, env_list in self.env_dict.items():
            if env_name == 'python':
                continue
            else:
                self.combo_box.addItem(env_name)

    def create_new_env(self):
        virtual_env = self.combo_box.currentText()
        env_name = self.le_env_name.text().strip()
        python_version = self.le_py_version.text().strip()
        if not virtual_env or env_name == '' or python_version == '':
            return
        self.thread_create_new_env = QThread_Create_New_Env(virtual_env, env_name, python_version)
        self.thread_create_new_env.signal_textbrowser.connect(self.text_browser.append_text)
        self.thread_create_new_env.signal_finished.connect(self.thread_finished)
        self.frame_pb.hide()
        self.thread_create_new_env.start()
        self.tree_update()

    def remove_env(self):
        current_item = self.tree_widget.currentItem()
        if not current_item:
            return
        confirm_dialog_result = QMessageBox.question(self, '确认删除', '删除动作不可撤回, 是否进行删除?',  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm_dialog_result == QMessageBox.No:
            return
        tree_item_text = current_item.text(0)
        self.thread_remove_env = QThread_Remove_Env(tree_item_text)
        self.thread_remove_env.signal_textbrowser.connect(self.text_browser.append_text)
        self.thread_remove_env.signal_finished.connect(self.thread_finished)
        self.frame_pb.hide()
        self.thread_remove_env.start()
        self.tree_update()

    def update_env(self):
        current_item = self.tree_widget.currentItem()
        if not current_item:
            return
        confirm_dialog_result = QMessageBox.question(self, '确认更新', '更新时间比较长, 是否进行更新?',  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm_dialog_result == QMessageBox.No:
            return
        tree_item_text = current_item.text(0)
        self.thread_update_env = QThread_Update_Env(tree_item_text)
        self.thread_update_env.signal_textbrowser.connect(self.text_browser.append_text)
        self.thread_update_env.signal_finished.connect(self.thread_finished)
        self.frame_pb.hide()
        self.thread_update_env.start()
        self.tree_update()

    def thread_finished(self):
        self.frame_pb.show()
        self.tree_update()

    def set_style_sheet(self):
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
                    }

                    QListView{
                        font: 18px  '黑体';
                        padding: 5px;
                    }

                    QListWidget, QTreeWidget, QComboBox{
                        font: 18px  '黑体';
                        color: rgb(19, 24, 66);
                        border: 0px solid;
                        border-radius: 10px;
                        background-color: rgb(251, 246, 226);
                    }

                    QTreeWidget{
                        padding: 10px;
                    }

                    QComboBox{
                        max-height: 40px;
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
