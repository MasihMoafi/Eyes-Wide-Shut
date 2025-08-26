#Disable Proxy

import os

def clear_proxy_settings():
    for var in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]:
        if var in os.environ:
            del os.environ[var]

clear_proxy_settings()


from ollama import chat

# Model configurations
LLM_MODEL = 'gpt-oss:20b'

def generate_response(prompt):
    """Generate response using specified LLM model"""
    response = chat(model=LLM_MODEL, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

# Example usage
if __name__ == "__main__":
    response = generate_response("Hello, how are you?")
    print(response) 


     
