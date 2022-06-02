# Chestgram
## CLI клиент Telegram
[![Website](https://edwardchest.pw/wp-content/uploads/2022/04/github_website.svg)](https://edwardchest.pw/chestgram)&emsp;[![Website](https://edwardchest.pw/wp-content/uploads/2022/04/github_release.svg)](https://github.com/EdwardChest/chestgram/releases)&emsp;[![Website](https://edwardchest.pw/wp-content/uploads/2022/04/github_docs.svg)](https://github.com/EdwardChest/chestgram/Wiki)

Chestgram разработан на Python 3.6+ за идею брал telegram-cli.
## Установка
Для работы команды **play**, необходимо установить ffmpeg
```sh
git clone https://github.com/EdwardChest/chestgram.git 
cd chestgram
pip3 install -R requirements.txt 
python3 chestgram.py
```
В одну команду
```sh
git clone https://github.com/EdwardChest/chestgram.git && cd chestgram && python3 -m pip install -r requirements.txt && python3 chestgram.py
```
Первым делом вам нужно получить API_ID и API_HASH.
Переходим на сайт [My Telegram](https://my.telegram.org/apps), авторизуемся и берем эти переменные.
Далее копируем эти данные в assets/config.json.
Запускаем и авторизуемся.
## Возможности

- Прослушивание аудио и видео файлов
- Включение тихого режима (только сообщения от пользователей)
- Отключение сообщений для определенного канала, пользователя
- История сообщений, вывод списка контактов
- Кастомизация цветов
- Удобная отправка сообщений
## Команды

| Команда | Аргументы | Описание |
| ------ | ------ | ------ |
| help | - | Выводит справочник команд |
| contacts | - | Выводит список контактов |
| msg | #Адресат# Сообщение | Отправляет сообщение в канал, чат |
| last | Сообщение | Отправляет сообщение последнему адресату |
| forward | #Адресат# ID-сообщения | Переслать сообщение в канал, чат |
| play | ID-сообщения | Прослушать аудио-видео сообщение|
| img | ID-сообщения | Открыть изображение через стандартный просмотр |
| history | #Адресат# Кол-во | Выводит историю диалога, макс. 50 сообщений |
| mute | #Адресат# | Отключает вывод сообщений для адресата |
| silent | - | Включает тихий режим, вывод только от пользователей |
| exit | - | Выход из клиента |

## Пример использования
Отправка сообщений по имени
```sh
msg #Lost Fire# Привет
```
По ID диалогу
```sh
msg #5108475664# Привет
```
Последнему получателю
```sh
last Как дела?
```

Переслать сообщение

```sh
forward #Lost Fire# 68493
```

Прослушать аудио-видео файл
```sh
play 68494
```

Просмотреть изображение
```sh
img 66677
```

История сообщений по диалогу
```
history #Lost Fire# 4
```

Отключить вывод конкретного чата
```sh
mute #Redmi 9T | RU Community | Русский чат#
```
