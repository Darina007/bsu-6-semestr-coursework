from datetime import datetime

import config
import utils

history = {}


def add_to_user_history(msg):
    if msg.chat.id in history:
        history[msg.chat.id].append((msg.text, 1))
        if len(history[msg.chat.id]) > 16:
            history[msg.chat.id].pop(0)
            history[msg.chat.id].pop(0)
    else:
        history[msg.chat.id] = [(msg.text, 1)]
    return history[msg.chat.id]


def historic_response_parser(txt, uid):
    resp = utils.rage_response_parser(txt).replace('Человек:', '')
    history[uid].append((resp, 0))
    return resp


def user_based_dialog_former(msg):
    if not msg.text or len(msg.text) < 1 or msg.text[0] == '/':
        return
    msg.text = utils.filter_symbol(msg.text, ":", " ")
    user_history = add_to_user_history(msg)
    start_text = 'Сейчас {} год. Я - {}. Встретил я человека, по имени {}. Решили поболтать.\n'.format(
        datetime.now().year, config.role,
        utils.translit(msg.chat.first_name).capitalize())
    dialog_text = ''
    offset = 0
    while len(start_text + dialog_text) > 1024 or offset == 0:
        dialog_text = ''
        for item in user_history[offset:]:
            if item[1] == 1:
                dialog_text += 'Человек: "' + item[0] + '".\n'
            else:
                dialog_text += 'Я: "' + item[0] + '".\n'
        dialog_text += 'Я: "'
        offset += 1
    return start_text + dialog_text
