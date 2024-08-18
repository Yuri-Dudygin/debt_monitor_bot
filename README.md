# Telegram Debt Bot

<details>
  <summary>Русский</summary>

Этот код представляет собой Телеграм-бота, предназначенного для учета долгов участников чата. Он отслеживает и записывает долги между пользователями, а также взаимодействует с пользователями через сообщения и команды в чате.

## Доступные команды бота:
- **`@username 100`**  
  Бот запомнит, что вы должны пользователю **`@username`** 100 денег.
- **`@username`**  
  Бот выведет список всех людей, кому пользователь **`@username`** должен.

## Внимание!
Для работы вам требуется самостоятельно создать файл **`config.py`** и прописать в нем строчку вида:

```python
TOKEN = 'MY_TOKEN'
```

Вместо **`MY_TOKEN`** укажите токен вашего бота, полученный от [@BotFather](https://t.me/BotFather).

## Инициализация и базовая настройка

### Создание экземпляра бота
- В классе **`MyDebtBot`** инициализируется Телеграм-бот с использованием токена, загружаются ID чатов из файла и настраиваются обработчики сообщений.

### Обработка событий нового чата
- При добавлении бота в новый чат его ID сохраняется в файл, и бот отправляет приветственное сообщение с кратким описанием своих возможностей.

## Работа с ID чатов

### Чтение и запись ID чатов
- ID чатов, в которых бот активен, сохраняются в файл **`chat_ids.txt`**. Это позволяет боту отправлять сообщения всем активным чатам и восстанавливать работу после перезапуска.

### Удаление ID чата
- Если бот был удален из чата, соответствующий ID удаляется из файла, чтобы избежать дальнейших попыток отправки сообщений в этот чат.

## Обработка сообщений

### Добавление долга
- Если сообщение содержит упоминание пользователя (например, **`@username`**) и сумму, бот добавляет указанную сумму к текущему долгу или создает новый долг.

### Просмотр долгов
- Если пользователь упоминает другого пользователя без указания суммы, бот показывает список долгов между этими пользователями.

### Приветственное сообщение
- Команда **`/start`** отправляет приветственное сообщение с описанием возможностей бота.

## Работа с таблицей долгов

### Запись долга
- Долги между пользователями сохраняются в **CSV-файл**. Если долг уже существует, он обновляется; если нет — создается новая запись.

### Чтение долга
- Бот может читать текущий долг между двумя пользователями.

### Поиск долгов
- Бот ищет и отображает все записи о долгах, связанных с конкретным пользователем.

## Обработка ошибок

### Работа с файлами
- Если при работе с файлами возникают ошибки (например, файл не найден), бот просто игнорирует их или создает пустой файл.

### Работа с Телеграм API
- Если бот был удален из чата, это событие корректно обрабатывается, и бот удаляет соответствующий ID из списка активных чатов.

## Заключение
Этот бот предназначен для автоматизации учета долгов в Телеграм-чате, что позволяет пользователям легко отслеживать и управлять своими финансовыми обязательствами в групповом общении.
</details>

___
This code represents a Telegram bot designed to track debts among chat participants. It records debts between users and interacts with them through messages and commands in the chat.

## Available Bot Commands:
- **`@username 100`**  
  The bot will remember that you owe **`@username`** 100 units of currency.
- **`@username`**  
  The bot will display a list of all people **`@username`** owes.

## Attention!
You need to create a **`config.py`** file and add the following line to it:

```python
TOKEN = 'MY_TOKEN'
```

Replace **`MY_TOKEN`** with your bot's token, which you can get from [@BotFather](https://t.me/BotFather).

## Initialization and Basic Setup

### Bot Instance Creation
- The **`MyDebtBot`** class initializes the Telegram bot using the token, loads chat IDs from a file, and sets up message handlers.

### New Chat Event Handling
- When the bot is added to a new chat, its ID is saved to a file, and the bot sends a welcome message with a brief description of its features.

## Working with Chat IDs

### Reading and Writing Chat IDs
- The chat IDs where the bot is active are saved to the **`chat_ids.txt`** file. This allows the bot to send messages to all active chats and restore operation after a restart.

### Deleting a Chat ID
- If the bot is removed from a chat, the corresponding ID is deleted from the file to prevent further attempts to send messages to that chat.

## Message Handling

### Adding a Debt
- If a message contains a mention of a user (e.g., **`@username`**) and an amount, the bot adds the specified amount to the current debt or creates a new debt.

### Viewing Debts
- If a user mentions another user without specifying an amount, the bot displays a list of debts between those users.

### Welcome Message
- The **`/start`** command sends a welcome message with a description of the bot's features.

## Working with the Debt Table

### Recording a Debt
- Debts between users are saved to a **CSV file**. If a debt already exists, it is updated; if not, a new record is created.

### Reading a Debt
- The bot can read the current debt between two users.

### Searching for Debts
- The bot searches and displays all debt records related to a specific user.

## Error Handling

### Working with Files
- If errors occur while working with files (e.g., file not found), the bot simply ignores them or creates an empty file.

### Working with the Telegram API
- If the bot is removed from a chat, this event is handled correctly, and the bot deletes the corresponding ID from the list of active chats.

## Conclusion
This bot is designed to automate debt tracking in a Telegram chat, allowing users to easily monitor and manage their financial obligations in a group setting.
