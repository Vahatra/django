from config import celery_app
from django.core.mail import send_mail


@celery_app.task()
def send_email_task(subject: str, message: str, recipient_list: list[str]):
    """A very simple send_email function."""

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return {"msg": "Email sent successfully"}
