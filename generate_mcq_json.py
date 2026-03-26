import json
import openai

# 🔴 Put your OpenAI API Key here
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ===== SETTINGS =====
DOMAIN = "C Language"
LEVEL = "Easy"
COUNT = 20  # Generate 20 at a time (repeat 10 times for 200)
# ====================

prompt = f"""
Generate {COUNT} multiple choice questions for {DOMAIN} ({LEVEL} level).

Rules:
- Questions must be original.
- Each question must contain:
    question_text
    option1
    option2
    option3
    option4
    correct_answer
- correct_answer must match exactly one option.
- Return ONLY valid JSON array.
"""

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
)

content = response["choices"][0]["message"]["content"]

try:
    data = json.loads(content)
except:
    print("⚠ AI did not return valid JSON. Please try again.")
    exit()

filename = f"{DOMAIN.replace(' ', '_').lower()}_{LEVEL.lower()}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"✅ File saved as {filename}")