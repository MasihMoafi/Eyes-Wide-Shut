import os

def clear_proxy_settings():
    for var in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]:
        if var in os.environ:
            del os.environ[var]

clear_proxy_settings()

import ollama
from typing import Iterator
from ollama._types import ChatResponse

def run_model_with_prompt(system_prompt: str, user_input: str, model_name: str = 'gpt-oss:20b', temperature: float = 1.0):
    """Run the model with given prompts and return both thinking and response"""
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_input}
    ]
    
    response_stream: Iterator[ChatResponse] = ollama.chat(
        model=model_name, 
        messages=messages,
        stream=True,
        think=True,
        options={'temperature': temperature}
    )
    
    thinking = ""
    response = ""
    
    for chunk in response_stream:
        if chunk.message.thinking:
            thinking += chunk.message.thinking
        if chunk.message.content:
            response += chunk.message.content
    
    return thinking, response

def display_result(thinking: str, response: str, title: str = "Model Output"):
    """Display thinking and response in formatted output"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")
    
    if thinking:
        print(f"\n💭 Chain of Thought:")
        print(f"{'-'*40}")
        print(thinking)
    
    print(f"\n✨ Response:")
    print(f"{'-'*40}")
    print(response)
    print(f"{'='*60}\n")

if __name__ == "__main__":
    print("🔥 GPT-OSS-20B Model Runner")
    print("="*40)
    print("This script provides the model loading functionality for all experiments.")
    print("Import this module in your experiment scripts to run the model.")
    print("="*40)