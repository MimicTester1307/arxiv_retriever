import os
from anthropic import Anthropic

from dotenv import load_dotenv

# load environment variables
load_dotenv()


def get_llm_response(prompt: str) -> str:
    """Prompt Claude 3.5 Sonnet for a response"""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0,
        system="You are a helpful AI assistant specializing in summarizing scientific papers, extracting the most "
               "meaningful parts of the paper.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text
