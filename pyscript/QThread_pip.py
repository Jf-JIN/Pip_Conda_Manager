

from PyQt5.QtCore import QThread, pyqtSignal

import os
import threading
import subprocess


class QThread_pip_update(QThread):
    signal_textbrowser = pyqtSignal(str)

    def __init__(self, python_exe_path, pip_environment):
        super().__init__()
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
        self.signal_textbrowser.emit(f"\n__________  pip更新 {name} 已完成操作 __________\n\n")

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
            self.signal_textbrowser.emit(f'__________ pip 安装/更新/卸载 操作失败: {e} __________\n')


class QThread_pip_install(QThread):
    output_to_textbrowser = pyqtSignal(str)

    def __init__(self, python_folder_path, python_version, install_flag, config_list):
        super().__init__()
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
                self.output_to_textbrowser.emit(output_line.strip())
        self.output_to_textbrowser.emit(f"\n__________  {item}  已完成操作 __________\n\n")

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
                self.textBrowser.append(f"__________ {item} 操作失败: {e} __________\n")
