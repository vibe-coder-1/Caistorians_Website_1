from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import GroupChatRoom, GroupMessage

@login_required
def redirect_to_chat(request):
    """Redirect user to their cohort chat"""
    year = getattr(request.user, 'graduation_year', None)
    if not year:
        return render(request, 'chat/error.html', {'message': 'Graduation year not set.'})
    return redirect('chat:cohort_chat', cohort_year=year)


@login_required
def cohort_chat_view(request, cohort_year):
    """Render chat page for a given cohort"""
    # Fetch or create the cohort room
    room, created = GroupChatRoom.objects.get_or_create(cohort_year=cohort_year)

    # Load last 100 messages and select sender to reduce queries
    messages = GroupMessage.objects.filter(room=room).select_related('sender').order_by('sent_at')[:100]

    return render(request, 'chat/cohort_chat.html', {
        'room': room,
        'messages': messages,
    })
