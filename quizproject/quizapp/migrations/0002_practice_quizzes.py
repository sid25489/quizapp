from django.db import migrations


def create_practice_quizzes(apps, schema_editor):
    Quiz = apps.get_model("quizapp", "Quiz")
    Question = apps.get_model("quizapp", "Question")
    Choice = apps.get_model("quizapp", "Choice")

    data = [
        {
            "title": "Cricket Basics",
            "description": "Test your knowledge of international cricket, formats and records.",
            "time_limit": 8,
            "questions": [
                {
                    "text": "How many players are there in a cricket team on the field?",
                    "points": 1,
                    "choices": [
                        ("9", False),
                        ("10", False),
                        ("11", True),
                        ("12", False),
                    ],
                },
                {
                    "text": "Which country won the ICC Cricket World Cup 2019?",
                    "points": 1,
                    "choices": [
                        ("India", False),
                        ("England", True),
                        ("Australia", False),
                        ("New Zealand", False),
                    ],
                },
                {
                    "text": "What is the maximum number of overs per bowler in a standard ODI match?",
                    "points": 1,
                    "choices": [
                        ("5 overs", False),
                        ("8 overs", False),
                        ("10 overs", True),
                        ("12 overs", False),
                    ],
                },
            ],
        },
        {
            "title": "Football Essentials",
            "description": "Rules, clubs and legends from the world of football.",
            "time_limit": 8,
            "questions": [
                {
                    "text": "How long is a standard professional football match (excluding extra time)?",
                    "points": 1,
                    "choices": [
                        ("70 minutes", False),
                        ("80 minutes", False),
                        ("90 minutes", True),
                        ("100 minutes", False),
                    ],
                },
                {
                    "text": "Which country has won the most FIFA World Cups (senior men's) as of 2022?",
                    "points": 1,
                    "choices": [
                        ("Germany", False),
                        ("Brazil", True),
                        ("Argentina", False),
                        ("Italy", False),
                    ],
                },
                {
                    "text": "Which player is famous for spending most of his career at FC Barcelona wearing number 10?",
                    "points": 1,
                    "choices": [
                        ("Cristiano Ronaldo", False),
                        ("Lionel Messi", True),
                        ("Neymar Jr.", False),
                        ("Andrés Iniesta", False),
                    ],
                },
            ],
        },
        {
            "title": "Technology & Computing",
            "description": "Core concepts in modern technology, software and the internet.",
            "time_limit": 10,
            "questions": [
                {
                    "text": "What does 'HTTP' stand for?",
                    "points": 1,
                    "choices": [
                        ("HyperText Transfer Protocol", True),
                        ("HighText Transfer Protocol", False),
                        ("Hyperlink Text Transmission Process", False),
                        ("Hyper Transfer Text Program", False),
                    ],
                },
                {
                    "text": "Which company created the Windows operating system?",
                    "points": 1,
                    "choices": [
                        ("Apple", False),
                        ("Google", False),
                        ("Microsoft", True),
                        ("IBM", False),
                    ],
                },
                {
                    "text": "In computing, what does CPU stand for?",
                    "points": 1,
                    "choices": [
                        ("Central Processing Unit", True),
                        ("Core Programming Unit", False),
                        ("Central Performance Utility", False),
                        ("Control Processing Unit", False),
                    ],
                },
            ],
        },
        {
            "title": "Current Affairs (General)",
            "description": "Recent events in politics, economy and society (general awareness).",
            "time_limit": 10,
            "questions": [
                {
                    "text": "Which international organisation is headquartered in New York City, USA?",
                    "points": 1,
                    "choices": [
                        ("World Bank", False),
                        ("United Nations (UN)", True),
                        ("NATO", False),
                        ("European Union (EU)", False),
                    ],
                },
                {
                    "text": "Which term is commonly used for unexpected and rapid increase in general price levels?",
                    "points": 1,
                    "choices": [
                        ("Deflation", False),
                        ("Stagnation", False),
                        ("Inflation", True),
                        ("Depression", False),
                    ],
                },
                {
                    "text": "Which global health crisis significantly impacted the world starting in 2019?",
                    "points": 1,
                    "choices": [
                        ("SARS", False),
                        ("COVID-19 pandemic", True),
                        ("Ebola outbreak", False),
                        ("Zika virus", False),
                    ],
                },
            ],
        },
        {
            "title": "Geopolitics & World Order",
            "description": "Countries, alliances and key concepts in global geopolitics.",
            "time_limit": 12,
            "questions": [
                {
                    "text": "NATO is primarily a treaty organisation for which purpose?",
                    "points": 1,
                    "choices": [
                        ("Economic cooperation", False),
                        ("Military and collective defence alliance", True),
                        ("Environmental protection", False),
                        ("Cultural exchange", False),
                    ],
                },
                {
                    "text": "Which two countries share the world's longest international land border?",
                    "points": 1,
                    "choices": [
                        ("India and China", False),
                        ("Russia and China", False),
                        ("United States and Canada", True),
                        ("Brazil and Argentina", False),
                    ],
                },
                {
                    "text": "The term 'Global South' is often used to describe:",
                    "points": 1,
                    "choices": [
                        ("High-income industrialised countries", False),
                        ("Low and middle-income countries in Asia, Africa and Latin America", True),
                        ("Countries only in the Southern Hemisphere", False),
                        ("European Union member states", False),
                    ],
                },
            ],
        },
    ]

    for quiz_data in data:
        quiz, created = Quiz.objects.get_or_create(
            title=quiz_data["title"],
            defaults={
                "description": quiz_data["description"],
                "time_limit": quiz_data["time_limit"],
                "is_active": True,
            },
        )
        if not created:
            continue

        for order, q in enumerate(quiz_data["questions"], start=1):
            question = Question.objects.create(
                quiz=quiz,
                text=q["text"],
                points=q["points"],
                order=order,
            )
            for text, is_correct in q["choices"]:
                Choice.objects.create(
                    question=question,
                    text=text,
                    is_correct=is_correct,
                )


def reverse_practice_quizzes(apps, schema_editor):
    Quiz = apps.get_model("quizapp", "Quiz")
    titles = [
        "Cricket Basics",
        "Football Essentials",
        "Technology & Computing",
        "Current Affairs (General)",
        "Geopolitics & World Order",
    ]
    Quiz.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("quizapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_practice_quizzes, reverse_practice_quizzes),
    ]

