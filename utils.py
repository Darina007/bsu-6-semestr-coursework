import re

translitDict = {
    'eng': 'qwertyuiopasdfghjklzxcvbnm',
    'ru': 'квертиуиопасдфжхжклзкцвбнм'
}


def filter_symbol(string, symbol, alternative):
    return string.replace(symbol, alternative)


def translit(input_text):
    """Удаляет непонятные символы и транслитит английский текст на кириллицу (🚲)"""
    output = []
    input_text = re.sub('[^a-zA-ZА-Яа-яёЁ_ \-]+', '', input_text)
    input_text = input_text.lower().replace('x', 'ks').replace(
        'j', 'dj').replace('sh', 'ш').replace('zh', 'ж').replace('ch', 'ч')
    for char in input_text:
        output.append(
            char.translate(
                str.maketrans(translitDict.get('eng'),
                              translitDict.get('ru'))))
    return ''.join(output)


def cut_extra_stuff(txt):
    """Вырезает артефакты"""
    extra = txt.find('\n\n\n')
    return txt[0:extra] if extra != -1 else txt


def rage_response_parser(txt):
    return txt[0:txt.find('"')]
