try:
    from django.shortcuts import render, get_object_or_404, redirect
    from django.contrib.auth.decorators import login_required, user_passes_test
    from django.contrib import messages
    from Accounts.models import User
    from events.models import Event
    from community.models import Photo, Story
    from .models import AdminLog, Report
    from django.db.models import Q
    from interactions.models import Message
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")
    print("\nOr models not available.\n")

def staff_required(user):
    if user.is_staff or user.is_superuser:
        answer = True
    else:
        answer = False
    return answer

@login_required
@user_passes_test(staff_required)
def dashboard(request):
    search_query = request.GET.get('search', '')
       
    users = User.objects.filter(school=request.user.school)


    if request.user.school:
        users = User.objects.filter(school=request.user.school)
    else:
        users = User.objects.all()

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    events = Event.objects.filter(school=request.user.school)
    photos = Photo.objects.filter(school=request.user.school)
    stories = Story.objects.filter(school=request.user.school)
    reports = Report.objects.filter(school=request.user.school, resolved=False)
    chat_logs = Message.objects.filter(
        Q(sender__school=request.user.school) | Q(recipient__school=request.user.school),
        Q(sender__is_staff=False) | Q(recipient__is_staff=False)
    )
    logs = AdminLog.objects.filter(school=request.user.school).order_by('-created_at')[:50]  # last 50 actions

    return render(request, "custom_admin/dashboard.html", {
        "users": users,
        "events": events,
        "photos": photos,
        "stories": stories,
        "reports": reports,
        "logs": logs,
        "search_query": search_query,
        "chat_logs": chat_logs,
    })

# ------------------------
# User management
# ------------------------
@login_required
@user_passes_test(staff_required)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user:
        if user.profile_picture:
            user.profile_picture.delete(save=False)
    user.delete()
    messages.success(request, "User deleted")
    AdminLog.objects.create(admin=request.user, action=f"Deleted user {user.username}", school=user.school)
    return redirect("custom_admin:dashboard")

# ------------------------
# Event management
# ------------------------
@login_required
@user_passes_test(staff_required)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted")
    AdminLog.objects.create(admin=request.user, action=f"Deleted event {event.title}", school=request.user.school)
    return redirect("custom_admin:dashboard")

@login_required
@user_passes_test(staff_required)
def approve_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.approved = True
    event.save()
    messages.success(request, "Event approved")
    AdminLog.objects.create(
        admin=request.user,
        action=f"Approved event {event.title}",
        school=request.user.school
    )
    return redirect("custom_admin:dashboard")


# ------------------------
# Photo moderation
# ------------------------
@login_required
@user_passes_test(staff_required)
def approve_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    photo.approved = True
    photo.save()
    messages.success(request, "Photo approved")
    AdminLog.objects.create(admin=request.user, action=f"Approved photo {photo.caption}", school=request.user.school)
    return redirect("custom_admin:dashboard")

@login_required
@user_passes_test(staff_required)
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if photo:
        photo.image.delete(save=False)
    photo.delete()
    messages.success(request, "Photo deleted")
    AdminLog.objects.create(admin=request.user, action=f"Deleted photo {photo.caption}", school=request.user.school)
    return redirect("custom_admin:dashboard")

# ------------------------
# Story moderation
# ------------------------
@login_required
@user_passes_test(staff_required)
def approve_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    story.approved = True
    story.save()
    messages.success(request, "Story approved")
    AdminLog.objects.create(admin=request.user, action=f"Approved story {story.title}", school=request.user.school)
    return redirect("custom_admin:dashboard")

@login_required
@user_passes_test(staff_required)
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if story:
        if story.pdf_file:
            story.pdf_file.delete(save=False)
    story.delete()
    messages.success(request, "Story deleted")
    AdminLog.objects.create(admin=request.user, action=f"Deleted story {story.title}", school=request.user.school)
    return redirect("custom_admin:dashboard")

# ------------------------
# Reporting actions
# ------------------------
@login_required
@user_passes_test(staff_required)
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.resolved = True
    report.save()
    messages.success(request, "Report marked as resolved")
    AdminLog.objects.create(admin=request.user, action=f"Resolved report #{report.id}", school=request.user.school)
    return redirect("custom_admin:dashboard")

