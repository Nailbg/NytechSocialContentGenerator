import json
from openai import OpenAI

client = OpenAI()

with open("inputs/inspiration.txt", "r") as f:
    caption = f.read()

with open("prompts/analyze_inspiration.txt", "r") as f:
    prompt = f.read().replace("{{CAPTION}}", caption)

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "You output ONLY valid JSON."},
        {"role": "user", "content": prompt}
    ]
)

analysis = response.choices[0].message.content

with open("outputs/analysis.json", "w") as f:
    f.write(analysis)

print("Analysis complete.")
