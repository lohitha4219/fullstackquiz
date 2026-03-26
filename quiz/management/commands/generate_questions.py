from django.core.management.base import BaseCommand
from ...models import Question
import random

class Command(BaseCommand):
    help = "Generate quiz questions automatically"

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)
        parser.add_argument('level', type=str)
        parser.add_argument('count', type=int)

    def handle(self, *args, **kwargs):
        domain = kwargs['domain']
        level = kwargs['level']
        count = kwargs['count']

        for i in range(count):

            a = random.randint(1, 50)
            b = random.randint(1, 50)
            correct = a + b

            options = [
                correct,
                correct + random.randint(1, 10),
                correct - random.randint(1, 5),
                correct + random.randint(11, 20)
            ]

            random.shuffle(options)

            Question.objects.create(
                domain=domain,
                level=level,
                question_text=f"What is {a} + {b} ?",
                option1=str(options[0]),
                option2=str(options[1]),
                option3=str(options[2]),
                option4=str(options[3]),
                correct_answer=str(correct)
            )

        self.stdout.write(self.style.SUCCESS(f"{count} questions generated successfully!"))