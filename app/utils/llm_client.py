import requests
class LLMClient:
    def __init__(self, api_key):
        self._url = 'https://np6jbwtoaiv4y8cw.us-east4.gcp.endpoints.huggingface.cloud/v1/chat/completions'
        self._api_key = api_key

    def make_chat_completions_request(self, model, messages, temperature, max_tokens):
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        response = requests.post(self._url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()