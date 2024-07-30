
import os
import sys
import time
import math

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QMessageBox, QListWidgetItem, QFileDialog, QCheckBox, QLabel, QListWidget

from pip_manager_main_win_ui import *
from ConsoleTextBrowser import *
from Environment_Variant_QThread import *

# APP_PATH = os.getcwd()
APP_PATH = os.path.dirname(__file__)


class Manager_UI(Ui_MainWindow, QMainWindow):
    '''
    主窗口 GUI 界面类
    '''

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.parameter_init()
        self.signal_connections()
        self.ui_init()

    def parameter_init(self):
        '''
        参数初始化
        '''
        self.check_box_package_list = []
        self.check_box_installed_list = []
        self.config_list = []
        self.python_folder_path = ''

    def signal_connections(self):
        '''
        信号连接初始化
        '''
        self.pb_all_clear.clicked.connect(self.all_clear)
        self.pb_env.clicked.connect(self.open_enviroment_variant)
        self.pb_open_file.clicked.connect(self.open_config)
        self.pb_edit_file.clicked.connect(self.edit_config)
        self.pb_package_invert.clicked.connect(self.inverse_select)
        self.pb_package_update.clicked.connect(self.refresh_list)

        self.cb_package_all_select.stateChanged.connect(self.ckb_all_select)
        self.cb_package_all_select.clicked.connect(self.ckb_clicked)

        self.le_package_path.textChanged.connect(self.can_pb_edit_enable)

    def ui_init(self):
        '''
        界面初始化
        '''
        self.textbrowser_init()
        self.combo_init()
        self.pb_edit_file.hide()
        self.treeWidget_env.header().setVisible(False)
        self.treeWidget_dependency.header().setVisible(False)

    def textbrowser_init(self):
        '''
        TextBrowser 初始化
        '''
        layout = QHBoxLayout(self.frame_textbrowser)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.textbrowser = Console_TextBrowser()
        layout.addWidget(self.textbrowser)

    def combo_init(self):
        '''
        Combobox 初始化
        '''
        self.cbb_install_env.setPlaceholderText(' ')

    def add_item_of_checkbox_after_checking_repeat(self, content):
        '''
        检查 Checkbox 添加项是否有重复
        '''
        add_new_python_path_flag = 0
        if self.cbb_install_env.count() == 0:
            self.cbb_install_env.addItem(content)
        else:
            for i in range(self.cbb_install_env.count()):
                item = self.cbb_install_env.itemText(i)
                if item == content:
                    add_new_python_path_flag += 1
            if add_new_python_path_flag == 0:
                self.cbb_install_env.addItem(content)

    def can_pb_edit_enable(self):
        '''
        判断并更改是否可以使用 编辑文件 按钮功能
        '''
        if self.le_package_path.text().strip() != '':
            self.pb_edit_file.show()
        else:
            self.pb_edit_file.hide()

    def open_config(self):
        '''
        通过窗口打开 Config 文件
        '''
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, '请选择 Config_pip_conda_install 文件', APP_PATH, '配置文件(*.pipInstall)', options=options)
        if filename:
            self.le_package_path.setText(filename)
            self.list_widget_show(self.listWidget_package)

    def edit_config(self):
        '''
        用记事本打开Config文件
        '''
        if os.path.exists(self.le_package_path.text()):
            # os.system(str('"'+self.Win.LE_ConfigPath.text()+'"'))
            subprocess.Popen(str('"'+self.le_package_path.text()+'"'), shell=True)
        else:
            QMessageBox.information(None, '提示', '请重新核对配置文件的路径, 当前路径无效')

    def get_config_content(self):
        '''
        获取Config_pip_install.ini文件中的内容(含行内注释, 不含整行注释, 排除空行)
        '''
        self.config = []
        self.config_path = self.le_package_path.text()
        try:
            with open(self.config_path, encoding='UTF-8') as self.config_ini:
                for content in self.config_ini.readlines():
                    if not content.startswith('#') and not content.startswith('\n'):
                        self.config.append(content.strip())
            return self.config
        except:
            QMessageBox.information(None, '提示', '请重新核对配置文件的路径, 当前路径无效')

    def list_widget_show(self, list_widget: QListWidget):
        '''
        List-Widget 列表元素显示
        '''
        def get_adjust_label_height(label_widget):
            text_document = QTextDocument()
            text_document.setDefaultFont(label_widget.font())
            text_document.setTextWidth(label_widget.sizeHint().width())
            text_document.setPlainText(label_widget.text())
            label_widget = text_document.size().height()
            return label_widget
        list_widget.clear()
        check_box_list = []
        Config_Content = self.get_config_content()
        if Config_Content:
            for i in Config_Content:
                i: str
                item = QListWidgetItem()
                widget = QWidget()
                label = QLabel(i.split('#')[0].strip())
                label.setWordWrap(True)
                label.setStyleSheet("color: rgb(19, 24, 66);")
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                height = get_adjust_label_height(label)
                check_box = QCheckBox()
                check_box_list.append(check_box)
                layout = QHBoxLayout(widget)
                layout.addWidget(check_box, stretch=0)
                layout.addWidget(label, stretch=30)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(10)
                # 如果有注释的话
                if len(i.split('#')) > 1:
                    complement = '# ' + i.split('#')[1].strip()
                    label_complement = QLabel(complement)
                    label_complement.setWordWrap(True)
                    label_complement.setStyleSheet("color: rgb(19, 24, 66);")
                    label_complement.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    height = max(height, get_adjust_label_height(label_complement))
                    layout.addWidget(label_complement, stretch=100)
                # 调整label的高度
                item.setSizeHint(QSize(int(label.sizeHint().width()), int(height)))
                list_widget.addItem(item)
                list_widget.setItemWidget(item, widget)
                widget.mousePressEvent = lambda event, checkbox=check_box: self.cb_widget_connect(checkbox)
                check_box.stateChanged.connect(self.ckb_config_item_connect)
                if list_widget == self.listWidget_package:
                    self.check_box_package_list = check_box_list
                elif list_widget == self.listWidget_installed:
                    self.check_box_installed_list = check_box_list
        # for i in range(list_widget.count()):
        #     item: QListWidgetItem = list_widget.item(i)
        #     check_box_list.append(list_widget.itemWidget(item))

    def ckb_config_item_connect(self):
        '''
        信号连接, 功能：如果有一个勾选框未被选择, 则全选勾选框置为未选择
        '''
        all_checked = all(check_box.isChecked() for check_box in self.check_box_package_list)
        self.cb_package_all_select.setChecked(all_checked)

    def cb_widget_connect(self, checkbox: QCheckBox):
        checkbox.setChecked(not checkbox.checkState())

    def ckb_all_select(self):
        '''
        全选功能
        '''
        sender = self.sender()
        if sender == self.cb_package_all_select:
            if self.cb_package_all_select.isChecked():
                for i in self.check_box_package_list:
                    i: QCheckBox
                    i.setChecked(True)
        elif sender == self.cb_installed_all_select:
            if self.cb_installed_all_select.isChecked():
                for i in self.check_box_installed_list:
                    i: QCheckBox
                    i.setChecked(True)

    def ckb_clicked(self):
        '''
        取消全选功能
        '''
        sender = self.sender()
        if sender == self.cb_package_all_select:
            if not self.cb_package_all_select.isChecked():
                for i in self.check_box_package_list:
                    i: QCheckBox
                    i.setChecked(False)
        elif sender == self.cb_installed_all_select:
            if not self.cb_installed_all_select.isChecked():
                for i in self.check_box_installed_list:
                    i: QCheckBox
                    i.setChecked(False)

    def inverse_select(self):
        '''
        反选功能
        '''
        sender = self.sender()
        if sender == self.pb_package_invert:
            check_box_list = self.check_box_package_list
        elif sender == self.pb_installed_invert:
            check_box_list = self.check_box_installed_list
        else:
            return
        for i in check_box_list:
            i: QCheckBox
            if i.isChecked():
                i.setChecked(False)
            else:
                i.setChecked(True)

    def refresh_list(self):
        '''
        刷新List-Widget功能
        '''
        sender = self.sender()
        if sender == self.pb_pip_upgrade:
            self.list_widget_show(self.listWidget_package)
            self.cb_package_all_select.setChecked(False)
        elif sender == self.pb_installed_update:
            self.list_widget_show(self.listWidget_installed)
            self.cb_installed_all_select.setChecked(False)

    def get_python_path(self):
        '''
        获取系统中Python的默认安装路径
        '''
        try:
            self.python_folder_path = ''
            path_list = os.environ.get('PATH').split(os.pathsep)
            for python_path in path_list:
                if 'Python' in python_path:
                    self.python_folder_path = os.path.join(python_path.split('Python')[0], 'Python')
                    break
            self.python_folder_list = os.listdir(self.python_folder_path)
            for item in self.python_folder_list:
                self.add_item_of_checkbox_after_checking_repeat(item)
            return self.python_folder_list
        except:
            QMessageBox.information(None, '提示', '无法自动加载Python安装路径，请检查python是否被添加到环境变量中')

    def all_clear(self):
        '''
        清空所有显示
        '''
        self.textbrowser.clear()
        self.le_package_path.clear()
        self.le_single_command.clear()
        self.cbb_install_env.clear()
        self.listWidget_package.clear()
        self.cb_package_all_select.setChecked(False)

    def open_enviroment_variant(self):
        '''
        打开系统环境变量
        '''
        env_var = Environment_Variant_QThread()
        env_var.start()
        time.sleep(0.1)
        env_var.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Manager_UI()
    exe.show()
    sys.exit(app.exec_())
