import requests
import json
import time

class AIInterface:
    def __init__(self, model_name="llama3:8b"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"

    def send_message(self, message):
        """Send a message to Ollama and get response"""

        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model_name,
            "prompt": message,
            "stream": False
        }

        for attempt in range(3): 
            try:
                response = requests.post(url, json=payload)
                # print(f"Response Status Code: {response.status_code}") # Debug
                response.raise_for_status()

                result = response.json()

                # Check if model is still loading
                if result.get("done_reason") == "load":
                    # print(f"Model is still loading... (attempt {attempt + 1})") # Debug
                    time.sleep(2) # Wait before retrying
                    continue

                # print(f"full JSON response: {result}") # Debug 
                return result["response"]
            
            except requests.RequestException as e:
                return f"Error communicating with Ollama: {e}"
            
        return "Failed to get response after multiple attempts."