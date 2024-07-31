

from PyQt5.QtCore import QObject, QThread, pyqtSignal

import subprocess
import threading


class QThread_Create_New_Env(QThread):
    signal_textbrowser = pyqtSignal(str)
    signal_finished = pyqtSignal()

    def __init__(self, virtual_env, env_name, python_version) -> None:
        super().__init__()
        self.virtual_env: str = virtual_env
        self.env_name: str = env_name
        self.python_version: str = python_version

    def read_output(self):
        while True:
            output_line = self.process.stdout.readline()
            if output_line == '' and self.process.poll() is not None:
                break
            if output_line:
                self.signal_textbrowser.emit(output_line.strip())
        self.signal_textbrowser.emit(f"\n__________  新建虚拟环境完成 __________\n\n")
        self.signal_finished.emit()

    def run(self):
        command = ''
        if self.virtual_env == 'conda':
            command = f'conda create --name {self.env_name} python={self.python_version}'
        if command == '':
            return
        full_command = f'echo Y | {command}'
        try:
            self.process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.threading_read = threading.Thread(target=self.read_output)
            self.threading_read.start()
        except subprocess.CalledProcessError as e:
            self.signal_textbrowser.emit(f'__________ 操作失败: {e} __________\n')


class QThread_Remove_Env(QThread):
    signal_textbrowser = pyqtSignal(str)
    signal_finished = pyqtSignal()

    def __init__(self, tree_item_text: str) -> None:
        super().__init__()
        self.virtual_env: str = tree_item_text.split('(')[1].split(')')[0]
        self.env_name: str = tree_item_text.split(')')[1]

    def read_output(self):
        while True:
            output_line = self.process.stdout.readline()
            if output_line == '' and self.process.poll() is not None:
                break
            if output_line:
                self.signal_textbrowser.emit(output_line.strip())
        self.signal_textbrowser.emit(f"\n__________  删除虚拟环境完成 __________\n\n")
        self.signal_finished.emit()

    def run(self):
        command = ''
        if self.virtual_env == 'conda':
            command = f'conda env remove --name {self.env_name}'
        if command == '':
            return
        full_command = f'echo Y | {command}'
        try:
            self.process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.threading_read = threading.Thread(target=self.read_output)
            self.threading_read.start()
        except subprocess.CalledProcessError as e:
            self.signal_textbrowser.emit(f'__________ 操作失败: {e} __________\n')


class QThread_Update_Env(QThread):
    signal_textbrowser = pyqtSignal(str)
    signal_finished = pyqtSignal()

    def __init__(self, tree_item_text: str) -> None:
        super().__init__()
        self.virtual_env: str = tree_item_text.split('(')[1].split(')')[0]
        self.env_name: str = tree_item_text.split(')')[1]

    def read_output(self):
        while True:
            output_line = self.process.stdout.readline()
            if output_line == '' and self.process.poll() is not None:
                break
            if output_line:
                self.signal_textbrowser.emit(output_line.strip())
        self.signal_textbrowser.emit(f"\n__________  更新虚拟环境完成 __________\n\n")
        self.signal_finished.emit()

    def run(self):
        command = ''
        if self.virtual_env == 'conda':
            command = f'conda activate {self.env_name} && conda update --all'
        if command == '':
            return
        full_command = f'echo Y | {command}'
        try:
            self.process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.threading_read = threading.Thread(target=self.read_output)
            self.threading_read.start()
        except subprocess.CalledProcessError as e:
            self.signal_textbrowser.emit(f'__________ 操作失败: {e} __________\n')
