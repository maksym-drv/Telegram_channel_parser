import logging
from config import Config
from database import Database
from buttons import Button
from states import States
from aiogram import executor, types
from aiogram.dispatcher import FSMContext

# Configure logging
logging.basicConfig(level=logging.INFO)
cfg = Config()
btn = Button()
db = Database()

# first
@cfg.dp.message_handler(commands="start")
async def Start(message: types.Message):
    if await check_user(message.from_user.id):
        await cfg.bot.send_message(message.from_user.id, "Привет {}!\nЭтот бот".format(message.from_user.first_name) +
        " создан для парсинга чатов и каналов в Telegram", reply_markup=btn.markup)
    else:
        await cfg.bot.send_message(message.from_user.id, "Привет {}!\nК сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(lambda message: message.text == 'Добавить узел') 
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        await cfg.bot.send_message(message.from_user.id, "Введите название нового узла",
        reply_markup=btn.back)
        await States.node_name.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.node_name) 
async def setFolder(message: types.Message, state: FSMContext):
    if await check_user(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
        elif await db.check_node(message.text):
            await cfg.bot.send_message(message.from_user.id, "Узел с таким названием уже существует!")
        else:
            node_id = await db.create_node(message.text)
            await cfg.bot.send_message(message.from_user.id, "Узел успешно создан")
            await cfg.buffer.set_buffer(message.from_user.id, node_id)
            await cfg.bot.send_message(message.from_user.id, "Перешлите сообщение из канала-источника", reply_markup=btn.back)
            await States.add_source.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.add_source, content_types=['text', 'photo', 'video', 'voice', 'audio', 'document']) 
async def setFolder(message: types.Message, state: FSMContext):
    if await check_user(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
        elif message.forward_from_chat == None:
            await cfg.bot.send_message(message.from_user.id, "Сообщение должно быть пересланным из канала!")
        else:
            await db.add_source(
                message.forward_from_chat['id'], 
                message.forward_from_chat['title'],
                (await cfg.buffer.get_buffer())[str(message.from_user.id)]
                )
            await cfg.bot.send_message(message.from_user.id, "Перешлите сообщение из канала-получателя", reply_markup=btn.back)
            await States.add_recipient.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.add_recipient, content_types=['text', 'photo', 'video', 'voice', 'audio', 'document']) 
async def setFolder(message: types.Message, state: FSMContext):
    if await check_user(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
        elif message.forward_from_chat == None:
            await cfg.bot.send_message(message.from_user.id, "Сообщение должно быть пересланным из канала!")
        else:
            await db.add_recipient(
                message.forward_from_chat['id'], 
                message.forward_from_chat['title'],
                (await cfg.buffer.get_buffer())[str(message.from_user.id)]
                )
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", reply_markup=btn.markup)
            await state.finish()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

# nodes

@cfg.dp.message_handler(lambda message: message.text == 'Мои узлы') 
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        await cfg.bot.send_message(message.from_user.id, "Список ваших узлов:\n" + 
        f"{await print_list(await db.get_nodes(), '/')}\n\nВыберите узел для взаимодействия",
        reply_markup=btn.back)
        await States.choise_node.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.choise_node)
async def folders_apps(message: types.Message, state: FSMContext):
    if await check_user(message.from_user.id):
        node_name = ''
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
            return
        try:
            node_name = message.text.split('/')[1]
        except:
            await cfg.bot.send_message(message.from_user.id, "Узел с таким именем не найден!\n\nВы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
            return
        if not await db.check_node(node_name):
            await cfg.bot.send_message(message.from_user.id, "Узел с таким именем не найден!\n\nВы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
        else:
            await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
            f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
            f' их в каналы\n{await print_list(await db.get_recipients(node_name))}'
            , reply_markup=btn.settings_node)
            await cfg.buffer.set_buffer(message.from_user.id, node_name)
            await States.node_settings.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.node_settings)
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Список ваших узлов:\n" + 
            f"{await print_list(await db.get_nodes(), '/')}\n\nВыберите узел для взаимодействия",
            reply_markup=btn.back)
            await States.choise_node.set()
        elif message.text == "Добавить источник":
            await cfg.bot.send_message(message.from_user.id, "Перешлите сообщение из канала-источника", 
            reply_markup=btn.back)
            await States.add_sources.set()
        elif message.text == "Удалить источник":
            await cfg.bot.send_message(message.from_user.id, "Введите номер канала-источника который" +
            f" хотите удалить:\n{await print_list(await db.get_sources((await cfg.buffer.get_buffer())[str(message.from_user.id)]))}", 
            reply_markup=btn.back)
            await States.del_sources.set()
        elif message.text == "Добавить получателя":
            await cfg.bot.send_message(message.from_user.id, "Перешлите сообщение из канала-получателя", 
            reply_markup=btn.back)
            await States.add_recipients.set()
        elif message.text == "Удалить получателя":
            await cfg.bot.send_message(message.from_user.id, "Введите номер канала-получателя который" +
            f" хотите удалить:\n{await print_list(await db.get_recipients((await cfg.buffer.get_buffer())[str(message.from_user.id)]))}", 
            reply_markup=btn.back)
            await States.del_recipients.set()
        elif message.text == "Удалить узел":
            await cfg.bot.send_message(message.from_user.id, f'Вы уверены, что хотите удалить узел?',
            reply_markup=btn.delete_node_markup)
            await States.del_node.set()
        elif message.text == "Горячие слова":
            node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
            await cfg.bot.send_message(message.from_user.id, f'Горячие слова узла {node_name}:\n{await print_ignore(node_name)}' +
            '\n\nЧтобы удалить горячие слова, введите их номер',
            reply_markup=btn.ignore_markup)
            await States.hot_words.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

# node operations
@cfg.dp.message_handler(state=States.hot_words)
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
            f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
            f' их в каналы\n{await print_list(await db.get_recipients(node_name))}'
            , reply_markup=btn.settings_node)
            await States.node_settings.set()
        elif message.text.isdigit() and int(message.text) > 0:
            words = await db.get_ignore(node_name)
            if int(message.text) <= len(words):
                await db.del_ignore(words[int(message.text) - 1][3], await db.get_node_id(node_name))
                await cfg.bot.send_message(message.from_user.id, "Текст успешно удалён!")
                await cfg.bot.send_message(message.from_user.id, f'Горячие слова узла {node_name}:\n{await print_ignore(node_name)}' +
                '\n\nЧтобы удалить горячие слова, введите их номер',
                reply_markup=btn.ignore_markup)
                await States.hot_words.set()
            else:
                await cfg.bot.send_message(message.from_user.id, "Указанный текст не найден!")
        elif message.text == "Добавить горячие слова":
                await cfg.bot.send_message(message.from_user.id, "Введите горячие слова", reply_markup=btn.hot_keys_markup)
                await States.input_words.set()
        else:
            await cfg.bot.send_message(message.from_user.id, "Данные введены некорректно!")
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.input_words)
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, f'Горячие слова узла {node_name}:\n{await print_ignore(node_name)}' +
            '\n\nЧтобы удалить горячие слова, введите их номер',
            reply_markup=btn.ignore_markup)
            await States.hot_words.set()
            return
        await cfg.bot.send_message(message.from_user.id, 'Выберите операцию с текстом', reply_markup=btn.word_markup)
        await cfg.words.set_buffer(message.from_user.id, message.text)
        await States.word_settings.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.word_settings)
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        string_text = (await cfg.words.get_buffer())[str(message.from_user.id)]
        if message.text == "Игнорировать сообщение":
            await db.add_ignore(
                string_text,
                None,
                True,
                await db.get_node_id(node_name))
            await cfg.bot.send_message(message.from_user.id, 'Горячие слова добавлены')
            await cfg.bot.send_message(message.from_user.id, f'Горячие слова узла {node_name}:\n{await print_ignore(node_name)}' +
            '\n\nЧтобы удалить горячие слова, введите их номер',
            reply_markup=btn.ignore_markup)
            await States.hot_words.set()
        elif message.text == "Вырезать текст":
            await db.add_ignore(
                string_text,
                None,
                False,
                await db.get_node_id(node_name))
            await cfg.bot.send_message(message.from_user.id, 'Горячие слова добавлены')
            await cfg.bot.send_message(message.from_user.id, f'Горячие слова узла {node_name}:\n{await print_ignore(node_name)}' +
            '\n\nЧтобы удалить горячие слова, введите их номер',
            reply_markup=btn.ignore_markup)
            await States.hot_words.set()
        elif message.text == "Заменить текст":
            await cfg.bot.send_message(message.from_user.id, 'Введите текст для замены', reply_markup=types.ReplyKeyboardRemove())
            await States.input_replace.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.input_replace)
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        string_text = (await cfg.words.get_buffer())[str(message.from_user.id)]
        await db.add_ignore(
                string_text,
                message.text,
                False,
                await db.get_node_id(node_name))
        await cfg.bot.send_message(message.from_user.id, 'Горячие слова добавлены')
        await cfg.bot.send_message(message.from_user.id, f'Горячие слова узла {node_name}:\n{await print_ignore(node_name)}' +
        '\n\nЧтобы удалить горячие слова, введите их номер',
        reply_markup=btn.ignore_markup)
        await States.hot_words.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.del_node)
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
            f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
            f' их в каналы\n{await print_list(await db.get_recipients(node_name))}'
            , reply_markup=btn.settings_node)
            await States.node_settings.set()
        elif message.text == "Да":
            await db.del_node(node_name)
            await cfg.bot.send_message(message.from_user.id, "Список ваших узлов:\n" + 
            f"{await print_list(await db.get_nodes(), '/')}\n\nВыберите узел для взаимодействия",
            reply_markup=btn.back)
            await States.choise_node.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.add_sources, content_types=['text', 'photo', 'video', 'voice', 'audio', 'document'])
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
            f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
            f' их в каналы\n{await print_list(await db.get_recipients(node_name))}'
            , reply_markup=btn.settings_node)
            await States.node_settings.set()
        else:
            try:
                await db.add_source(
                message.forward_from_chat['id'], 
                message.forward_from_chat['title'],
                await db.get_node_id(node_name)
                )
                await cfg.bot.send_message(message.from_user.id, 'Добавлен новый источник')
            except:
                await cfg.bot.send_message(message.from_user.id, 'Источник не удалось добавить в узел!')
            finally:
                await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
                f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
                f' их в каналы\n{await print_list(await db.get_recipients(node_name))}'
                , reply_markup=btn.settings_node)
                await States.node_settings.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.add_recipients, content_types=['text', 'photo', 'video', 'voice', 'audio', 'document'])
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
            f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
            f' их в каналы\n{await print_list(await db.get_recipients(node_name))}'
            , reply_markup=btn.settings_node)
            await States.node_settings.set()
        else:
            try:
                await db.add_recipient(
                message.forward_from_chat['id'], 
                message.forward_from_chat['title'],
                await db.get_node_id(node_name)
                )
                await cfg.bot.send_message(message.from_user.id, 'Добавлен новый источник')
            except:
                await cfg.bot.send_message(message.from_user.id, 'Получателя не удалось добавить в узел!')
            finally:
                await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
                f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
                f' их в каналы\n{await print_list(await db.get_recipients(node_name))}'
                , reply_markup=btn.settings_node)
                await States.node_settings.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.del_sources)
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        if message.text == "Вернуться назад":
            pass
        elif message.text.isdigit() and int(message.text) > 0:
            sources_list = await db.get_sources(node_name)
            if int(message.text) <= len(sources_list):
                await db.del_source(sources_list[int(message.text) - 1][1])
                await cfg.bot.send_message(message.from_user.id, "Источник успешно удалён!")
            else:
                await cfg.bot.send_message(message.from_user.id, "Указанный источник не найден!")
        else:
            await cfg.bot.send_message(message.from_user.id, "Данные введены некорректно!")
        await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
        f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
        f' их в каналы\n{await print_list(await db.get_recipients(node_name))}'
        , reply_markup=btn.settings_node)
        await States.node_settings.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.del_recipients)
async def folders_apps(message: types.Message):
    if await check_user(message.from_user.id):
        node_name = (await cfg.buffer.get_buffer())[str(message.from_user.id)]
        if message.text == "Вернуться назад":
            pass
        elif message.text.isdigit() and int(message.text) > 0:
            recipients_list = await db.get_recipients(node_name)
            if int(message.text) <= len(recipients_list):
                await db.del_recipient(recipients_list[int(message.text) - 1][1])
                await cfg.bot.send_message(message.from_user.id, "Получатель успешно удалён!")
            else:
                await cfg.bot.send_message(message.from_user.id, "Указанный получатель не найден!")
        else:
            await cfg.bot.send_message(message.from_user.id, "Данные введены некорректно!")
        await cfg.bot.send_message(message.from_user.id, f'Узел {node_name} принимает сообщения из каналов:\n' +
        f'{await print_list(await db.get_sources(node_name))}\n\nи передаёт' +
        f' их в каналы\n{await print_list(await db.get_recipients(node_name))}', 
        reply_markup=btn.settings_node)
        await States.node_settings.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

# users

@cfg.dp.message_handler(lambda message: message.text == 'Пользователи') 
async def users(message: types.Message):
    if await check_user(message.from_user.id):
        await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
        await States.users.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.users) 
async def set_users(message: types.Message, state: FSMContext):
    if await check_user(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Вы в главном меню", 
            reply_markup=btn.markup)
            await state.finish()
        if message.text == "Добавить пользователя":
            await cfg.bot.send_message(message.from_user.id, "Введите id нового пользователя:", reply_markup=btn.back)
            await States.add_user.set()
        elif message.text == "Удалить пользователя":
            await cfg.bot.send_message(message.from_user.id, f"Укажите номер ID пользователя, которого хотите удалить\n\nСписок пользователей:{await print_users()}", reply_markup=btn.back)
            await States.del_user.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.add_user) 
async def add_user(message: types.Message):
    if await check_user(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
            await States.users.set()
        else:
            await cfg.users.add_user(message.text)
            await cfg.bot.send_message(message.from_user.id, "Пользователь успешно добавлен !")
            await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
            await States.users.set()
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

@cfg.dp.message_handler(state=States.del_user) 
async def del_user(message: types.Message):
    if await check_user(message.from_user.id):
        if message.text == "Вернуться назад":
            await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
            await States.users.set()
        elif message.text.isdigit() and int(message.text) > 0:
            users = await cfg.users.get_users()
            user_id = users[int(message.text) - 1]
            if int(message.text) <= len(users):
                if message.from_user.id == user_id:
                    await cfg.users.del_user(user_id)
                    await cfg.bot.send_message(message.from_user.id, "ID пользователя успешно удалён !")
                    await cfg.bot.send_message(message.from_user.id, "Выберите операцию над пользователями:", reply_markup=btn.user_markup)
                    await States.users.set()
                else:
                    await cfg.bot.send_message(message.from_user.id, "Вы не можете удалить сами себя!")
            else:
                await cfg.bot.send_message(message.from_user.id, "Указанный id пользователя не найдена!")
        else:
            await cfg.bot.send_message(message.from_user.id, "Данные введены некорректно!")
    else:
        await cfg.bot.send_message(message.from_user.id, "К сожалению,".format(message.from_user.first_name) +
        " этот бот для вас недоступен, обратитесь к администратору :(")

async def check_user(user_id):
    for user in await cfg.users.get_users():
        if str(user) == str(user_id):
            return True
    return False

async def print_list(action, param: str = ''):
    data_list = ""
    index = 0
    for data in action:
        index += 1
        data = f"\n{index}. "+ param + data[0]
        data_list += data
    if data_list == "":
        data_list = "\nсписок пуст!"
    return data_list

async def print_users():
    users = ""
    index = 0
    for user in await cfg.users.get_users():
        index += 1
        user = "\n{}. ".format(index) + user
        users += user
    if users == "":
        users = "\ncписок пользователей пуст!"
    return users

async def print_ignore(node_name: str):
    words = ""
    index = 0
    for word in await db.get_ignore(node_name):
        add = '- вырезается из сообщения'
        if word[2]:
            add = '- сообщение игнорируется'
        elif not word[1] == None:
            add = f'- заменяется на «{word[1]}»'
        index += 1
        word = f"\n{index}. «{word[0]}» " + add
        words += word
    if words == "":
        words = "\ncписок пуст!"
    return words

if __name__ == "__main__":
    executor.start_polling(cfg.dp, skip_updates=True)