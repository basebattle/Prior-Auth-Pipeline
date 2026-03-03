import os
import json
import traceback
from openai import OpenAI
from typing import Dict, Any, Optional
from config.settings import GEMINI_API_KEY, HAIKU_MODEL, SONNET_MODEL

# Initialize OpenAI client with Gemini base URL
try:
    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=GEMINI_API_KEY,
    )
except Exception as e:
    print(f"CRITICAL: Failed to initialize OpenAI client for Gemini: {e}")
    client = None

def call_claude(prompt: str, system_prompt: str = "", model: str = HAIKU_MODEL, max_tokens: int = 4096) -> str:
    """Wrapper for Gemini API calls via OpenAI compatibility layer."""
    if not client:
        print("ERROR: OpenAI client not initialized.")
        return ""
        
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
        print(f"ERROR: LLM call failed (Gemini): {e}")
        # traceback.print_exc()
        return ""

def parse_json_response(response: str) -> Dict[str, Any]:
    """Extract and parse JSON from Claude's response."""
    if not response:
        return {}
        
    try:
        # Try direct parse
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to find JSON block using regex
        import re
        # Look for the last JSON object in the string to avoid prologues
        matches = re.findall(r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}', response, re.DOTALL)
        if matches:
            try:
                # Use the last match which is usually the intended JSON response
                return json.loads(matches[-1])
            except json.JSONDecodeError:
                pass
    return {}
