import os
import json
import anthropic
from typing import Dict, Any, Optional
from config.settings import ANTHROPIC_API_KEY, HAIKU_MODEL, SONNET_MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def call_claude(prompt: str, system_prompt: str = "", model: str = HAIKU_MODEL, max_tokens: int = 4096) -> str:
    """Wrapper for Anthropic API calls."""
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error calling Claude: {e}")
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
