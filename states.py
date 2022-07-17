from aiogram.dispatcher.filters import state

class States(state.StatesGroup):
    node_name = state.State()
    add_source = state.State()
    add_recipient = state.State()
    
    choise_node = state.State()
    node_settings = state.State()

    add_sources = state.State()
    add_recipients = state.State()
    del_sources = state.State()
    del_recipients = state.State()
    
    del_node = state.State()
    hot_words = state.State()
    input_words = state.State()
    word_settings = state.State()
    input_replace = state.State()

    users = state.State()
    add_user = state.State()
    del_user = state.State()