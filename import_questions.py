import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from quiz.models import Question

FILE_NAME = "c_medium_200.json"

with open(FILE_NAME, "r", encoding="utf-8") as file:
    data = json.load(file)

count = 0

for item in data:
    Question.objects.create(
        domain="c",
        level="medium",
        question_text=item["question_text"],
        option1=item["option1"],
        option2=item["option2"],
        option3=item["option3"],
        option4=item["option4"],
        correct_answer=item["correct_answer"]
    )
    count += 1

print(f"✅ {count} Questions Inserted Successfully!")