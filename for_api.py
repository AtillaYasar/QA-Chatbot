"""This is step 3/3 for the Q&A algorithm: make an api call to answer the question.

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

openai.api_key = openai_key
def get_api_caller(provider):
    """Returns the function that you can use to call an api."""

    layer_n = 1
    location = 'api'
    show_layer(layer_n, [f'get {location} getter', f'provider:{provider}'])

    def codex_completion(prompt):
        settings = {
            'engine':'code-davinci-002',
            'prompt':prompt,
            'temperature':0.3,
            'max_tokens':50,
            'n':1,
            'stop':None
            }
        completions = openai.Completion.create(**settings)
        print(col('re', f'actual settings used:{settings}'))
        print(col('re', f'actual api completions object:{completions}'))

        responses = [choice['text'] for choice in completions.choices]
        return responses[0]
    
    def novelai_completion(prompt):
        secret_authorization_key = novelai_key
        headers = {'Content-Type': 'application/json',
                'authorization': f'Bearer {secret_authorization_key}'
                }
        payload = {
            "input": prompt,
            "model": "krake-v2", #2.7B, 6B-v4, euterpe-v2, krake-v2
            "parameters":{
                "use_string":True,
                "prefix":"style_hplovecraft", # or vanilla for no module. find more at https://github.com/wbrown/novelai-research-tool
                "temperature":1,
                "max_length":100,
                "min_length":1
                }
            }
        url = "https://api.novelai.net/ai/generate"
        response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        content = response.content

        decodedContent = content.decode()
        decodedContent = decodedContent.replace("null", "0.0000")
        stringified = ast.literal_eval(decodedContent)
        output = stringified["output"]

        if 'logprobs' in stringified:
            logprobs = stringified["logprobs"]
        
        return output
    
    def turbo_completion(messages):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()['choices'][0]

    if provider == 'novelai':
        caller = novelai_completion
    elif provider == 'codex':
        caller = codex_completion
    elif provider == 'turbo':
        caller = turbo_completion
    else:
        raise ValueError('only novelai and codex as provider')

    info = {
        'description':provider,
    }
    to_return = (
        caller,
        info,
    )
    check_return(to_return)
    return to_return