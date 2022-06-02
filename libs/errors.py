from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
import os

print = print_formatted_text
path = os.getcwd()

class ErrorHandler:
    def __init__(self):
        self.errorMsgPrefix = '[Ошибка] '
        self.errorInfoPrefix = '[Информация] '
        self.errorExamplePrefix = '[Пример] '

    def proccessError(self, command, error):
        try:
            with open(os.path.join(path, 'log.txt'), 'a+', encoding="utf-8") as log:
                log.write(f'[{command}] {str(error)}\n')
            command = command.split(' ')[0]
            errorMsg = f' При вызове метода {command}'
            errorInfo = 'Неизвестная ошибка'
            errorExample = 'Отправьте лог ошибки на https://github.com/chestgram/issues'
            if command == 'msg':
                errorInfo = 'Не удалось отправить сообщение. Проверьте правильность набора команды или диалог'
                errorExample = 'msg #Адресат# Сообщение'
            elif command == 'last':
                errorInfo = 'Вы ещё не отправили не одного сообщения, получение прошлого адресата не удалось'
                errorExample = 'last Сообщение'
            elif command == 'mute':
                errorInfo = 'Возможно вы не правильно ввели команду, либо данного диалога нет'
                errorExample = 'mute #Адресат#'
            elif command == 'forward':
                errorInfo = 'Возможно вы не правильно ввели команду, либо данного диалога нет'
                errorExample = 'forward Адресат ID-сообщения'
            elif command == 'history':
                errorInfo = 'Диалог не найден или команда введена неверно'
                errorExample = 'history #Адресат# Кол-во'
            elif command == 'play':
                errorInfo = 'Голосовое сообщение не найдено'
                errorExample = 'play ID-cообщения'
            else:
                errorInfo = 'Команда не найдена'
                errorExample = 'Используйте help'
            print(FormattedText([
                ['ansired', self.errorMsgPrefix + errorMsg + '\n'],
                ['ansiyellow', self.errorInfoPrefix + errorInfo + '\n'],
                ['ansiblue', self.errorExamplePrefix + errorExample + '\n'],
                ['ansibrightblack', self.errorInfoPrefix + 'Внимание, если ошибка повторяется, отправьте текст файла log.txt на https://github.com/EdwardChest/chestgram/issues/new']
            ]))
        except Exception as error:
            with open(os.path.join(path, 'log.txt', encoding="utf-8"), 'a+') as log:
                log.write(f'[{command}] {str(error)}\n')
            print(FormattedText([
                ['ansired', self.errorMsgPrefix + 'Неизвестная ошибка'],
                ['ansiyellow', self.errorInfoPrefix + 'Отправьте текст файла log.txt на https://github.com/EdwardChest/chestgram/issues/new'],
            ]))
