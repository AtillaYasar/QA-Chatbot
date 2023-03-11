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
    - (for novelai api call) requests https://pypi.org/project/requests/
    - (for openai api call) openai https://github.com/openai/openai-python

# thoughts/notes
It is runnable in its current form, api's it uses:
- openai's codex, 3.5-turbo, or novelai's api (set to the finetuned 20B model but you do need Opus to use that one) to generate answer a question.
- I feel like the hardest part of this are still ahead of me: finding good text snippets, ranking them, and assembling them into an AI input
- for the "get snippets" part:
    + i played a bit with getting info from wikipedia https://github.com/AtillaYasar/random-collection-of-things/blob/main/wiki_poc.py
    + for ranking snippets, i know 2 apis: the openai api which i played with a bit and is easy to use, and https://github.com/different-ai/embedbase which also uses openai afaik.
