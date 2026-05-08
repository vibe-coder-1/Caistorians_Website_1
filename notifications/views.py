try:
    from django.shortcuts import render
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

# Create your views here.
# notifications/views.py
try:
    from django.shortcuts import render, get_object_or_404, redirect
    from .models import Notification, UserNotification
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

def notifications_list(request):
    # school-wide notifications
    try:
        # Try to filter by approved if the field exists
        school_notes = Notification.objects.filter(school=request.user.school, approved=True)
    except Exception:
        # Fallback: just get all notifications for the school
        school_notes = Notification.objects.filter(school=request.user.school)

    individual_notes = Notification.objects.filter(school__isnull=True, user_states__user=request.user)

    # Merge and exclude deleted for this user
    user_states = UserNotification.objects.filter(user=request.user)
    deleted_ids = [state.notification.id for state in user_states if state.deleted]
    all_notifications = list(school_notes) + list(individual_notes)
    all_notifications = [n for n in all_notifications if n.id not in deleted_ids]
    all_notifications.sort(key=lambda x: x.created_at, reverse=True)

    context = {'notifications': all_notifications, 'user_states': {state.notification.id: state for state in user_states}}
    return render(request, 'notifications/notifications_list.html', context)

try:
    from django.shortcuts import get_object_or_404, redirect
    from .models import Notification
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.delete()
    return redirect("notifications:list")