#!/usr/bin/env python3
import os
import json
import urllib.request

api_key = os.environ.get("OPENROUTER_API_KEY")
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/auth/key",
    headers={"Authorization": f"Bearer {api_key}"}
)

with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode("utf-8"))["data"]

try:
    req_cred = urllib.request.Request(
        "https://openrouter.ai/api/v1/credits",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    with urllib.request.urlopen(req_cred, timeout=10) as resp_c:
        cred_data = json.loads(resp_c.read().decode("utf-8"))["data"]
        total_cred = cred_data.get("total_credits", 0)
        total_used = cred_data.get("total_usage", 0)
        print(f"Total Deposited: ${total_cred:.2f}")
        print(f"Total Lifetime Usage: ${total_used:.4f}")
        print(f"Current Available Balance: ${total_cred - total_used:.4f}")
except Exception as err:
    print(f"Credits query fallback: {err}")
