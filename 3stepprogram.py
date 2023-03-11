
import os, time, json, openai, requests, ast
from secrets import openai_key, novelai_key

from overall_imports import text_append, text_create, text_read, make_json, open_json, col, check_return, show_layer, cols
# those are all functions, except for cols. that just stores colors for col to use.

# get getters. these are functions that return functions that get stuff. (snippets, context, api response)
from for_snippets import get_snippets_getter
from for_context import get_context_getter
from for_api import get_api_caller

'''# the more basic version of the loop was this.

while True:
    """Bot responds in 3 steps: get snippets, make AI context, get AI response

    0) create a database of snippets
        (this one obviously doesnt count. who the fuck starts counting from 0 anyway)
        (hard to do. requires craftsmanship and testing.)
    1) gather relevant snippets
        (embedding search, also not easy to do, has lots of unexplored space)
    2) create a context for the api
        (pure string for normal apis, list of dictionaries with 'role' and 'content' keys for gpt turbo)
    3) make an api call"""

    question = input('What do you want to know?\n')
    # step 1
    snippets_getter, snippets_getter_info = get_snippets_getter()
    snippets = snippets_getter(question)
    # step 2
    context_getter, context_getter_info = get_context_getter()
    context = context_getter(snippets)
    # step 3
    api_caller, api_caller_info = get_api_caller()
    api_response = api_caller(context)
    # result
    print(f'The answer to your question is:\n{api_response}')
'''

for n, layer_color in enumerate(cols):
    print(col(layer_color, f'layer {n} has this color'))

while True:
    """Bot responds in 3 steps: get snippets, make AI context, get AI response

    0) create a database of snippets
        (this one obviously doesnt count. who the fuck starts counting from 0 anyway)
        (hard to do. requires craftsmanship and testing.)
    1) gather relevant snippets
        (embedding search, also not easy to do, has lots of unexplored space)
    2) create a context for the api
        (pure string for normal apis, list of dictionaries with 'role' and 'content' keys for gpt turbo)
    3) make an api call"""

    question = input('What do you want to know?\n')

    provider = 'novelai'

    # step 1: get snippets
    show_layer(0, 'calling snippets getter')
    snippets_getter, snippets_getter_info = get_snippets_getter()
    show_layer(0, ['snippets_getter_info', snippets_getter_info])
    snippets = snippets_getter(question)
    show_layer(0, 'done calling snippets getter')

    # step 2: get context
    show_layer(0, 'calling context getter')
    context_getter, context_getter_info = get_context_getter(provider)
    print(col('re', f'context_getter:{context_getter}'))
    show_layer(0, ['context_getter_info', context_getter_info])
    context = context_getter(question, snippets)
    show_layer(0, 'done calling context getter')

    # step 3: get response
    show_layer(0, 'calling api getter')
    api_caller, api_caller_info = get_api_caller(provider)
    show_layer(0, ['api_caller_info', api_caller_info])
    print('the actual input being used for the api. (for turbo its a list of dictionaries, otherwise its a pure string.)')
    print(col('gr', context))
    api_response = api_caller(context)
    show_layer(0, 'done calling api getter')

    # result
    print(f'the pure api response:')
    print(f'{col("gr",api_response)}')

    print('=============================')
    print('=============================')
    input('press enter to go again.')
