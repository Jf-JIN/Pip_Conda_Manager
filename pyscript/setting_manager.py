
import os
import json
import copy

DEFAULT_SETTING = {
    'language': [str, 'english']
}


class Setting_Manager():
    def __init__(self, exe_path) -> None:
        self.exe_path = exe_path
        self.setting_path = os.path.join(self.exe_path, 'setting')
        self.setting_data = self.__check_file()
        print(self.setting_data)

    def __check_file(self):
        # 检查是否存在 setting 文件
        if not os.path.exists(self.setting_path):
            # 不存在文件, 则创建 setting
            temp = self.__rebuild_setting()
        else:
            # 存在文件, 则检查 json 格式, 冗余, 丢失, 类型
            # 检查 json 格式
            temp = self.__check_json(self.setting_path)
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
        for key, value in content.items():
            if type(value) != DEFAULT_SETTING[key][0]:
                temp[key] = DEFAULT_SETTING[key][1]
                flag_write = True
        if flag_write:
            self.write_file_to_json(self.setting_path, temp)
        return temp

    def __check_redundancy(self, content: dict):
        temp = copy.deepcopy(content)
        flag_write = False
        for key, value in content.items():
            if key not in DEFAULT_SETTING:
                del temp[key]
                flag_write = True
        if flag_write:
            self.write_file_to_json(self.setting_path, temp)
        return temp

    def __check_lost(self, content: dict):
        temp = {}
        flag_write = False
        for key, value in DEFAULT_SETTING.items():
            if key not in content:
                temp[key] = value[1]
                flag_write = True
            else:
                temp[key] = content[key]
        if flag_write:
            self.write_file_to_json(self.setting_path, temp)
        return temp

    def __rebuild_setting(self):
        temp = {}
        for key, value in DEFAULT_SETTING.items():
            temp[key] = value[1]
        self.write_file_to_json(self.setting_path, temp)
        return temp

    def __open_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            temp = file.read()
        return temp

    def open_file_to_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data

    def write_file_to_json(self, file_path, content: dict):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(content, file, indent=None, ensure_ascii=True)