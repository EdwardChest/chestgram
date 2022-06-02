# -*- coding: utf-8 -*-
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from .config import Config
from telethon import functions, utils, events, types
import re, json, os, sys, subprocess

print = print_formatted_text

class CommandsHandler:
    def __init__(self, client):
        self.__config = Config()
        self.last_peer = ''
        self.client = client
        self.app_id = int(self.__config.getVariable('app_id'))
        self.client.add_event_handler(self.handleMessage)

    # Open file image
    def openImage(self, path):
        imageViewerFromCommandLine = {'linux':'xdg-open',
            'win32':'explorer',
            'darwin':'open'}[sys.platform]
        subprocess.Popen([imageViewerFromCommandLine, path])

    # Type of message for print correctly
    def message_object(self, msg):
        if msg.media:
            if msg.sticker:
                attrs = msg.sticker.attributes[1]
                msg.text = 'Стикер: ' + attrs.alt if attrs.alt != '' else 'Стикер'
            elif msg.gif:
                msg.text = 'GIF'
            elif msg.video_note:
                msg.text = f'Видеосообщение'
            elif msg.video:
                msg.text = f'Видео'
            elif msg.photo:
                msg.text = f'Фото'
            elif msg.voice:
                msg.text = f'Голосовое сообщение'
            elif msg.poll:
                msg.text = 'Опрос'
            elif msg.file:
                msg.text = f'Файл'
            return msg.text
        else:
            return msg.text

    # New messages handler
    @events.register(events.NewMessage)
    async def handleMessage(self, event):
        chat_from = event.chat if event.chat else (await event.get_chat())
        chat_title = utils.get_display_name(chat_from)
        sender = await event.get_sender()
        name = utils.get_display_name(sender)
        msg = self.message_object(event.message)
        silent = self.__config.getVariable('only_contacts')
        output = FormattedText([
            ('ansibrightblack', f'[{event.message.id}] '),
            ('ansiblue', f'#{chat_title}# ' if chat_title != name else ''),
            ('ansibrightcyan', f'[{name}] » '),
            ('ansiwhite', msg),
        ])
        if silent and type(chat_from).__name__ == 'User':
            print(output)
        elif not silent:
            if str(chat_from.id) not in self.__config.getVariable('mute'):
                print(output)

    # Send message to peer
    async def send_message(self, peer_id, msg, reply=False):
        self.last_peer = peer_id
        if reply:
            await self.client.send_message(peer_id, msg, reply_to=int(reply))
        else:
            await self.client.send_message(peer_id, msg)

    # Get list of chats
    async def get_chats(self):
        async for dialog in self.client.iter_dialogs():
            if (isinstance(dialog.entity, types.Chat) or isinstance(dialog.entity, types.Channel)):
                print(FormattedText([
                    (self.__config.getVariable('user_color'), f'{dialog.name} '),
                    (self.__config.getVariable('chat_color'), f'» {dialog.entity.id}'),
                ]))

    # Get list of contacts
    async def get_contacts(self):
        result = await self.client(functions.contacts.GetContactsRequest(hash=self.app_id))
        for contact in result.users:
            last_name =  contact.last_name if contact.last_name != None else ""
            id = contact.id
            print(FormattedText([
                (self.__config.getVariable('user_color'), f'{contact.first_name} {last_name} '),
                (self.__config.getVariable('chat_color'), f'» {id}'),
            ]))

    # Play audio message
    async def playAudio(self, msg_id):
        filename = ''
        msg = await self.client(functions.messages.GetMessagesRequest(id=[int(msg_id)]))
        msg = msg.messages[0]
        if msg.voice:
            filename = 'voice.oga'
        elif msg.video:
            filename = 'video.mp4'
        path = os.path.join(os.getcwd(), 'assets', filename)
        await self.client.download_media(message=msg, file=path)
        print(FormattedText([
            ('ansired', '[CTRL + C] '),
            ('ansiyellow', 'Чтобы остановить прослушивание'),
        ]))
        os.system(f'ffplay -nodisp -autoexit -hide_banner -loglevel error {path}')

    # Save and view image
    async def show_image(self, msg_id):
        msg = await self.client(functions.messages.GetMessagesRequest(id=[int(msg_id)]))
        msg = msg.messages[0]
        if msg.photo:
            path = os.path.join(os.getcwd(), 'assets', 'img.png')
            await self.client.download_media(message=msg, file=path)
            self.openImage(path)
        else:
            print(FormattedText([
                ('ansired', '[Ошибка] '),
                ('ansiyellow', 'Изображение не найдено'),
            ]))
            # os.system(f'ffplay -nodisp -autoexit -hide_banner -loglevel error {path}')

    # Prints history of chat
    async def print_history(self, message):
        sender = await self.client.get_entity(message.from_id if message.from_id else message.peer_id)
        name = utils.get_display_name(sender)
        msg = self.message_object(message)
        output = FormattedText([
            (self.__config.getVariable('user_color'), f'[{name}] » '),
            ('ansiwhite', msg),
        ])
        print(output)

    # Get peer from dialogs or ID
    def get_peer(self, peer):
        with open('assets/dialogs.json', 'r', encoding="utf-8") as dialogs_file:
            dialogs = json.load(dialogs_file)
            try:
                peer_id = int(peer)
            except:
                peer_id = dialogs[peer]
        return int(peer_id)

    # Command proccessing
    def proccess(self, command):
        # Write message
        if command.startswith('msg'):
            args = re.findall(r'(\#.+\#) (.+)', command)[0]
            peer_id = self.get_peer(args[0][1:-1])
            self.client.loop.run_until_complete(self.send_message(peer_id, args[1]))
        # Mute chat
        elif command.startswith('mute'):
            dialog_name = re.findall(r'(\#.+\#)', command)[0][1:-1]
            dialog_id = self.get_peer(dialog_name)
            mute = self.__config.getVariable('mute')
            if dialog_id not in mute:
                mute.append(dialog_id)
                self.__config.setVariable('mute', mute)
        # Reply to user
        elif command.startswith('reply'):
            args = re.findall(r'(\#.+\#) (\d+) (.+)', command)[0]
            peer_id = self.get_peer(args[0][1:-1])
            self.client.loop.run_until_complete(self.send_message(peer_id, args[2], reply=args[1]))
        # Send to the last recepient
        elif command.startswith('last'):
            self.client.loop.run_until_complete(self.send_message(self.last_peer, command[5:]))
        # Messages history
        elif command.startswith('history'):
            args = re.findall(r'(\#.+\#) (\d+)', command)[0]
            limit = int(args[-1])
            limit = limit if limit <= 50 else 50
            peer_id = self.get_peer(args[0][1:-1])
            messages = self.client.loop.run_until_complete(self.client.get_messages(peer_id, limit=limit))
            for message in reversed(messages):
                self.client.loop.run_until_complete(self.print_history(message))
        # Save and show image
        elif command.startswith('img'):
            msg_id = command[3:]
            self.client.loop.run_until_complete(self.show_image(msg_id))
        # Display list of contacts
        elif command == 'contacts':
            self.client.loop.run_until_complete(self.get_contacts())
        # Display list of chats
        elif command == 'chats':
            self.client.loop.run_until_complete(self.print_chats())
        # Silent mode (only contacts)
        elif command == 'silent':
            silent = self.__config.getVariable('only_contacts')
            silent = False if silent else True
            self.__config.setVariable('only_contacts', silent) 
            print(FormattedText(
                [
                    (self.__config.getVariable('user_color'), '[Тихий режим] '),
                    ('ansiwhite', 'Включен' if silent else 'Выключен')
                ]
            ))
        elif command == 'help':
            print(FormattedText(
                [
                    (self.__config.getVariable('user_color'), '[Сообщение] '),
                    ('ansiwhite', 'Я добавлю эту команду позже :)')
                ]
            ))
        # Play audio/video
        elif command.startswith('play'):
            msg_id = command[4:]
            self.client.loop.run_until_complete(self.playAudio(msg_id))
        # Exit session
        elif command == 'exit':
            exit(0)
