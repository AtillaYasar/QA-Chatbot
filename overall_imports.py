import os, time, json

# from overall_imports import text_append, text_create, text_read, make_json, open_json, col, check_return, show_layer, cols

cols = [
    'ma',
    'cy',
    'ye',
]

def text_append(path, appendage):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(appendage)

def text_create(path, content=''):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def text_read(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        contents = f.read()
    return contents

def make_json(dic, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(dic, f, indent=2)
        f.close()

def open_json(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        contents = json.load(f)
        f.close()
    return contents

def col(ft, s):
    """For printing text with colors.

    Uses ansi escape sequences. (ft is "first two", s is "string")"""
    # black-30, red-31, green-32, yellow-33, blue-34, magenta-35, cyan-36, white-37
    u = '\u001b'
    numbers = dict([(string,30+n) for n, string in enumerate(('bl','re','gr','ye','blu','ma','cy','wh'))])
    n = numbers[ft]
    return f'{u}[{n}m{s}{u}[0m'

def check_return(tup):
    # enforce return from getter getters
    assert callable(tup[0])
    assert type(tup[1]) is dict

def show_layer(layer_n, to_print):
    # to_print can be a string or any list of objects that you can call str on.
    if type(to_print) is str:
        pass
    else:
        to_print = ''.join(map(str, to_print))
    print(col(cols[layer_n], f'(layer {layer_n}) ' + to_print))
