import os
import json
from openai import OpenAI
from typing import Dict, Any, Optional
from config.settings import OPENROUTER_API_KEY, HAIKU_MODEL, SONNET_MODEL

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def call_claude(prompt: str, system_prompt: str = "", model: str = HAIKU_MODEL, max_tokens: int = 4096) -> str:
    """Wrapper for OpenRouter/OpenAI API calls."""
    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM (OpenRouter): {e}")
        return ""

def parse_json_response(response: str) -> Dict[str, Any]:
    """Extract and parse JSON from Claude's response."""
    try:
        # Try direct parse
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to find JSON block
        import re
        match = re.search(r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {}
