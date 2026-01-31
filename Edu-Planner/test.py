from openai import OpenAI

api_key = "Open-router API key of the Deepseek"

# Initialize the client with custom timeout
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com/v1",
    timeout=120.0  
)

prompt = "Write a Python function to calculate factorial recursively."

model_name = "deepseek-reasoner"

response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

print(response.choices[0].message.content)
