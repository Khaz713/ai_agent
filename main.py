import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import time
from datetime import datetime
from call_function import available_functions, call_function
from log import append_log, get_used_prompt_tokens, get_log
from prompts import system_prompt



def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    verbose = True if '--verbose' in sys.argv else False
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    start = time.time()
    conversation_start = datetime.now().strftime("%d %H:%M:%S")
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )
    end = time.time()
    response_time = end - start

    append_log(sys.argv[1], response, conversation_start, response_time)
    tokens_used = get_used_prompt_tokens(get_log())
    if verbose:
        print(f"User prompt: {sys.argv[1]}\n"
              f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
              f"Response tokens: {response.usage_metadata.candidates_token_count}\n"
              f"Tokens used this month: {tokens_used}\n")
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Function call failed")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                function_call_result = call_function(function_call_part, False)

    else:
        print(f"Response:\n {response.text}")



if __name__ == "__main__":
    main()
