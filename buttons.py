from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class Button:
    def __init__(self):
        button_add = KeyboardButton('Добавить узел')
        button_all = KeyboardButton('Мои узлы')
        button_users = KeyboardButton('Пользователи')
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True).row(button_add).row(button_all).row(button_users)

        button_back = KeyboardButton('Вернуться назад')
        self.back = ReplyKeyboardMarkup(resize_keyboard=True).row(button_back)

        hot_word = KeyboardButton('Горячие слова')
        del_node = KeyboardButton('Удалить узел')
        add_source = KeyboardButton('Добавить источник')
        add_recipient = KeyboardButton('Добавить получателя')
        delete_source = KeyboardButton('Удалить источник')
        delete_recipient = KeyboardButton('Удалить получателя')
        self.settings_node = ReplyKeyboardMarkup(resize_keyboard=True).row(add_source, add_recipient).row(delete_source, delete_recipient).row(hot_word).row(del_node).row(button_back)
        
        yes_button = KeyboardButton('Да')
        self.delete_node_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(yes_button).row(button_back)

        add_user = KeyboardButton('Добавить пользователя')
        del_user = KeyboardButton('Удалить пользователя')
        self.user_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(add_user, del_user).row(button_back)
    
        add_ignore = KeyboardButton('Добавить горячие слова')
        self.ignore_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(add_ignore).row(button_back)

        button_ignore = KeyboardButton('Игнорировать сообщение')
        button_cut = KeyboardButton('Вырезать текст')
        button_replace = KeyboardButton('Заменить текст')
        self.word_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(button_ignore).row(button_cut).row(button_replace)

        id_hot_button = KeyboardButton('@')
        http_hot_button = KeyboardButton('http://')
        https_button = KeyboardButton('https://')
        self.hot_keys_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(id_hot_button).row(http_hot_button).row(https_button).row(button_back)