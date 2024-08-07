
import os
import sys
import time

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextDocument, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QMessageBox, QListWidgetItem, QFileDialog, QCheckBox, QLabel, QListWidget, QTreeWidget, QTreeWidgetItem, QMenu, QAction, QLineEdit, qApp

from pip_manager_win_main_ui import *
from pipInstall_file_Editor import *
from ConsoleTextBrowser import *
from QThread_Environment_Variant import *
from svg_data import *

# APP_PATH = os.getcwd()
APP_PATH = os.path.dirname(__file__)

RESTART_EXIT_CODE = 88888888


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
        self.flag_trackback = True
        self.dependency_version_width = 130
        self.flag_init = True

    def signal_connections(self):
        '''
        信号连接初始化
        '''
        self.pb_all_clear.clicked.connect(self.all_clear)
        self.pb_env.clicked.connect(self.open_enviroment_variant)
        self.pb_open_file.clicked.connect(self.open_config)
        self.pb_create_new_file.clicked.connect(self.create_config)
        self.pb_edit_file.clicked.connect(self.edit_config)
        self.pb_package_invert.clicked.connect(self.inverse_select)
        self.pb_package_update.clicked.connect(self.refresh_list)
        self.pb_all_collapse.clicked.connect(self.tree_widget_all_collapse)
        self.pb_all_expand.clicked.connect(self.tree_widget_all_expand)
        self.pb_dependency_find.clicked.connect(self.find_in_treewidget_dependency)
        # self.pb_restart.clicked.connect(self.restart)

        self.cb_package_all_select.stateChanged.connect(self.ckb_all_select)
        self.cb_package_all_select.clicked.connect(self.ckb_clicked)

        self.le_package_path.textChanged.connect(self.can_pb_edit_enable)
        self.le_dependency_find.returnPressed.connect(self.find_in_treewidget_dependency)
        self.le_dependency_find.textChanged.connect(lambda: self.clear_find_result_in_treewidget(self.treeWidget_dependency))
        self.le_installed_find.returnPressed.connect(self.find_in_listwidget_installed)
        self.le_installed_find.textChanged.connect(lambda: self.clear_find_result_in_listwidget(self.le_installed_find, self.listWidget_installed))
        self.le_package_find.returnPressed.connect(self.find_in_listwidget_package)
        self.le_package_find.textChanged.connect(lambda: self.clear_find_result_in_listwidget(self.le_package_find, self.listWidget_package))

        self.treeWidget_env.customContextMenuRequested.connect(self.context_menu_treewidget_env_init)
        self.treeWidget_dependency.customContextMenuRequested.connect(self.context_menu_treewidget_dependency_init)
        # self.treeWidget_env.customContextMenuRequested.connect(self.open_config)

    def ui_init(self):
        '''
        界面初始化
        '''
        self.setMinimumSize(800, 600)
        self.textbrowser_init()
        self.combo_init()
        self.pb_edit_file.hide()
        self.pb_restart.hide()
        self.cb_use_module.setEnabled(False)
        self.cb_use_module.hide()
        self.frame_cb_command.hide()
        self.le_dependency_find.setClearButtonEnabled(True)
        self.le_installed_find.setClearButtonEnabled(True)
        self.le_package_find.setClearButtonEnabled(True)
        self.le_package_path.setClearButtonEnabled(True)
        self.le_single_command.setClearButtonEnabled(True)
        self.treeWidget_env.setColumnCount(2)
        self.treeWidget_env.setColumnWidth(0, 200)
        self.treeWidget_env.header().setVisible(False)
        self.treeWidget_env.setSelectionMode(QTreeWidget.SingleSelection)
        self.treeWidget_env.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget_dependency.header().setVisible(True)
        self.treeWidget_dependency.setColumnCount(3)
        self.treeWidget_dependency.setColumnWidth(0, 350)
        self.treeWidget_dependency.setColumnWidth(1, self.dependency_version_width)
        self.treeWidget_dependency.setColumnWidth(2, self.dependency_version_width)
        self.treeWidget_dependency.setHeaderLabels(['包名', '当前版本', '要求版本'])
        self.treeWidget_dependency.setContextMenuPolicy(Qt.CustomContextMenu)

    def textbrowser_init(self):
        '''
        TextBrowser 初始化
        '''
        layout = QHBoxLayout(self.frame_textbrowser)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.textbrowser = Console_TextBrowser(default_font_family='黑体', default_font_size=16)
        layout.addWidget(self.textbrowser)

    def combo_init(self):
        '''
        Combobox 初始化
        '''
        self.cbb_install_env.setPlaceholderText(' ')

    def resizeEvent(self, event):
        self.resize_tree_widget_dependency()
        super().resizeEvent(event)

    def resize_tree_widget_dependency(self):
        dependency_width = self.treeWidget_dependency.width() - 2*self.dependency_version_width
        if self.flag_init:  # 判断如果是第一次改变大小，即初始化，则忽略重置大小
            self.flag_init = False
            return
        if dependency_width < self.dependency_version_width:
            dependency_width = self.dependency_version_width
        self.treeWidget_dependency.setColumnWidth(0, dependency_width)

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
            self.list_widget_show(self.listWidget_package, self.get_config_content())

    def create_config(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, '新建 pipInstall 文件', APP_PATH, 'pipInstall Files (*.pipInstall)', options=options)
        print(file_path)
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                text = '''# 注释符为'#', 无行间释符, 只有行内注释符\n# 例如: numpy   # numpy 是一个科学计算的第三方包\n'''
                file.write(text)
            self.le_package_path.setText(file_path)
            # self.open_config()

    def edit_config(self):
        '''
        用记事本打开Config文件
        '''
        if os.path.exists(self.le_package_path.text()):
            self.pipInstall_editor = pipInstall_Editor(self, self.le_package_path.text())
            self.pipInstall_editor.exec_()
            self.list_widget_show(self.listWidget_package, self.get_config_content())
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
            # print(self.config)
            return self.config
        except:
            QMessageBox.information(None, '提示', '请重新核对配置文件的路径, 当前路径无效')

    def list_widget_show(self, list_widget: QListWidget, config_content):
        '''
        List-Widget 列表元素显示
        '''
        list_widget.clear()
        check_box_list = []
        if config_content:
            for i in config_content:
                i: str
                item = QListWidgetItem()
                widget = QWidget()
                label = QLabel(i.split('#')[0].strip())
                label.setWordWrap(True)
                label.setStyleSheet('color: rgb(19, 24, 66);')
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                height = self.get_adjust_label_height(label)
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
                    label_complement.setStyleSheet('color: rgb(19, 24, 66);')
                    label_complement.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    height = max(height, self.get_adjust_label_height(label_complement))
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

    def get_adjust_label_height(self, label_widget: QLabel):
        text_document = QTextDocument()
        text_document.setDefaultFont(label_widget.font())
        text_document.setTextWidth(label_widget.sizeHint().width())
        text_document.setPlainText(label_widget.text())
        label_widget_height = text_document.size().height()
        return label_widget_height

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
        print(sender)
        if sender == self.pb_package_update:
            self.list_widget_show(self.listWidget_package, self.get_config_content())
            self.cb_package_all_select.setChecked(False)
        elif sender == self.pb_installed_update:
            self.list_widget_show(self.listWidget_installed)
            self.cb_installed_all_select.setChecked(False)

    def tree_widget_all_expand(self):
        '''
        tree_widget 全部展开
        '''
        sender = self.sender()
        if sender == self.pb_all_expand:
            if self.treeWidget_dependency.topLevelItemCount() > 0:
                self.treeWidget_dependency.expandAll()

    def tree_widget_all_collapse(self):
        '''
        tree_widget 全部折叠
        '''
        sender = self.sender()
        if sender == self.pb_all_collapse:
            if self.treeWidget_dependency.topLevelItemCount() > 0:
                self.treeWidget_dependency.collapseAll()

    def all_clear(self):
        '''
        清空所有显示
        '''
        self.textbrowser.clear()
        self.le_package_path.clear()
        self.le_single_command.clear()
        self.le_dependency_find.clear()
        self.le_installed_find.clear()
        self.le_package_find.clear()
        self.cb_package_all_select.setChecked(False)
        self.treeWidget_env.clearSelection()
        self.cbb_install_env.setCurrentIndex(-1)
        self.treeWidget_dependency.clear()
        self.listWidget_package.clear()
        self.frame_cb_command.hide()

    def open_enviroment_variant(self):
        '''
        打开系统环境变量
        '''
        env_var = QThread_Environment_Variant()
        env_var.start()
        time.sleep(0.1)
        env_var.quit()

    def icon_setup(self, icon_code: str):
        '''
        设置图标

        参数:
            Icon_code: SVG 的源码(str)
        '''
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(icon_code.encode()))
        return QIcon(pixmap)

    def context_menu_treewidget_env_init(self, pos):
        def open_env_folder(item):
            if not item or not os.path.exists(item.text(1)):
                return
            subprocess.Popen(['explorer', '/select,', item.text(1)], creationflags=subprocess.CREATE_NO_WINDOW)
        item = self.sender().itemAt(pos)
        menu_context = QMenu(self.treeWidget_env)
        action_open = QAction('打开文件所在位置', self)
        action_open.setIcon(self.icon_setup(OPEN_FOLDER_ICON))
        action_open.triggered.connect(lambda: open_env_folder(item))
        menu_context.addAction(action_open)
        menu_context.setStyleSheet('color: rgb(19, 24, 66)')
        menu_context.exec_(self.sender().mapToGlobal(pos))

    def context_menu_treewidget_dependency_init(self, pos):
        def expand_collapse_all(item: QTreeWidgetItem, status: bool):
            item.setExpanded(status)
            for index in range(item.childCount()):
                expand_collapse_all(item.child(index), status)
        item: QTreeWidgetItem = self.sender().itemAt(pos)
        key_menu = QMenu(self.treeWidget_dependency)
        action_expand = QAction('展开当前', self)
        action_expand.setIcon(self.icon_setup(EXPAND_ICON))
        action_expand.triggered.connect(lambda: expand_collapse_all(item, True))
        key_menu.addAction(action_expand)
        action_collapse = QAction('折叠当前', self)
        action_collapse.setIcon(self.icon_setup(COLLAPSE_ICON))
        action_collapse.triggered.connect(lambda: expand_collapse_all(item, False))
        key_menu.addAction(action_collapse)
        key_menu.setStyleSheet('color: rgb(19, 24, 66)')
        key_menu.exec_(self.sender().mapToGlobal(pos))

    def find_in_treewidget(self, treewidget: QTreeWidget, content: str):
        def highlight_item(item: QTreeWidgetItem):
            item.setBackground(0, QBrush(QColor('#B4E380')))  # Highlight the item with yellow background
            item.setSelected(True)

        def clear_highlighting(treewidget):
            for item in treewidget.findItems('', Qt.MatchContains | Qt.MatchRecursive):
                item: QTreeWidgetItem
                item.setBackground(0, QBrush(QColor('transparent')))
                item.setSelected(False)

        def search_items(item: QTreeWidgetItem, content):
            for index in range(item.childCount()):
                child = item.child(index)
                if content in child.text(0).lower():
                    highlight_item(child)
                search_items(child, content)
        clear_highlighting(treewidget)
        search_items(treewidget.invisibleRootItem(), content)

    def clear_find_result_in_treewidget(self, treewidget: QTreeWidget):
        if self.le_dependency_find.text() and self.le_dependency_find.text() != '':
            return
        for item in treewidget.findItems('', Qt.MatchContains | Qt.MatchRecursive):
            item: QTreeWidgetItem
            item.setBackground(0, QBrush(QColor('transparent')))
            item.setSelected(False)

    def find_in_treewidget_dependency(self):
        content = self.le_dependency_find.text().lower()
        if not content or content == '':
            return
        self.find_in_treewidget(self.treeWidget_dependency, content)

    def find_in_listwidget_installed(self):
        content = self.le_installed_find.text().lower()
        if not content or content == '':
            return
        count = self.listWidget_installed.count()
        for index in range(count):
            item = self.listWidget_installed.item(index)
            if content in item.text().lower():
                item.setBackground(QBrush(QColor('#B4E380')))
            else:
                item.setBackground(QBrush(QColor('transparent')))

    def find_in_listwidget_package(self):
        content = self.le_package_find.text().lower()
        if not content or content == '':
            return
        count = self.listWidget_package.count()
        for index in range(count):
            item = self.listWidget_package.item(index)
            widget = self.listWidget_package.itemWidget(item)
            label: QLabel = widget.findChild(QLabel)
            if content in label.text().lower():
                item.setBackground(QBrush(QColor('#B4E380')))
            else:
                item.setBackground(QBrush(QColor('transparent')))

    def clear_find_result_in_listwidget(self, line_edit: QLineEdit, listwidget: QListWidget):
        if line_edit.text() and line_edit.text() != '':
            return
        count = listwidget.count()
        for index in range(count):
            item = listwidget.item(index)
            item.setBackground(QBrush(QColor('transparent')))

    def get_selected_item_package_list(self) -> list:
        command_list = []
        count = self.listWidget_package.count()
        for index in range(count):
            item = self.listWidget_package.item(index)
            widget = self.listWidget_package.itemWidget(item)
            checkbox: QCheckBox = widget.findChild(QCheckBox)
            label: QLabel = widget.findChild(QLabel)
            if checkbox.isChecked():
                text = label.text()
                command_list.append(text)
        return command_list

    # def restart(self):
    #     self.hide()
    #     qApp.exit(RESTART_EXIT_CODE)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = Manager_UI()
    exe.show()
    sys.exit(app.exec_())
