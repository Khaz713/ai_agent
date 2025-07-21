from google import genai
import json
from datetime import datetime
import os

def get_date_key():
    now = datetime.now()
    return f"{now.year}-{now.month:02d}"

def get_log():
    with open('log.json', 'r', encoding='utf-8') as f:
        if os.path.getsize('log.json') == 0:
            return {get_date_key(): {}}
        return json.load(f)


def append_log(prompt, response, conversation_start, response_time):
    log = get_log()
    with open('log.json', 'w', encoding='utf-8') as f:
        if log[get_date_key()].get(conversation_start) is None:
            log[get_date_key()][conversation_start] = []
        log[get_date_key()][conversation_start].append({
            'prompt': prompt,
            'response': response.text,
            'prompt_tokens': response.usage_metadata.prompt_token_count,
            'response_tokens': response.usage_metadata.candidates_token_count,
            'response_time': response_time
        })
        json.dump(log, f, indent=4, ensure_ascii=False)

def get_used_prompt_tokens(log):
    used_prompt_tokens = 0
    date_key = get_date_key()
    for conversation in log[date_key].keys():
        for content in log[date_key][conversation]:
            used_prompt_tokens += content['prompt_tokens'] + content['response_tokens']
    return used_prompt_tokens