
import shutil

from pip_virtual_environment_manager import *
from pip_manager_splash_screen import *
from pip_manager_win_mainUI import *
from QThread_Conda_Env import *
from QThread_pip import *


from PyQt5.QtCore import pyqtSlot, QEventLoop


class Manager_Function(Manager_UI):
    def __init__(self):
        super().__init__()
        self.splash = Manager_Splash_Screen()
        self.load_pip_env()
        self.splash.close_splash_screen(self)
        # self.update_tree_dependency()

    def parameter_init(self):
        super().parameter_init()
        self.ignore_changes = False
        self.stack = [self.treeWidget_dependency.invisibleRootItem()]
        self.indent = ''
        self.indent_sign = 0
        # self.stop = False
        self.flag_has_virtual_env = False

    def signal_connections(self):
        super().signal_connections()
        self.treeWidget_env.itemSelectionChanged.connect(self.change_combobox_from_tree_widget)
        self.cbb_install_env.currentIndexChanged.connect(self.change_tree_widget_from_combobox)
        self.pb_pip_upgrade.clicked.connect(self.upgrade_pip)
        self.pb_env_manager.clicked.connect(self.virtual_env_manager)
        self.pb_single_command_launch.clicked.connect(self.launch_single_command)
        self.pb_package_install.clicked.connect(self.install_package_list)
        self.le_single_command.returnPressed.connect(self.launch_single_command)
        self.cb_use_path.clicked.connect(self.display_cb_use_module)

    def ui_init(self):
        super().ui_init()
        # self.treeWidget_env.setHeaderLabels(['键名 Key', '值 Value'])

    def load_pip_env(self):
        '''
        加载 pip 安装环境
        '''
        self.env_dict = self.get_environment_list()
        self.tree_env_display()

    def tree_env_display(self):
        '''
        显示环境树
        '''
        try:
            self.treeWidget_env.clear()
            for env_name, env_list in self.env_dict.items():
                if env_list:
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
                        if env_name == 'python' and env_item_list[0] == 'WindowsApps':
                            item.setIcon(0, self.icon_setup(WARNING_ICON))
                            voll_tip_text = f'无法对此 Python 进行操作\n{name} {env_item_list[0]}   {env_item_list[1]}'
                            item.setToolTip(0, voll_tip_text)
                            item.setToolTip(1, voll_tip_text)
        except Exception as e:
            if self.flag_trackback:
                e = traceback.format_exc()
            # print(e)
            current_splash_flags = self.splash.windowFlags()
            self.splash.setWindowFlags(current_splash_flags & ~Qt.WindowStaysOnTopHint)
            self.splash.show()
            QMessageBox.information(None, '提示', f'环境加载错误, 请检查 Python 环境<br>{e}')
            self.splash.setWindowFlags(current_splash_flags | Qt.WindowStaysOnTopHint)
            self.splash.show()
            # sys.exit()

    def tree_env_update(self):
        '''
        更新环境树
        '''
        self.env_dict['conda'] = self.get_conda_environment_list()
        self.tree_env_display()

    def change_combobox_from_tree_widget(self):
        '''
        通过 Combobox 更改 Treewidget
        '''
        if self.ignore_changes:
            return

        tree_current_item = self.treeWidget_env.currentItem()
        if tree_current_item:
            self.ignore_changes = True
            self.cbb_install_env.setCurrentText(tree_current_item.text(0))
            self.update_tree_dependency()
            self.ignore_changes = False
            self.frame_cb_command.show()
            self.display_cb_use_module()

    def change_tree_widget_from_combobox(self):
        '''
        通过 Treewidget 更改 Combobox
        '''
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
            self.update_tree_dependency()
            self.frame_cb_command.show()
            self.display_cb_use_module()

    def display_cb_use_module(self):
        if self.treeWidget_env.currentItem().text(0).startswith('Python') and self.cb_use_path.isChecked():
            self.cb_use_module.show()
            self.cb_use_module.setEnabled(True)
        else:
            self.cb_use_module.hide()
            self.cb_use_module.setEnabled(False)

    def get_environment_list(self):
        '''
        获取环境列表, 并在加载页面中显示信息
        '''
        python_env_dict = {}
        python_path_list = self.get_python_path_list()
        conda_env_list = self.get_conda_environment_list()
        python_env_dict['python'] = python_path_list
        python_env_dict['conda'] = conda_env_list
        self.splash.show_message('加载完成, 完成初始化, 进入程序')
        return python_env_dict

    def get_python_path_list(self) -> list:
        '''
        获取系统中Python的默认安装路径
        '''
        self.splash.show_message('加载 Python 解释器路径')
        try:
            python_version_path_list = []
            python_list_result = subprocess.Popen(
                'where python.exe',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            python_path_list: str = python_list_result.stdout.read().split('\n')
            for python_path in python_path_list:
                if 'WindowsApps' in python_path:
                    python_version_path_list.append(['WindowsApps', python_path])
                elif os.path.exists(python_path) and python_path not in python_version_path_list:
                    result = subprocess.Popen(
                        [python_path, '--version'],
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    python_version_path_list.append([result.stdout.read().split('\n')[0], python_path])
                # 老方法，使用环境变量
                # path_env_list = os.environ.get('PATH').split(os.pathsep)
                # if 'python' in python_env_path.lower() and 'Script' in python_env_path:
                #     python_root_folder_path = python_env_path.split('Script')[0]
                #     python_exe_path = os.path.join(python_root_folder_path, 'python.exe')
                #     if os.path.exists(python_exe_path) and python_exe_path not in python_version_path_list:
                #         result = subprocess.Popen(
                #             [python_exe_path, '--version'],
                #             shell=True,
                #             stdout=subprocess.PIPE,
                #             stderr=subprocess.STDOUT,
                #             text=True,
                #             creationflags=subprocess.CREATE_NO_WINDOW
                #         )
                #         python_version_path_list.append([result.stdout.read().split('\n')[0], python_exe_path])
            if len(python_version_path_list) == 0:
                assert ()
            return python_version_path_list
        except Exception as e:
            if self.flag_trackback:
                e = traceback.format_exc()
            current_splash_flags = self.splash.windowFlags()
            self.splash.setWindowFlags(current_splash_flags & ~Qt.WindowStaysOnTopHint)
            self.splash.show()
            QMessageBox.information(None, '提示', f'无法自动加载 Python 安装路径, 请检查 python 安装路径<br>{e}')
            self.splash.setWindowFlags(current_splash_flags | Qt.WindowStaysOnTopHint)
            self.splash.show()

    def get_conda_environment_list(self):
        '''
        获取 Conda 中的虚拟环境
        '''
        conda_env_list = []
        self.splash.show_message('加载 Conda 环境')

        @ pyqtSlot(list)
        def set_conda_env_list(conda_env):
            '''
            更新 Conda 环境列表
            '''
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
        try:
            if shutil.which("conda"):  # 检查是否安装了 Conda
                get_conda_env_thread = QThread_Conda_Get_Env_List(self)
                get_conda_env_thread.signal_conda_env_list.connect(set_conda_env_list)
                get_conda_env_thread.start()
                loop = QEventLoop()
                loop.exec_()
                self.flag_has_virtual_env = True
                return conda_env_list
            else:
                return None
        except Exception as e:
            if self.flag_trackback:
                e = traceback.format_exc()
            QMessageBox.information(None, '提示', f'读取 Conda 错误<br>{e}')

    def upgrade_pip(self):
        '''
        更新 pip
        '''
        current_item = self.treeWidget_env.currentItem()
        if current_item:
            pip_env = current_item.text(0)
            python_exe_path = current_item.text(1)
            if pip_env == 'WindowsApps':
                return
            self.pip_upgrade_thread = QThread_pip_update(python_exe_path, pip_env)
            self.pip_upgrade_thread.signal_textbrowser.connect(self.textbrowser.append_text)
            self.pip_upgrade_thread.start()

    def virtual_env_manager(self):
        '''
        打开虚拟环境管理界面
        '''
        if not self.flag_has_virtual_env:
            QMessageBox.information(None, '提示', '未检测到虚拟环境')
            return
        env_manager = Virtual_Environment_Manager(self, self.env_dict)
        env_manager.exec_()
        self.tree_env_update()

    def launch_single_command(self):
        '''
        运行单行命令
        '''
        command = self.le_single_command.text().strip()
        env_path_list = None
        if not command or command == '':
            return
        if self.cb_use_module.isChecked() and self.cb_use_module.isEnabled() and self.cb_use_path.isChecked():
            command = '-m ' + command
        if self.cb_use_path.isChecked() and self.treeWidget_env.currentItem():
            env_path_list = [self.treeWidget_env.currentItem().text(0), self.treeWidget_env.currentItem().text(1)]
        self.thread_command = QThread_Single_Command(command, env_path_list)
        self.thread_command.signal_textbrowser.connect(self.textbrowser.append_text)
        self.thread_command.start()

    def build_dependency_tree_on_tree_widget(self, line: str):
        '''
        建立依赖树
        '''
        # if self.stop:   # 用于调试
        #     return
        try:
            def get_indent_info(single_line_string: str, indent_sign: int):
                '''
                获取缩进信息
                '''
                tab = self.indent
                tab_num = self.indent_sign
                if single_line_string.startswith(' ') and indent_sign == 0:
                    num = 0
                    for k in single_line_string:
                        if k != ' ':
                            tab_num = num
                            tab = single_line_string[0:num]
                            break
                        num += 1
                return tab, tab_num

            def get_name_version(line: str):
                '''
                获取依赖树中的 包名, 当前版本号, 要求版本号
                '''
                name = None
                version_current = None
                version_required = None
                try:
                    if not line.startswith(' '):
                        name: str = line.split('==')[0].strip()
                        version_current: str = line.split('==')[1].strip()
                    elif '[required:' in line:
                        name = line.split('[required:')[0].split('- ')[1].strip()
                        version_current = line.split('installed:')[1].split(']')[0].strip().split('\n')[0]
                        version_required = line.split(',')[0].split('[required:')[1].strip()
                except Exception as e:
                    if self.flag_trackback:
                        e = traceback.format_exc()
                        # print(e)
                    self.textbrowser.append_text(line)
                finally:
                    return name, version_current, version_required

            # 添加单个元素到树中
            self.indent, self.indent_sign = get_indent_info(line, self.indent_sign)
            if self.indent_sign == 0:
                indent_level = 0
            else:
                indent_level = line.count(self.indent)  # 计算缩进级别

            name, version_current, version_required = get_name_version(line)
            # if name is None:
            #     self.stop = True    # 用于调试
            #     return
            if name is None or version_current is None:
                return

            # 删除当前级别之后的所有项
            if indent_level > 0:
                while len(self.stack) > indent_level + 1:
                    self.stack.pop()
                item = QTreeWidgetItem(self.stack[-1])
            else:
                self.stack = [self.treeWidget_dependency.invisibleRootItem()]
                item = QTreeWidgetItem(self.treeWidget_dependency)
            item.setText(0, name)
            item.setText(1, version_current)
            item.setText(2, version_required)
            self.stack[-1].addChild(item)
            self.stack.append(item)

            self.treeWidget_dependency.expandAll()
        except Exception as e:
            if self.flag_trackback:
                e = traceback.format_exc()
                print(e)
            # self.textbrowser.append_text(e)
            self.textbrowser.append_text(f'{self.treeWidget_env.currentItem().text(0)}: 未安装pipdeptree')

    def update_tree_dependency(self):
        '''
        获取并更新依赖树
        '''
        self.treeWidget_dependency.clear()
        tree_widget_env_item = self.treeWidget_env.currentItem()
        self.thread_dependency = QThread_Pipdeptree(tree_widget_env_item)
        self.thread_dependency.signal_deptree_line.connect(self.build_dependency_tree_on_tree_widget)
        self.thread_dependency.signal_textbrowser.connect(self.textbrowser.append_text)
        self.thread_dependency.start()

    def install_package_list(self):
        selected_item = self.get_selected_item_package_list()
        env_name = self.cbb_install_env.currentText()
        if len(selected_item) < 1:
            QMessageBox.information(None, '提示', '请选择安装模块/包')
            return
        elif not env_name or env_name == '':
            QMessageBox.information(None, '提示', '请选择安装环境')
            return
        elif env_name == 'WindowsApps':
            return
        env_path = self.treeWidget_env.currentItem().text(1)
        print(env_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Manager_Function()
    exe.show()
    sys.exit(app.exec_())
