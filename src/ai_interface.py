import requests
import json
import time
import os

class AIInterface:
    def __init__(self, model_name="pplx-70b-online", base_url="https://api.perplexity.ai"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise RuntimeError("Missing PERPLEXITY_API_KEY environment")
    
    def send_message(self, message, system="You are a creative D&D Dungeon Master. Keep responses concise and actionable."):
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": message}
            ]
        }

        backoff = 1.0
        for attempt in range(3): 
            try:
                print("Payload:", json.dumps(payload, indent=2)) # Debugging line to print the payload
                resp = requests.post(url, headers=headers, json=payload, timeout=60)
                if resp.status_code == 429:
                    time.sleep(backoff)
                    backoff *= 2
                    continue 
                resp.raise_for_status()
                result = resp.json()
                # Perplexity response format: choices[0].message.content
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            except requests.RequestException as e:
                if attempt == 2:
                    return f"Error communicating with Perplexity: {e}"
                time.sleep(backoff)
                backoff *= 2

        return "Failed to get response after multiple attempts."