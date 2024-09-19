

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem

import os
import pkg_resources
import datetime
import threading
import subprocess

# from Manager_language import *
from Manager_pip_record import *


class QThread_read_output(QThread):
    signal_original_str = pyqtSignal(str)
    signal_strip_str = pyqtSignal(str)
    signal_finished_display = pyqtSignal(str)
    signal_finished = pyqtSignal()

    def __init__(self, process: subprocess.Popen, finished_display=''):
        super().__init__()
        self.process: subprocess.Popen = process
        self.finished_display: str = finished_display

    def run(self):
        while True:
            output_line: str = self.process.stdout.readline()
            if output_line == '' and self.process.poll() is not None:
                break
            if output_line:
                self.signal_original_str.emit(output_line)
                self.signal_strip_str.emit(output_line.strip())
        if self.finished_display or self.finished_display != '':
            self.signal_finished_display.emit(f'\n__________ {self.finished_display} __________\n\n')
        self.signal_finished.emit()


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


class QThread_pip_install_list(QThread):
    signal_textbrowser = pyqtSignal(str)
    signal_progressbar_num = pyqtSignal(int)
    signal_finished = pyqtSignal()

    def __init__(self, parent, exe_folder_path: str, env_info: str, python_exe_path: str, flag_install: str, package_list: list) -> None:
        """
            参数：
            - parent: 父对象
            - exe_folder_path: 可执行文件夹路径, 用于放置记录文件
            - env_info: 环境信息, Treewidget第一列
            - python_exe_path: Python可执行文件路径, Treewidget第二列
            - flag_install: 安装标志, 'install' / 'uninstall'
            - package_list: 包列表

            返回值：
            无返回值
        """
        super().__init__()
        self.parent_obj = parent
        self.language: Language_Manager = parent.language
        self.exe_folder_path: str = exe_folder_path
        self.env_info: str = env_info
        self.python_exe_path: str = python_exe_path
        self.flag_install: str = flag_install
        self.package_list: list = package_list
        # self.manager_record: Manager_Pip_Record = Manager_Pip_Record(self, self.exe_folder_path)
        self.manager_record = self.parent_obj.manager_record
        self.record: dict = self.manager_record.record

    def update_record(self, signal_info):
        python_exe_path = signal_info[0]
        package_name = signal_info[1]
        version = signal_info[2]
        date_time = signal_info[3]
        if self.flag_install == 'install':
            if python_exe_path not in self.record:
                self.record[python_exe_path] = {
                    package_name: {
                        'version': version,
                        'date_time': date_time
                    }
                }
            else:
                if package_name not in self.record[python_exe_path]:
                    self.record[python_exe_path][package_name] = {
                        'version': version,
                        'date_time': date_time
                    }
                else:
                    self.record[python_exe_path][package_name]['version'] = version
                    self.record[python_exe_path][package_name]['date_time'] = date_time
        else:
            if python_exe_path in self.record:
                if package_name in self.record[python_exe_path]:
                    del self.record[python_exe_path][package_name]

        # print('self.record', self.record)
        self.manager_record.write(self.record)

        # print('self.record', self.record)
        self.manager_record.write(self.record)

    def signal_textbrowser_emit(self, signal_info) -> None:
        self.signal_textbrowser.emit(signal_info)

    def run(self) -> None:
        installed_num = 0
        for item in self.package_list:
            try:
                thread_single_pip_install = QThread_pip_install_single(parent=self, env_info=self.env_info, python_exe_path=self.python_exe_path, package_name=item, flag_install=self.flag_install)
                thread_single_pip_install.signal_textbrowser.connect(self.signal_textbrowser_emit)
                thread_single_pip_install.signal_package_info.connect(self.update_record)
                thread_single_pip_install.start()
                thread_single_pip_install.wait()
                installed_num += 1
                self.signal_progressbar_num.emit(installed_num)
            except subprocess.CalledProcessError as e:
                self.signal_textbrowser.emit(f'__________ {item} {self.language.operation_error}: {e} __________\n')
        self.manager_record.write(self.record)


class QThread_pip_install_single(QThread):
    signal_textbrowser = pyqtSignal(str)
    signal_package_info = pyqtSignal(tuple)
    signal_finished = pyqtSignal()

    def __init__(self, parent, env_info: str, python_exe_path: str, package_name: str, flag_install: str):
        super().__init__()
        self.language: Language_Manager = parent.language
        self.env_info: str = env_info
        self.python_exe_path = python_exe_path
        self.package_name = package_name.split(' --')[0]
        self.flag_install = flag_install

    def pip_version_handle(self, full_command: str):
        try:
            print(full_command)
            print(self.env_info)
            env_info_for_version = full_command.split('-m')[0].split('&&')[0]
            print(env_info_for_version)
            connect_sign = ''
            if not self.env_info.startswith('Python'):
                connect_sign = '&& python '
            version_cmd = f'{env_info_for_version}{connect_sign}-m pip show {self.package_name}'
            print(version_cmd)
            self.process = subprocess.Popen(version_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            output = self.process.stdout.read()
            output_list = output.splitlines()
            output_dict = {}
            # print(output_list)
            for item in output_list:
                # print(item.split(':'))
                output_dict[item.split(':')[0].strip()] = item.split(':')[1].strip()
            # print(output_dict)
            return output_dict
        except Exception as e:
            # print('pip_version_handle\t', e)
            return {'Name': self.package_name, 'Version': '', 'Summary': '', 'Home-page': '', 'Author': '', 'Author-email': '', 'License': '', 'Location': '', 'Requires': '', 'Required-by': ''}

    def run(self) -> None:
        identity = None
        virtual_env_name = None
        if self.env_info.startswith('Python'):
            identity: str = 'python'
        else:
            identity: str = self.env_info.split(')')[0].split('(')[1]
            virtual_env_name: str = self.env_info.split(')')[1]
        if identity == 'python':
            if self.flag_install == 'install':
                full_command = f'echo Y | {self.python_exe_path} -m pip install --upgrade {self.package_name}'
            else:
                full_command = f'echo Y | {self.python_exe_path} -m pip uninstall {self.package_name}'
        elif identity == 'conda':
            if self.flag_install == 'install':
                full_command = f'conda activate {virtual_env_name} && echo Y | pip install --upgrade {self.package_name}'
            else:
                full_command = f'conda activate {virtual_env_name} && echo Y | pip uninstall {self.package_name}'
        elif identity == 'venv':
            pip_path = self.python_exe_path.split('python.exe')[0] + '/pip.exe'
            if self.flag_install == 'install':
                full_command = f'echo Y | {pip_path} install --upgrade {self.package_name}'
            else:
                full_command = f'echo Y | {pip_path} uninstall {self.package_name}'
        try:
            self.process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            while True:
                output_line: str = self.process.stdout.readline()
                if output_line == '' and self.process.poll() is not None:
                    break
                if output_line:
                    self.signal_textbrowser.emit(output_line.strip())
            version = ''
            if self.flag_install == 'install':
                version = self.pip_version_handle(full_command)['Version']
                # version = pkg_resources.get_distribution("requests").version
            self.signal_package_info.emit((self.python_exe_path, self.package_name, version, str(datetime.datetime.now())))
            self.signal_textbrowser.emit(f'\n__________ {self.package_name} {self.language.operation_finished} __________\n\n')
            self.signal_finished.emit()
        except subprocess.CalledProcessError as e:
            self.signal_textbrowser.emit(f'__________ {self.package_name} {self.language.operation_error}: {e} __________\n')


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
