import ollama

def call_llm(prompt: str, model: str = "deepseek-r1:latest", temp: float = 0.7) -> str:
    response = ollama.generate(
        model=model,
        prompt=prompt,
        options={"temperature": temp}
    )
    print(response['response'].strip())
    return response['response'].strip()

# import requests

# def call_llm(prompt: str, model: str = "deepseek-r1:latest", temp: float = 0.7) -> str:
#     """
#     Cloud-based version of local Ollama call_llm function using OpenRouter API.
#     The structure and parsing match the local implementation for consistency.
#     """
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": "Bearer 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",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": model,
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": temp
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()

#         # Simulate Ollama’s structure for compatibility with local parsing
#         api_response = response.json()
#         result_text = api_response["choices"][0]["message"]["content"].strip()
        
#         # Create a similar structure as Ollama's output
#         response_data = {
#             "response": result_text
#         }

#         # Matching Ollama’s local behavior
#         print(response_data["response"])
#         return response_data["response"]

#     except requests.exceptions.RequestException as e:
#         raise Exception(f"OpenRouter API request failed: {e}")
#     except (KeyError, IndexError) as e:
#         raise Exception(f"Unexpected response structure: {e}\nFull response: {response.text}")




#openrouter_api_key=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
#https://openrouter.ai/api/v1/keys