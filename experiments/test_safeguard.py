#!/usr/bin/env python3
import os
import json
import urllib.request

api_key = os.environ.get("OPENROUTER_API_KEY")
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps({
        "model": "openai/gpt-oss-safeguard-20b",
        "messages": [{"role": "user", "content": "State your model identity in one brief sentence."}],
        "max_tokens": 50
    }).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/MasihMoafi/eyes-wide-shut",
    }
)

with urllib.request.urlopen(req, timeout=20) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    print("SUCCESS! Response from openai/gpt-oss-safeguard-20b:")
    print(res["choices"][0]["message"])
