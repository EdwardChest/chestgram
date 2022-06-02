# -*- coding: utf-8 -*-
from telethon import TelegramClient
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import FormattedText
from libs.commands import CommandsHandler
from libs.config import Config
from libs.errors import ErrorHandler
import json

print = print_formatted_text

class ChestGram:
    def __init__(self):
        __config = Config()
        self.app_id = __config.getVariable('app_id')
        self.api_hash = __config.getVariable('api_hash')
        self.client = TelegramClient('assets/chestgram', self.app_id, self.api_hash)
        self.initClient()

    def initClient(self):
        self.client.start()
        dialogs = {}
        for dialog in self.client.iter_dialogs():
            id = dialog.entity.id
            name = dialog.name
            dialogs[name] = id
        with open('assets/dialogs.json', 'w', encoding="utf-8") as dialog_file:
            json.dump(dialogs, dialog_file, ensure_ascii=False, indent=1)
        return self.client

def main(client):
    errors = ErrorHandler()
    commandHandler = CommandsHandler(client)
    while True:
        with patch_stdout():
            result = prompt('>> ')
            try:
                commandHandler.proccess(result)
            except Exception as error:
                errors.proccessError(result, error)

if __name__ == '__main__':
    print_formatted_text(
    FormattedText([
    ('ansiblue',
    """
        
    ▄████▄   ██░ ██ ▓█████   ██████ ▄▄▄█████▓  ▄████  ██▀███   ▄▄▄       ███▄ ▄███▓
    ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒ ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▓██▒▀█▀ ██▒
    ▒▓█    ▄ ▒██▀▀██░▒███   ░ ▓██▄   ▒ ▓██░ ▒░▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄  ▓██    ▓██░
    ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄   ▒   ██▒░ ▓██▓ ░ ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██ ▒██    ▒██ 
    ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒██████▒▒  ▒██▒ ░ ░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒▒██▒   ░██▒
    ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░    ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ░  ░
    ░  ▒    ▒ ░▒░ ░ ░ ░  ░░ ░▒  ░ ░    ░      ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░░  ░      ░
    ░         ░  ░░ ░   ░   ░  ░  ░    ░      ░ ░   ░   ░░   ░   ░   ▒   ░      ░   
    ░ ░       ░  ░  ░   ░  ░      ░                 ░    ░           ░  ░       ░   
    ░                                                                               
    
    Website: https://edwardchest.pw/chestgram
    Author: Edward Chesterton
     """),
    ])
    )
    client = ChestGram().initClient()
    main(client)
    client.run_until_disconnected()
