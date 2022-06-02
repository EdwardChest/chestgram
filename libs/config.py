# -*- coding: utf-8 -*-
import os
import json
from os.path import exists, join

class Config:
    def __init__(self):
        self.path = join(os.getcwd(), 'assets')
        self.config = join(self.path, 'config.json')
        if not exists(self.path):
            os.mkdir(self.path)
        if not exists(self.config):
            with open(self.config, 'w', encoding="utf-8") as config_file:
                config = {}
                config['app_id'] = 123321
                config['api_hash'] = '123h123'
                config['mute'] = []
                config['user_color'] = 'ansibrightcyan'
                config['chat_color'] = 'ansiblue'
                config['only_contacts'] = False
                json.dump(config, config_file, indent=1)
                print('Конфигурационный файл config.json создан, заполните его и запустите снова')
                exit(0)

    def getVariable(self, key):
        with open(self.config, 'r', encoding="utf-8") as config_file:
            config = json.load(config_file)
            try:
                return config[key]
            except:
                print('Ошибка чтения из конфига')

    # {"TELEGRAM": {"app_id": "2257769", "api_hash": "3d3681d2010eb2015264fed4b4de8bb8"}, "SETTINGS": {"mute": ["609517172"], "only_contacts": false}}
    def setVariable(self, key, value):
        with open(self.config, 'r', encoding="utf-8") as config_file:
            config = json.load(config_file)
        with open(self.config, 'w', encoding="utf-8") as config_file:
            try:
                config[key] = value
                json.dump(config, config_file, indent=1)
            except:
                print('Ошибка записи в конфиг')
