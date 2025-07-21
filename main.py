import os
from dotenv import load_dotenv
from google import genai
import sys
import time

from log import append_log, get_used_prompt_tokens, get_log


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    start = time.time()
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=sys.argv[1])
    end = time.time()
    response_time = end - start
    append_log(sys.argv[1], response, response_time)
    tokens_used = get_used_prompt_tokens(get_log())
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
          f"Response tokens: {response.usage_metadata.candidates_token_count}\n"
          f"Tokens used this month: {tokens_used}\n"
          f"Response:\n {response.text}")


if __name__ == "__main__":
    main()
