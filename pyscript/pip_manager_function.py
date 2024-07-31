
import shutil
from pip_manager_winUI_main import *
from QThread_Conda_Env import *

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot, QEventLoop
# from PyQt5.QtConcurrent import run, QFuture, QFutureWatcher


class Manager_Function(Manager_UI):
    def __init__(self):
        super().__init__()
        # self.treeWidget_env.setHeaderLabels(['键名 Key', '值 Value'])
        self.treeWidget_env.setColumnCount(2)
        self.treeWidget_env.setColumnWidth(0, 200)
        self.load_pip_env()

    def parameter_init(self):
        super().parameter_init()
        self.ignore_changes = False

    def signal_connections(self):
        super().signal_connections()
        self.treeWidget_env.itemSelectionChanged.connect(self.change_combobox_from_tree_widget)
        self.cbb_install_env.currentIndexChanged.connect(self.change_tree_widget_from_combobox)

    def load_pip_env(self):
        '''
        加载 pip 安装环境
        '''
        env_list = self.get_environment_list()
        for env_name, env_list in env_list.items():
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
        python_path_dict = self.get_python_path_dict()
        conda_env_dict = self.get_conda_environment_dict()
        for env_dict_list in [python_path_dict, conda_env_dict]:
            if env_dict_list:
                python_env_dict = {**python_env_dict, **env_dict_list}
        return python_env_dict

    def get_python_path_dict(self) -> list:
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
                        result = subprocess.run(
                            [python_exe_path, '--version'],
                            capture_output=True,
                            text=True,
                            check=True
                        )
                        python_path_list.append([result.stdout.split('\n')[0], python_exe_path])
            return {'python': python_path_list}
        except Exception as e:
            e = traceback.format_exc()
            print(e)
            QMessageBox.information(None, '提示', '无法自动加载Python安装路径，请检查python是否被添加到环境变量(用户)中')

    def get_conda_environment_dict(self):
        '''
        获取 Conda 中的虚拟环境
        '''
        conda_env_list = []

        @pyqtSlot(list)
        def set_conda_env_list(conda_env):
            nonlocal conda_env_list
            if conda_env:
                conda_env_list[:] = conda_env
                loop.quit()
        if shutil.which("conda"):
            get_conda_env_thread = Conda_Get_Env_List_QThread(self)
            get_conda_env_thread.signal_conda_env_list.connect(set_conda_env_list)
            get_conda_env_thread.start()
            loop = QEventLoop()
            loop.exec_()
            return {'conda': conda_env_list}
        else:
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Manager_Function()
    exe.show()
    sys.exit(app.exec_())
