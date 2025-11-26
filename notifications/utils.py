# notifications/utils.py
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import Notification, UserNotification

def create_notification(title, message, link=None, school=None, users=None, send_email=False, request=None):
    """
    Create a notification and optionally send an HTML email.
    - school: assign to a school (all users in that school)
    - users: list of User objects for individual notifications
    - send_email: send email to users if True
    - request: needed to generate full absolute URLs for links
    """
    # Create main notification
    note = Notification.objects.create(title=title, message=message, link=link, school=school)

    if users:
        for user in users:
            UserNotification.objects.create(user=user, notification=note)

            if send_email and user.email:
                # Use HTML template for the email
                html_content = render_to_string(
                    "notifications/emails/notification_email.html",  # add 'notifications/' at the start
                    {
                        "user": user,
                        "title": title,
                        "message": message,
                        "link": request.build_absolute_uri(link) if request and link else None,
                    }
                )
                email = EmailMessage(
                    subject=title,
                    body=html_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                email.content_subtype = "html"  # send HTML email
                email.send(fail_silently=True)

    return note
