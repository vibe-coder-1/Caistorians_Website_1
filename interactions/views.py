from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Message
from .forms import MessageForm
from notifications.utils import create_notification
#Create your views here.

@login_required
def inbox_view(request):
    messages = request.user.received_messages.all()
    return render(request, "interactions/inbox.html", {"messages": messages})

@login_required
def outbox_view(request):
    messages = request.user.sent_messages.all()
    return render(request, "interactions/outbox.html", {"messages": messages})

@login_required
def message_detail_view(request, pk):
    message = get_object_or_404(Message, pk=pk)

    # Only the sender or recipient can view it
    if request.user != message.recipient and request.user != message.sender:
        return redirect("interactions:inbox")

    # Mark as read only if recipient is opening it
    if request.user == message.recipient:
        message.is_read = True
        message.save()

    return render(request, "interactions/message_detail.html", {"message": message})

@login_required
def compose_view(request):
    initial_data = {}
    to_user = request.GET.get("to")
    subject = request.GET.get("subject")

    if to_user:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            initial_data["recipient"] = User.objects.filter(school=request.user.school).get(username=to_user)
        except User.DoesNotExist:
            pass

    if subject:
        initial_data["subject"] = f"Re: {subject}"

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()

            # Send notification and HTML email
            create_notification(
                title="New Message",
                message=f"You got a new message from {request.user.username}",
                users=[msg.recipient],
                link=reverse("interactions:detail", args=[msg.id]),
                send_email=True,
                request=request  # needed to build full URL in the email
            )

            return redirect("interactions:outbox")
    else:
        form = MessageForm(initial=initial_data)

    return render(request, "interactions/compose.html", {"form": form})
