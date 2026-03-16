from core.notifier import EmailNotifier


def get_email_notifier() -> EmailNotifier:
    return EmailNotifier()
