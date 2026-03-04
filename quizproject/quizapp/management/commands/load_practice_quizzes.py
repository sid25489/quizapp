from django.core.management.base import BaseCommand

from quizapp.loaders import load_practice_quizzes


class Command(BaseCommand):
    help = "Load practice quizzes: Cricket and 10 other topics (10 questions each)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace existing practice quizzes with fresh data",
        )

    def handle(self, *args, **options):
        replace = options.get("replace", False)
        created_count, question_count = load_practice_quizzes(replace=replace)
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created {created_count} new quiz(zes). Total questions processed: {question_count}."
            )
        )
