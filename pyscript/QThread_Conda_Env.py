
from PyQt5.QtCore import QThread, pyqtSignal

import subprocess


class Conda_Get_Env_List_QThread(QThread):
    signal_conda_env_list = pyqtSignal(list)
    signal_finished = pyqtSignal()
    text_to_textBrowser_cmd = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent_class = parent
        self.conda_env_list = None

    def run(self):
        try:
            result = subprocess.Popen('conda env list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = result.stdout.read().strip()
            # print(output)
            lines = output.split('\n')
            # 获取环境列表 conda_env_list, 列表中的每一个元素中 [0]是环境名，[1]是环境地址
            conda_env_list: list = [line.split() for line in lines if not line.startswith('#')]
            # print(conda_env_list)
            self.signal_conda_env_list.emit(conda_env_list)
            self.signal_finished.emit()

        except subprocess.CalledProcessError as e:
            print(e)
            # self.text_to_textBrowser_cmd.emit(f'__________ {self.parent_class.json_general["error"]} __________\n{e}\n')
