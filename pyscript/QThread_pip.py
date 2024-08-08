

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem

import os
import threading
import subprocess

from language_manager import *


class QThread_pip_update(QThread):
    signal_textbrowser = pyqtSignal(str)

    def __init__(self, parent, python_exe_path, pip_environment):
        super().__init__()
        self.language: Language_Manager = parent.language
        self.python_exe_path = python_exe_path
        if '(' in pip_environment:
            self.pip_environment: str = pip_environment
            self.python_version = None
        else:
            self.pip_environment = None
            self.python_version = pip_environment

    def read_output(self):
        while True:
            output_line = self.process.stdout.readline()
            if output_line == '' and self.process.poll() is not None:
                break
            if output_line:
                self.signal_textbrowser.emit(output_line.strip())
        if self.pip_environment:
            name = self.pip_environment
        else:
            name = self.python_version
        self.signal_textbrowser.emit(f'\n__________  {self.language.pip_update} {name} {self.language.operation_finished} __________\n\n')

    def run(self):
        if self.pip_environment:
            env = self.pip_environment.split(')')[0].split('(')[1]
            env_name = self.pip_environment.split(')')[1]
            if env == 'conda':
                env_activate_command = f'conda activate {env_name} &&'
        else:
            env_activate_command = ''
        command = [self.python_exe_path, '-m', 'pip', 'install', '--upgrade', 'pip']
        command_str = ' '.join(command)
        full_command = f'echo Y | {" ".join([env_activate_command, command_str])}'
        try:
            self.process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.threading_read = threading.Thread(target=self.read_output)
            self.threading_read.start()
        except subprocess.CalledProcessError as e:
            self.signal_textbrowser.emit(f'__________ pip {self.language.operation_error}: {e} __________\n')


class QThread_pip_install(QThread):
    signal_textbrowser = pyqtSignal(str)

    def __init__(self, parent, python_folder_path, python_version, install_flag, config_list):
        super().__init__()
        self.language: Language_Manager = parent.language
        self.python_folder_path = python_folder_path
        self.python_version = python_version
        self.install_flag = install_flag
        self.config_list = config_list

    def read_output(self, item):
        while True:
            output_line = self.process.stdout.readline()
            if output_line == '' and self.process.poll() is not None:
                break
            if output_line:
                self.signal_textbrowser.emit(output_line.strip())
        self.signal_textbrowser.emit(f'\n__________  {item}  {self.language.operation_finished} __________\n\n')

    def run(self):
        for item in self.config_list:
            if self.install_flag == 'install':
                full_command = f'echo Y | {os.path.join(self.python_folder_path, self.python_version, "python.exe")} -m pip install --upgrade {item}'
            else:
                full_command = f'echo Y | {os.path.join(self.python_folder_path, self.python_version, "python.exe")} -m pip uninstall {item}'
            try:
                self.process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self.thread = threading.Thread(target=self.read_output(item))
                self.thread.start()
            except subprocess.CalledProcessError as e:
                self.signal_textbrowser.emit(f'__________ {item} {self.language.operation_error}: {e} __________\n')


class QThread_Single_Command(QThread):
    signal_textbrowser = pyqtSignal(str)
    signal_finished = pyqtSignal()

    def __init__(self, parent, command, env_path_list=None):
        super().__init__()
        self.language: Language_Manager = parent.language
        self.ori_command = command
        self.command = command
        if env_path_list:
            self.command = env_path_list[1] + ' ' + self.command
            if 'conda' in env_path_list[0]:
                conda_env_name = env_path_list[0].split(')')[1]
                self.command = f'conda activate {conda_env_name} && ' + self.ori_command
        self.command = f'echo Y | {self.command}'

    def read_output(self):
        while True:
            output_line = self.process.stdout.readline()
            if output_line == '' and self.process.poll() is not None:
                break
            if output_line:
                self.signal_textbrowser.emit(output_line.strip())
                # print(repr(output_line))
        self.signal_textbrowser.emit(f'\n__________  {self.language.operation_finished} __________\n\n')
        self.signal_finished.emit()

    def run(self):
        try:
            # print(self.command)
            self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.thread_read = threading.Thread(target=self.read_output)
            self.thread_read.start()
        except subprocess.CalledProcessError as e:
            self.signal_textbrowser.emit(f'__________ {self.language.operation_error}: {e} __________\n')


class QThread_Pipdeptree(QThread):
    signal_deptree_line = pyqtSignal(str)
    signal_textbrowser = pyqtSignal(str)
    signal_finished = pyqtSignal()

    def __init__(self, parent, tree_item):
        super().__init__()
        self.language: Language_Manager = parent.language
        self.tree_item: QTreeWidgetItem = tree_item
        text_0 = self.tree_item.text(0)
        text_1 = self.tree_item.text(1)
        if text_0.startswith('(conda'):
            conda_name = text_0.split(')')[1]
            self.command = f'conda activate {conda_name} && pipdeptree'
        else:
            python_path = text_1
            self.command = f'{python_path} -m pipdeptree'

    def read_output(self):
        while True:
            output_line = self.process.stdout.readline()
            if output_line == '' and self.process.poll() is not None:
                break
            if output_line:
                self.signal_deptree_line.emit(output_line)
                # print(repr(output_line))
        self.signal_finished.emit()

    def run(self):
        try:
            self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.thread_read = threading.Thread(target=self.read_output)
            self.thread_read.start()
        except subprocess.CalledProcessError as e:
            self.signal_textbrowser.emit(f'__________ {self.language.operation_error}: {e} __________\n')
