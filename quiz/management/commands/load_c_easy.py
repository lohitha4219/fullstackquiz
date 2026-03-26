import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from quiz.models import Question


class Command(BaseCommand):
    help = "Load C Easy Questions from JSON"

    def handle(self, *args, **kwargs):

        file_path = os.path.join(settings.BASE_DIR, "python_hard_200.json")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        count = 0

        for item in data:

            # Convert correct answer text to option number
            if item["correct_answer"] == item["option1"]:
                correct_option = 1
            elif item["correct_answer"] == item["option2"]:
                correct_option = 2
            elif item["correct_answer"] == item["option3"]:
                correct_option = 3
            else:
                correct_option = 4

            Question.objects.create(
                domain="py",
                level="hard",
                question_text=item["question_text"],
                option1=item["option1"],
                option2=item["option2"],
                option3=item["option3"],
                option4=item["option4"],
                correct_answer=correct_option
            )

            count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} questions loaded successfully!"))