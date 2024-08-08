import os
import json
import locale
from Const_language_chinese import *
from Const_language_english import *
# from PyQt5.QtWidgets import QMessageBox


class Widgets_Language():
    def __init__(self) -> None:
        self.__display_text: str = ''
        self.__tool_tip: str = ''

    @property
    def display_text(self) -> str:
        return self.__display_text

    @property
    def tool_tip(self) -> str:
        return self.__tool_tip

    def set_display_text(self, text: str) -> None:
        self.__display_text = str(text)

    def set_tool_tip(self, text: str) -> None:
        self.__tool_tip = str(text)


class Part_Language():
    def __init__(self) -> None:
        self.__display_text: str = ''

    @property
    def display_text(self) -> str:
        return self.__display_text

    def set_display_text(self, text: str) -> None:
        self.__display_text = str(text)


class Language_Manager():
    def __init__(self, exe_folder_path, language_package_name=None) -> None:
        self.__exe_folder_path = exe_folder_path
        self.__language_package_name = language_package_name
        if not language_package_name or language_package_name == 'default':
            self.__select_default_language_package()
        self.__expand_language_package_folder_path = os.path.join(self.__exe_folder_path, '.Languages')
        self.__language_example_package_name = 'english_example.lpkg'
        self.__check_load_file_int()
        self.__parameter_init()

    def open_language_package(self, pkg_name):
        if not pkg_name:
            return
        if '<build-in>' in pkg_name:
            self.__current_language_package = LANGUAGE_ENGLISH
            self.__set_object_text()
            return
        elif '<内置>' in pkg_name:
            self.__current_language_package = LANGUAGE_CHINESE
            self.__set_object_text()
            return
        elif not os.path.exists(os.path.join(self.__expand_language_package_folder_path, pkg_name+'.lpkg')):
            return
        else:
            package_path = os.path.join(self.__expand_language_package_folder_path, pkg_name+'.lpkg')
        try:
            self.__current_language_package = self.__open_file(package_path)
            self.__set_object_text()
        except:
            return

    def __open_file(self, file_path) -> dict:
        with open(file_path, 'r', encoding='utf-8') as file:
            content: dict = json.load(file)
        return content

    def __write_example_file(self) -> None:
        package_path = os.path.join(self.__expand_language_package_folder_path, self.__language_example_package_name)
        with open(package_path, 'w', encoding='utf-8') as file:
            json.dump(LANGUAGE_ENGLISH, file, indent=4, ensure_ascii=False)

    def __parameter_init(self) -> None:
        self.list_widges = []
        self.list_others = []
        self.__object_init()
        self.__update_object_list()
        self.__set_object_text()

    def __object_init(self) -> None:
        self.__widgets_object_init()
        self.__others_object_init()

    def __widgets_object_init(self) -> None:
        # widgets_dict: dict = self.__current_language_package['widgets']
        # for key in widgets_dict.keys():
        #     setattr(self, key, Widgets_Language())
        self.lb_title = Widgets_Language()
        self.lb_single_command = Widgets_Language()
        self.cb_use_path = Widgets_Language()
        self.cb_use_module = Widgets_Language()
        self.cb_installed_all_select = Widgets_Language()
        self.cb_package_all_select = Widgets_Language()
        self.pb_all_clear = Widgets_Language()
        self.pb_env = Widgets_Language()
        self.pb_env_add = Widgets_Language()
        self.pb_pip_upgrade = Widgets_Language()
        self.pb_env_manager = Widgets_Language()
        self.pb_single_command_launch = Widgets_Language()
        self.pb_all_expand = Widgets_Language()
        self.pb_dependency_tree_update = Widgets_Language()
        self.pb_all_collapse = Widgets_Language()
        self.pb_dependency_find = Widgets_Language()
        self.pb_installed_invert = Widgets_Language()
        self.pb_installed_update = Widgets_Language()
        self.pb_indtalled_find = Widgets_Language()
        self.pb_installed_stop = Widgets_Language()
        self.pb_installed_uninstall = Widgets_Language()
        self.pb_installed_upgrade = Widgets_Language()
        self.pb_open_file = Widgets_Language()
        self.pb_create_new_file = Widgets_Language()
        self.pb_edit_file = Widgets_Language()
        self.pb_package_invert = Widgets_Language()
        self.pb_package_update = Widgets_Language()
        self.pb_package_find = Widgets_Language()
        self.pb_package_stop = Widgets_Language()
        self.pb_package_install = Widgets_Language()
        self.pb_package_uninstall = Widgets_Language()

    def __others_object_init(self) -> None:
        # others_dict: dict = self.__current_language_package['others']
        # for key in others_dict.keys():
        #     setattr(self, key, Part_Language())
        self.win_title = ''
        self.module_name = ''
        self.current_version = ''
        self.required_version = ''
        self.config_file = ''
        self.open_config_title = ''
        self.create_config_title = ''
        self.information = ''
        self.edit_config_error = ''
        self.read_config_error = ''
        self.context_menu_tree_env_open = ''
        self.context_menu_tree_env_remove = ''
        self.context_menu_tree_dep_expand = ''
        self.context_menu_tree_dep_collapse = ''
        self.windowsapp_tooltip = ''
        self.display_tree_env_error = ''
        self.get_config_env_error = ''
        self.load_python_error = ''
        self.load_conda_error = ''
        self.virtual_env_not_found = ''
        self.please_select_module = ''
        self.please_select_install_env = ''
        self.dialog_add_env_title = ''
        self.browser = ''
        self.add = ''
        self.cancel = ''
        self.env_type = ''
        self.python_path = ''
        self.please_select_env_tpye = ''
        self.please_input_python_path = ''
        self.please_check_python_path = ''
        self.add_python_pathS = ''
        self.dialog_virtual_env_manager_title = ''
        self.new_env_name = ''
        self.create_env = ''
        self.export_env = ''
        self.update_env = ''
        self.remove_env = ''
        self.python_version = ''
        self.remove_confirm = ''
        self.env_remove_hint = ''
        self.update_confirm = ''
        self.env_update_hint = ''
        self.save_confirm = ''
        self.file_save_hint = ''
        self.operation_finished = ''
        self.pip_update = ''
        self.operation_error = ''
        self.dependency_tree = ''
        self.installed_package = ''
        self.package_batch_install = ''

    def __update_object_list(self) -> None:
        self.__update_list_widges()
        self.__update_list_others()

    def __update_list_others(self) -> None:
        self.list_others = [[key, value] for key, value in self.__dict__.items()
                            if isinstance(value, Part_Language)]

    def __update_list_widges(self) -> None:
        self.list_widges = [[key, value] for key, value in self.__dict__.items()
                            if isinstance(value, Widgets_Language)]

    def __set_object_text(self) -> None:
        self.__set_widget_object_text(self.__current_language_package)
        self.__set_others_object_text(self.__current_language_package)

    def __set_widget_object_text(self, lang_dict: dict) -> None:
        if 'widgets' not in lang_dict:
            return
        widgets_dict: dict = lang_dict['widgets']
        for key, value in widgets_dict.items():
            value: dict
            if not key or key == '':
                continue
            if hasattr(self, key):
                object: Widgets_Language = getattr(self, key)
            else:
                return
            if 'display_text' in value:
                object.set_display_text(value['display_text'])
            if 'tool_tip' in value:
                object.set_tool_tip(value['tool_tip'])

    def __set_others_object_text(self, lang_dict: dict) -> None:
        if 'others' not in lang_dict:
            return
        others_dict: dict = lang_dict['others']
        for key, value in others_dict.items():
            value: dict
            if not key or key == '':
                continue
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                return

    def __check_load_file_int(self) -> None:
        if not os.path.exists(self.__expand_language_package_folder_path):
            os.makedirs(self.__expand_language_package_folder_path)
            self.__write_example_file()
        else:
            if len(os.listdir(self.__expand_language_package_folder_path)) == 0:
                self.__write_example_file()
        if self.__language_package_name:
            self.__language_package_path = os.path.join(self.__expand_language_package_folder_path, self.__language_package_name+'.lpkg')
            if not os.path.exists(self.__language_package_path):
                self.__select_default_language_package()
            else:
                try:
                    self.__current_language_package = self.__open_file(self.__language_package_path)
                except:
                    self.__select_default_language_package()
                    # QMessageBox.information(None, '提示', '语言包读取错误, 请检查语言包。当前为默认语言包')
        else:
            self.__select_default_language_package()

    def __select_default_language_package(self) -> None:
        # lang: str = locale.getlocale()[0] # exe 中无法识别
        lang: str = locale.getdefaultlocale()[0]  # exe 中可以识别
        if lang is not None and ('chinese' in lang.lower() or lang.startswith('zh')):
            self.__current_language_package = LANGUAGE_CHINESE
            self.cbb_init_display = '简体中文<内置>'
        else:
            self.__current_language_package = LANGUAGE_ENGLISH
            self.cbb_init_display = 'English<build-in>'


# a = Language_Manager(os.path.dirname(__file__))
# print(a.lb_title.tool_tip)
# a.open_language_package('english')
# print(a.lb_title.display_text)
# a.open_language_package('english_example')
# print(a.lb_title.display_text)
# # print(a.win_title.display_text)
