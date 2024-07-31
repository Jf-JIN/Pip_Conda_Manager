
import shutil

from pip_virtual_environment_manager import *
from pip_manager_splash_screen import *
from pip_manager_win_mainUI import *
from QThread_Conda_Env import *
from QThread_pip import *

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot, QEventLoop


class Manager_Function(Manager_UI):
    def __init__(self):
        super().__init__()
        self.splash = Manager_Splash_Screen()
        self.load_pip_env()
        self.splash.close_splash_screen(self)

    def parameter_init(self):
        super().parameter_init()
        self.ignore_changes = False

    def signal_connections(self):
        super().signal_connections()
        self.treeWidget_env.itemSelectionChanged.connect(self.change_combobox_from_tree_widget)
        self.cbb_install_env.currentIndexChanged.connect(self.change_tree_widget_from_combobox)
        self.pb_pip_upgrade.clicked.connect(self.upgrade_pip)
        self.pb_env_manager.clicked.connect(self.virtual_env_manager)

    def ui_init(self):
        super().ui_init()
        # self.treeWidget_env.setHeaderLabels(['键名 Key', '值 Value'])
        self.treeWidget_env.setColumnCount(2)
        self.treeWidget_env.setColumnWidth(0, 200)

    def load_pip_env(self):
        '''
        加载 pip 安装环境
        '''
        self.env_dict = self.get_environment_list()
        self.tree_env_display()

    def tree_env_display(self):
        self.treeWidget_env.clear()
        for env_name, env_list in self.env_dict.items():
            for env_item_list in env_list:
                item = QTreeWidgetItem(self.treeWidget_env)
                if env_name == 'python':
                    name = ''
                else:
                    name = f'({env_name})'
                item.setText(0, name + env_item_list[0])
                item.setText(1, env_item_list[1])
                voll_tip_text = f'{name} {env_item_list[0]}   {env_item_list[1]}'
                item.setToolTip(0, voll_tip_text)
                item.setToolTip(1, voll_tip_text)
                self.cbb_install_env.addItem(name + env_item_list[0])

    def tree_env_update(self):
        self.env_dict['conda'] = self.get_conda_environment_list()
        self.tree_env_display()

    def change_combobox_from_tree_widget(self):
        if self.ignore_changes:
            return

        tree_current_item = self.treeWidget_env.currentItem()
        if tree_current_item:
            self.ignore_changes = True
            self.cbb_install_env.setCurrentText(tree_current_item.text(0))
            self.ignore_changes = False

    def change_tree_widget_from_combobox(self):
        if self.ignore_changes:
            return
        cbb_current_text = self.cbb_install_env.currentText()
        if cbb_current_text:
            self.ignore_changes = True
            for i in range(self.treeWidget_env.topLevelItemCount()):
                item = self.treeWidget_env.topLevelItem(i)
                if item.text(0) == cbb_current_text:
                    item.setSelected(True)
                    self.treeWidget_env.setCurrentItem(item)
                    break
            self.ignore_changes = False

    def get_environment_list(self):
        python_env_dict = {}
        self.splash.show_message('加载 Python 解释器路径')
        python_path_list = self.get_python_path_list()
        self.splash.show_message('加载 Conda 环境')
        conda_env_list = self.get_conda_environment_list()
        python_env_dict['python'] = python_path_list
        python_env_dict['conda'] = conda_env_list
        self.splash.show_message('加载完成, 完成初始化, 进入程序')
        return python_env_dict

    def get_python_path_list(self) -> list:
        '''
        获取系统中Python的默认安装路径
        '''
        try:
            python_path_list = []
            path_env_list = os.environ.get('PATH').split(os.pathsep)
            for python_env_path in path_env_list:
                if 'python' in python_env_path.lower() and 'Script' in python_env_path:
                    python_root_folder_path = python_env_path.split('Script')[0]
                    python_exe_path = os.path.join(python_root_folder_path, 'python.exe')
                    if os.path.exists(python_exe_path) and python_exe_path not in python_path_list:
                        result = subprocess.Popen(
                            [python_exe_path, '--version'],
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        # result = subprocess.run(
                        #     [python_exe_path, '--version'],
                        #     capture_output=True,
                        #     text=True,
                        #     check=True
                        # )
                        python_path_list.append([result.stdout.read().split('\n')[0], python_exe_path])
            return python_path_list
        except Exception as e:
            e = traceback.format_exc()
            print(e)
            QMessageBox.information(None, '提示', '无法自动加载Python安装路径, 请检查python是否被添加到环境变量(用户)中')

    def get_conda_environment_list(self):
        '''
        获取 Conda 中的虚拟环境
        '''
        conda_env_list = []

        @pyqtSlot(list)
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

    def upgrade_pip(self):
        current_item = self.treeWidget_env.currentItem()
        if current_item:
            pip_env = current_item.text(0)
            python_exe_path = current_item.text(1)
            self.pip_upgrade_thread = QThread_pip_update(python_exe_path, pip_env)
            self.pip_upgrade_thread.signal_textbrowser.connect(self.textbrowser.append_text)
            self.pip_upgrade_thread.start()

    def virtual_env_manager(self):
        env_manager = Virtual_Environment_Manager(self, self.env_dict)
        env_manager.exec_()
        self.tree_env_update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Manager_Function()
    exe.show()
    sys.exit(app.exec_())
