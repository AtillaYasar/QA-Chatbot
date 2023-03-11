"""This is step 2/3 for the Q&A algorithm: Create a context for the AI to generate from.

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

from overall_imports import text_append, text_create, text_read, make_json, open_json, col, check_return, show_layer

def get_context_getter(provider):
    """This returns *the function* that will be used to assemble the context for the AI."""

    location = 'context'
    layer_n = 1
    show_layer(layer_n, [f'get {location} getter', f'provider:{provider}'])

    def getter_normal(question, snippets):
        """This assembles the context for the api, using 'question' and 'snippets' args."""

        lines = []
        lines.append('The following is an example of a task description, followed by a correct performance on the task.')
        lines.append('It will be used as a reference point for how to answer questions in a helpful, insightful, and intelligent manner.')
        lines.append('If a question is weird or unexpected or unrelated to the snippets, a straightforwardly true answer is still required.')
        lines.append('')
        lines.append('TASK DESCRIPTION')
        lines.append('-----------')
        lines.append('Your job is to answer a question, by using a collection of text snippets.')
        lines.append('')
        for n, string in enumerate(snippets):
            lines.append(f'snippet {n}:')
            lines.append(string)
            lines.append('')
        lines.append('TASK PERFORMANCE')
        lines.append('-----------')
        lines.append(f'Question:')
        lines.append(question)
        lines.append('')
        lines.append('Answer:\n')
        
        assembled = '\n'.join(lines)
        return assembled
    
    def getter_turbo(question, snippets):
        messages = []  # will be used in the payload for the api.

        # helper function
        def add_message(role, content):
            assert role in ('system', 'assistant', 'user')
            messages.append({
                'role':role,
                'content':content,
            })

        # creates the part of the system message about snippets.
        lines = []
        for n, string in enumerate(snippets):
            lines.append('snippet {n}')
            lines.append(string)
            lines.append('')
        # use lines to create the initial system message.
        add_message(
            'system',
            'Your job is to answer questions, using the following snippets of text as a potential source of information:' + '\n'.join(lines),
        )

        # add the actual question, as a 'user' message.
        add_message(
            'user',
            question,
        )

        add_message(
            'system',
            'Note: If the question is unrelated to the snippets, please try to answer regardless.'
        )

        return messages
    
    if provider in ('novelai', 'codex'):
        getter = getter_normal
    elif provider == 'turbo':
        getter = getter_turbo
    else:
        raise ValueError

    info = {
        'description':f'context getter for provider:{provider}, getter name:{getter}'
    }
    to_return = (
        getter,
        info,
    )
    check_return(to_return)
    return to_return