It is runnable in its current form, though you do need secrets.py with an openai and novelai key. (I should change that to only require a key the moment you actually want to use an API)

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
    - (for novelai and openai api call) requests https://pypi.org/project/requests/
    - (for openai api call) openai https://github.com/openai/openai-python

# thoughts/notes
The idea is that it's modular, and you can use different algorithms for doing any of the 3 different things.

## for the "get snippets" part:
- i played a bit with getting info from wikipedia https://github.com/AtillaYasar/random-collection-of-things/blob/main/wiki_poc.py, should be promising
- for ranking snippets, i know 2 apis: the openai api for embeddings (and then doing cosine similarity) which i played with a bit and is easy to use, and https://github.com/different-ai/embedbase which last time I looked, used the openai api
- scraping is an option
    + (in general, you can get snippets either "at runtime" or beforehand, by collecting a big database of embedded text, and/or using a pre-existing one.)

## assembling context
- probably very finicky, the solution here is to make the stuff around context creation very tinkerable, so that it can be done by the end user "at runtime", instead of attempting to hardcode anything.
    + at best we could provide some templates/suggestions.

## For generating a response:
- openai's codex, 3.5-turbo, or novelai's api (set to the finetuned 20B model but you do need Opus to use that one) to generate answer a question.
- I feel like the hardest part of this are still ahead of me: finding good text snippets, ranking them, and assembling them into an AI input

# screeeshots
- with gpt turbo
- ![Schermopname (5)](https://user-images.githubusercontent.com/112716905/224482529-6d6533fa-e5ad-4bea-9d1e-24c5d54b4140.png)
- with krake, a neox-20b model finetuned by NovelAI on stories, also i used a soft prompt trained on HP Lovecraft. not well suited for this lol. (why the Lovecraft module? idk. why not.)
- ![Schermopname (6)](https://user-images.githubusercontent.com/112716905/224482565-a7f838b4-126f-4cd7-8d48-5ccf0dbefa8f.png)



( sorry i cant find a proper screenshot tool)

# misc
```
"just use google bro"
no, google searches over articles not snippets, also it doesnt talk to you, also ads and search-engine optimizations are super annoying

"just use bing bro"
the bing interface is ugly af, also i dont have access

in general, i just dont care if this exists or is obsolete, it just felt cool to make :p  especially on a whim.
```
