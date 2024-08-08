

import os
import json


class Env_Config_Manager():
    def __init__(self, exe_folder_path) -> None:
        self.exe_folder_path = exe_folder_path
        self.config_path = os.path.join(self.exe_folder_path, '.config_env')

    def open_config(self):
        '''
        读取 Config 文件, 并返回读取数据 <json>

        返回值: 返回标记, 返回数据

        返回标记: 
            1: 成功读取
            0: 路径错误, 无文件
            -1: 读取错误, 文件格式不是 <json>

        '''
        if not os.path.exists(self.config_path):
            return 0, None
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                temp: dict = json.load(file)
            return 1, temp
        except:
            return -1, None

    def write_config(self, content: dict):
        with open(self.config_path, 'w', encoding='utf-8') as file:
            json.dump(content, file, indent=4, ensure_ascii=False)
