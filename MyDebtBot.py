'''Телеграм бот для учета долгов участников чата'''

# import csv
import os
import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException

from config import TOKEN

CHAT_IDS_FILE = 'chat_ids.txt'

p = print


def get_chat_ids_file():
    '''Путь к файлу chat_ids'''
    folder_path = "data"
    # Проверяем, существует ли папка
    if not os.path.exists(folder_path):
        # Если папка не существует, создаем её
        os.makedirs(folder_path)

    # Путь к файлу, который нужно создать
    file_path = os.path.join(folder_path, "chat_ids.txt")
    return file_path


CHAT_IDS_FILE = get_chat_ids_file()


def tt(t):
    print(type(t))


class MyDebtBot:
    '''Бот для подсчтета долгов'''

    def __init__(self):
        self.chat_ids = self.read_chat_ids()
        self.bot = telebot.TeleBot(TOKEN)
        self.users_data = {}
        self.send_welcome_to_all_chats()
        # Обработчики сообщений
        self.bot.message_handler(
            content_types=['new_chat_members'])(self.new_chat)
        self.bot.message_handler(
            func=lambda message: True)(self.handle_message)

    def read_chat_ids(self, file_name=CHAT_IDS_FILE) -> set:
        '''Функция для чтения chat_ids из файла CHAT_IDS_FILE'''
        chat_ids = set()
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    chat_id = line.strip()
                    if chat_id:
                        chat_ids.add(int(chat_id))
        except FileNotFoundError:
            pass  # Если файла нет, просто возвращаем пустой set
        return chat_ids

    def write_chat_ids(self, file_name=CHAT_IDS_FILE):
        '''Функция для записи chat_ids в файл CHAT_IDS_FILE'''
        with open(file_name, 'w') as file:
            for chat_id in self.chat_ids:
                file.write(f"{chat_id}\n")

    def print(self, chat_id, text):
        '''Отправка сообщения в чат'''
        self.bot.send_message(chat_id, text)

    @staticmethod
    def remove_chat_id_from_file(chat_id_to_remove, filename=CHAT_IDS_FILE):
        '''Удаление chat_id из вайла chat_ids.txt'''
        # Преобразуем chat_id в строку, чтобы сравнивать с данными в файле
        chat_id_to_remove = str(chat_id_to_remove)

        try:
            with open(filename, 'r') as file:
                # Читаем все строки из файла
                lines = file.readlines()

            with open(filename, 'w') as file:
                for line in lines:
                    # Если строка не содержит нужный chat_id, записываем её обратно в файл
                    if line.strip() != chat_id_to_remove:
                        file.write(line)
        except FileNotFoundError:
            print(f"Ошибка: Файл {filename} не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def send_welcome_to_all_chats(self):
        '''Функция для отправки стартового сообщения во все чаты'''
        
        welcome_message = "Бот перезапущен"
        for chat_id in self.chat_ids:
            try:
                chat_title = self.bot.get_chat(chat_id).title
                print(chat_title)
                if chat_title == 'ttttttttttttttt':
                    try:
                        self.bot.send_message(chat_id, welcome_message)
                    except ApiTelegramException as e:
                        if e.error_code == 403 and "bot was kicked from the supergroup chat" in e.description:
                            print(
                                f"Ошибка: Бот был удален из чата {chat_id}. Сообщение не отправлено.")
                            self.remove_chat_id_from_file(chat_id)
                        else:
                            print(f"Произошла ошибка: {e}")
            except ApiTelegramException as e:
                if e.error_code == 403 and "bot was kicked from the supergroup chat" in e.description:
                    print(
                        f"Ошибка: Бот был удален из чата {chat_id}. Сообщение не отправлено.")
                    self.remove_chat_id_from_file(chat_id)
                else:
                    print(f"Произошла ошибка: {e}")


    def get_user(self, message, username):
        '''Поиск юзера по его @username (не работает!)'''
        chat_id = message.chat.id
        username = username[1:]
        try:
            # Получаем информацию о пользователе по username
            user = self.bot.get_chat_member(chat_id, username).user
            first_name = user.first_name
            last_name = user.last_name if user.last_name else ""
            # Формируем полное имя
            full_name = f'{first_name} {last_name}' if last_name else first_name
            return full_name
        except Exception as e:
            print(
                f"Не удалось получить информацию о пользователе @{username}: {e}")
            return None

    def new_chat(self, message):
        '''Обработчик события добавления бота в новый чат'''
        chat_id = message.chat.id
        if chat_id not in self.chat_ids:
            self.chat_ids.add(chat_id)  # Добавляем новый chat_id в список
            self.write_chat_ids()  # Записываем обновленный список в файл
            self.bot.send_message(
                chat_id, "Я бот. Умею хранить ваши долги. Напишите сообщение вида @username 100")

    @staticmethod
    def write_table(file_name, name1, name2, new_debt):
        try:
            # Считываем все строки из файла
            with open(file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            # Если файла нет, создаем пустой список строк
            lines = []
        found = False
        updated_lines = []
        for line in lines:
            # Убираем лишние пробелы
            line = line.strip()
            # Проверяем формат name1 name2: debt
            if line.startswith(f"{name1} {name2}:"):
                current_debt = float(line.split(':')[1].strip())
                new_line = f"{name1} {name2}: {current_debt + new_debt}\n"
                updated_lines.append(new_line)
                found = True
            # Проверяем формат name2 name1: debt
            elif line.startswith(f"{name2} {name1}:"):
                current_debt = float(line.split(':')[1].strip())
                new_line = f"{name2} {name1}: {current_debt - new_debt}\n"
                updated_lines.append(new_line)
                found = True
            else:
                # Если строка не соответствует ни одному из форматов, просто добавляем ее в результат
                updated_lines.append(line + '\n')
        if not found:
            # Если ни одна из записей не найдена, добавляем новую строку
            new_line = f"{name1} {name2}: {new_debt}\n"
            updated_lines.append(new_line)
        # Записываем обновленные строки обратно в файл
        with open(file_name, 'w') as file:
            file.writelines(updated_lines)

    @staticmethod
    def read_table(file_name, name1, name2):
        try:
            # Считываем все строки из файла
            with open(file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            # Если файл не найден, возвращаем 0
            return 0.0
        for line in lines:
            line = line.strip()
            # Проверяем формат name1 name2: debt
            if line.startswith(f"{name1} {name2}:"):
                debt = float(line.split(':')[1].strip())
                return debt
            # Проверяем формат name2 name1: debt
            elif line.startswith(f"{name2} {name1}:"):
                debt = float(line.split(':')[1].strip())
                return -debt
        # Если ни одна из записей не найдена, возвращаем 0
        return 0.0

    @staticmethod
    def search_table(file_name, username):
        results = []
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            return results
        for line in lines:
            line = line.strip()
            parts = line.split(':')
            if len(parts) != 2:
                continue
            users, debt = parts
            users = users.strip().split()
            debt = float(debt.strip())
            if len(users) == 2:
                name1, name2 = users
                if name1 == username:
                    results.append((name2, debt))
                elif name2 == username:
                    results.append((name1, -debt))
        return results

    @staticmethod
    def get_path(chat_id):
        '''Путь к файлу csv'''
        directory = 'data'
        # Убедимся, что папка существует
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Путь к файлу CSV
        file_name = f"{chat_id}.csv"
        file_path = os.path.join(directory, file_name)
        return file_path

    def handle_message(self, message: types.Message):
        '''Функция для обработки сообщений'''
        chat_id = message.chat.id
        sender = f'@{message.from_user.username}'
        if chat_id not in self.chat_ids:
            self.chat_ids.add(chat_id)
            self.write_chat_ids()
        # @username amount # Новый долг
        if ' ' in message.text:
            try:
                username, amount = message.text.split()
                if username.startswith('@') and self.is_number(amount):
                    amount = float(amount)
                    table_path = self.get_path(chat_id)
                    debt = self.read_table(table_path, sender, username)
                    new_debt = debt + amount
                    debt_str = int(debt) if debt.is_integer() else debt
                    amount_str = int(amount) if amount.is_integer() else amount
                    new_debt_str = int(
                        new_debt) if new_debt.is_integer() else new_debt
                    text = (f'{debt_str} + {amount_str} = {new_debt_str}\n'
                            f'{sender} должен {new_debt_str} пользователю {username}')
                    self.write_table(table_path, sender, username, amount)
                    self.bot.send_message(chat_id, text)
            except ValueError as e:
                if "too many values to unpack" in str(e):
                    self.print(chat_id,
                               ('Не понял вас. Правильный формат записи: \n'
                                '@username 100'
                                ))
        # /start            # приветственное сообщение
        elif message.text == '/start':
            self.bot.reply_to(
                message, 'Привет! Я бот для ведения счетов в групповом чате.')
        # @username --      # стираем задолженность
        elif message.text == '--':
            pass
        # @username         # показать все задолженности
        elif message.text.startswith('@') and ' ' not in message.text:

            table_path = self.get_path(chat_id)
            name_list = self.search_table(table_path, message.text)
            text = (f'Должник {message.text}\n'
                    f'Кому должен : сколько должен\n'
                    )
            for item in name_list:
                num = int(item[1]) if item[1].is_integer() else item[1]
                text += f'{item[0]} : {num} \n'
            self.bot.send_message(chat_id, text)

    @staticmethod
    def is_number(string):
        try:
            float(string)  # Попытка конвертировать строку в число
            return True
        except ValueError:
            return False
