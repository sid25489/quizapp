from django.apps import AppConfig


class QuizappConfig(AppConfig):
    name = 'quizapp'

    def ready(self):
        from django.db.models.signals import post_migrate

        def on_migrate(sender, **kwargs):
            if sender.name == 'quizapp':
                try:
                    from quizapp.loaders import load_practice_quizzes
                    load_practice_quizzes()
                except Exception:
                    pass

        post_migrate.connect(on_migrate, sender=self)
