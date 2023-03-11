# the basic idea
```python
# How to make a Q&A bot.
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
```

# requirements  (as far as i know):
- a secrets.py with openai_key and novelai_key (depending on which one(s) you wanna use)
- package installs:
    - (for getting snippets) wikipedia https://github.com/goldsmith/Wikipedia
    - (for getting snippets) wikipediaapi https://github.com/martin-majlis/Wikipedia-API
    - (for novelai api call) requests https://pypi.org/project/requests/
    - (for openai api call) openai https://github.com/openai/openai-python