import openai

client = openai.OpenAI(
    api_key="<sk-yuzgnijn1KdGLcDExLOMPPPpZZYkuIdfujrczFAY0I3UPtdG>",
    base_url="https://playground.opentyphoon.ai/"
)

response = client.chat.completions.create(
    model="typhoon-v2.5-30b-a3b-instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that translates English to Thai."},
        {"role": "user", "content": "Translate the following: Hello, how are you?"}
    ],
    temperature=0.7,
    max_tokens=256
)

print(response.choices[0].message.content)