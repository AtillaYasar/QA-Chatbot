"""This is step 1/3 for the Q&A algorithm: ~~create a database of snippets~~ get snippets.

The overall plan:

Bot responds in 3 steps: get snippets, make AI context, get AI response

0) create a database of snippets
    (this one obviously doesnt count. who the fuck starts counting from 0 anyway)
    (hard to do. requires craftsmanship and testing.)
1) gather relevant snippets
    (embedding search, also not easy to do, has lots of unexplored space)
2) create a context for the api
    (pure string for normal apis, list of dictionaries with 'role' and 'content' keys for gpt turbo)
3) make an api call"""

import os, time, json, openai, requests, ast
from secrets import openai_key, novelai_key

from overall_imports import text_append, text_create, text_read, make_json, open_json, col, check_return, show_layer


def get_snippets_getter(*args, **kwargs):
    location = 'snippets'
    layer_n = 1
    show_layer(layer_n, [f'get {location} getter', args, kwargs])
    
    def getter(*args, **kwargs):
        filename = 'snippets.txt'
        splitter = '\n\n'
        i = input(f'put snippets in {col("re",filename)}, it will split by {col("re", str([splitter]))}, if you are done, press enter.')
        snippets = text_read(filename).split(splitter)

        show_layer(layer_n, [f'{location} getter', args, kwargs, f'snippets:{snippets}'])
        return snippets
    info = {
        'description':'mock snippets getter'
    }
    to_return = (
        getter,
        info,
    )
    check_return(to_return)
    return to_return
