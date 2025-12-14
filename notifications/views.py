from django.shortcuts import render
from .models import Notification, UserNotification

def notifications_list(request):
    # School-wide notifications
    # Only include notifications linked to approved events
    school_notes = Notification.objects.filter(
        school=request.user.school
    ).exclude(
        event__approved=False  # exclude notifications tied to unapproved events
    )

    # Individual notifications (school=None)
    individual_notes = Notification.objects.filter(
        school__isnull=True,
        user_states__user=request.user
    )

    # Merge and exclude deleted notifications for this user
    user_states = UserNotification.objects.filter(user=request.user)
    deleted_ids = [state.notification.id for state in user_states if state.deleted]

    all_notifications = list(school_notes) + list(individual_notes)
    all_notifications = [n for n in all_notifications if n.id not in deleted_ids]

    # Sort by creation date descending
    all_notifications.sort(key=lambda x: x.created_at, reverse=True)

    context = {
        'notifications': all_notifications,
        'user_states': {state.notification.id: state for state in user_states}
    }
    return render(request, 'notifications/notifications_list.html', context)
