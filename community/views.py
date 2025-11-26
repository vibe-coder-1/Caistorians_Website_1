from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Photo, Story
from .forms import PhotoUploadForm, StoryForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from fundraisers.models import *
from Website import settings
# --- Photos ---
@login_required
def upload_photo(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()
            return redirect("community:gallery")
    else:
        form = PhotoUploadForm()
    return render(request, "community/upload_photo.html", {"form": form})

def gallery_view(request):
    photos = Photo.objects.filter(school=request.user.school, approved=True).order_by("-uploaded_at")
    #photos = Photo.objects.order_by("-uploaded_at")  ------For testing purposes, show unapproved photos too
    return render(request, "community/gallery.html", {"photos": photos})


# --- Delete Photo ---
@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user != photo.uploaded_by and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this photo.")
    if request.method == "POST":
        photo.delete()
        return redirect("community:gallery")
    return render(request, "community/confirm_delete.html", {"object": photo, "type": "photo"})

# --- Delete Story ---
@login_required
def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.user != story.author and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this story.")
    if request.method == "POST":
        story.delete()
        return redirect("community:story_list")
    return render(request, "community/confirm_delete.html", {"object": story, "type": "story"})

# --- Stories ---
@login_required
def submit_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.school = request.user.school  # match your existing photo logic
            story.save()
            return redirect("community:story_list")
    else:
        form = StoryForm()
    return render(request, "community/submit_story.html", {"form": form})

def story_list(request):
    stories = Story.objects.filter(school=request.user.school, approved=True).order_by("-created_at")
    #stories = Story.objects.order_by("-created_at") -----For testing purposes, show unapproved stories too
    return render(request, "community/story_list.html", {"stories": stories})
from django.http import FileResponse
@login_required
def story_detail(request, pk):
    story = get_object_or_404(Story, id=pk)
    print(story.content)
    if story.pdf_file:
        pdf = story.pdf_file.url
    else:
        pdf = story.text_content
    record = UnlockStories.objects.filter(user=request.user).first()
    has_paid = record is not None and record.paid
    return render(request, 'community/story_detail.html', {
        'story': story,
        'has_paid': has_paid,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
        'pdf': pdf,
    })


