
import os
import json
import copy

DEFAULT_SETTING = {
    'language': [str, 'default']
}


class Setting_Manager():
    def __init__(self, exe_folder_path) -> None:
        self.__exe_folder_path: str = exe_folder_path
        self.__setting_path = os.path.join(self.__exe_folder_path, '.setting')
        self.__setting_data: dict = self.__check_file()

    @property
    def setting_data(self):
        return self.__setting_data

    def open_file_to_json(self, file_path):
        if not os.path.exists(file_path):
            return
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data

    def write_file_to_json(self, content: dict, file_path: str = None):
        if not file_path:
            file_path = self.__setting_path
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(content, file, indent=4, ensure_ascii=False)

    def __check_file(self):
        # 检查是否存在 setting 文件
        if not os.path.exists(self.__setting_path):
            # 不存在文件, 则创建 setting
            temp = self.__rebuild_setting()
        else:
            # 存在文件, 则检查 json 格式, 冗余, 丢失, 类型
            # 检查 json 格式
            temp = self.__check_json(self.__setting_path)
            # 检查 冗余
            temp = self.__check_redundancy(temp)
            # 检查 丢失
            temp = self.__check_lost(temp)
            # 检查 类型
            temp = self.__check_type(temp)
        return temp

    def __check_json(self, file_path: str):
        try:
            data_str = self.__open_file(file_path)
            temp = json.loads(data_str)
        except:
            temp = self.__rebuild_setting()
        return temp

    def __check_type(self, content: dict):
        temp = copy.deepcopy(content)
        flag_write = False

        def __scan(current_key, current_value, default_value):
            nonlocal temp
            nonlocal flag_write
            if isinstance(default_value, dict):
                if not isinstance(current_value, dict):
                    temp[current_key] = copy.deepcopy(default_value)
                    flag_write = True
                else:
                    for key, value in default_value.items():
                        if key in current_value:
                            __scan(key, current_value[key], value)
                        else:
                            current_value[key] = copy.deepcopy(value)
                            flag_write = True
            else:
                expected_type, default = default_value
                if not isinstance(current_value, expected_type):
                    temp[current_key] = default
                    flag_write = True
        __scan('', content, DEFAULT_SETTING)
        if flag_write:
            self.write_file_to_json(temp, self.__setting_path)
        return temp

    def __check_redundancy(self, content: dict):
        compare_dict = copy.deepcopy(content)
        temp = {}
        flag_write = False

        def __scan(parent: dict, default: dict):
            nonlocal flag_write
            keys_to_delete = []
            for key, compare_value in parent.items():
                if isinstance(compare_value, dict):
                    if key not in default:
                        keys_to_delete.append(key)
                        flag_write = True
                    else:
                        __scan(compare_value, default[key][1])
                else:
                    if key not in default:
                        keys_to_delete.append(key)
                        flag_write = True
            for key in keys_to_delete:
                del parent[key]
        __scan(compare_dict, DEFAULT_SETTING)
        if flag_write:
            self.write_file_to_json(compare_dict, self.__setting_path)
        return temp

    def __check_lost(self, content: dict):
        temp = {}
        flag_write = False

        def __scan(parent: dict, compare: dict, temp_dict: dict):
            nonlocal flag_write
            for key, default_value in parent.items():
                if isinstance(default_value[1], dict):
                    temp_dict[key] = {}
                    if key not in compare:
                        self.__scan_to_build(default_value[1], temp_dict[key])
                        flag_write = True
                    else:
                        temp_dict[key] = {}
                        __scan(default_value[1], compare[key], temp_dict[key])
                else:
                    if key not in compare:
                        temp_dict[key] = default_value[1]
                        flag_write = True
                    else:
                        temp_dict[key] = compare[key]

        __scan(DEFAULT_SETTING, content, temp)
        if flag_write:
            self.write_file_to_json(temp, self.__setting_path)
        return temp

    def __scan_to_build(self, parent: dict, temp_dict: dict):
        for key, value in parent.items():
            if isinstance(value[1], dict):
                temp_dict[key] = {}
                self.__scan_to_build(value[1], temp_dict[key])
            else:
                temp_dict[key] = value[1]
        return temp_dict

    def __rebuild_setting(self):
        temp = {}
        self.__scan_to_build(DEFAULT_SETTING, temp)
        self.write_file_to_json(temp, self.__setting_path)
        return temp

    def __open_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            temp = file.read()
        return temp
