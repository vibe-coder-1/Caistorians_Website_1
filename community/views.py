from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from decimal import Decimal

from .models import Photo, Story, StoryAccess
from .forms import PhotoUploadForm, StoryForm
from fundraisers.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

# ----------------------- PHOTOS -----------------------

@login_required
def upload_photo(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            if request.user.is_staff or request.user.is_superuser:
                photo.approved = True
            photo.save()
            return redirect("community:gallery")
    else:
        form = PhotoUploadForm()
    return render(request, "community/upload_photo.html", {"form": form})

@login_required
def gallery_view(request):
    photos = Photo.objects.filter(school=request.user.school, approved=True).order_by("-uploaded_at")
    return render(request, "community/gallery.html", {"photos": photos})

@login_required
def gallery_photo_view(request):
    photo_id = request.GET.get("id")
    photos = Photo.objects.filter(school=request.user.school, approved=True, id=photo_id)
    photo = photos[0] if photos else None

    try:
        previous = Photo.objects.filter(school=request.user.school, approved=True, id=int(photo_id)-1)[0]
    except:
        previous = None

    try:
        next_photo = Photo.objects.filter(school=request.user.school, approved=True, id=int(photo_id)+1)[0]
    except:
        next_photo = None

    return render(request, "community/gallery_photo_view.html", {
        "photo": photo,
        "previous": previous,
        "next": next_photo
    })

@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user != photo.uploaded_by and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this photo.")
    if request.method == "POST":
        photo.delete()
        return redirect("community:gallery")
    return render(request, "community/confirm_delete.html", {"object": photo, "type": "photo"})

# ----------------------- STORIES -----------------------

@login_required
def submit_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.school = request.user.school
            # New fields
            story.price = form.cleaned_data.get("price")
            story.is_magazine = form.cleaned_data.get("is_magazine")
            story.thumbnail = form.cleaned_data.get("thumbnail")
            story.save()
            return redirect("community:story_list")
    else:
        form = StoryForm()
    return render(request, "community/submit_story.html", {"form": form})

@login_required
def story_list(request):
    stories = Story.objects.filter(school=request.user.school, approved=True).order_by("-created_at")
    return render(request, "community/story_list.html", {"stories": stories})

@login_required
def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.user != story.author and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this story.")
    if request.method == "POST":
        story.delete()
        return redirect("community:story_list")
    return render(request, "community/confirm_delete.html", {"object": story, "type": "story"})

@login_required
def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    # Check access
    has_access = StoryAccess.objects.filter(user=request.user, story=story).exists()
    pdf_file = story.pdf_file.url if story.pdf_file else None
    text_content = story.text_content if not story.pdf_file else None

    return render(request, "community/story_detail.html", {
        "story": story,
        "has_access": has_access,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
        "pdf_file": pdf_file,
        "text_content": text_content,
    })

# ----------------------- STRIPE PAYMENTS -----------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from decimal import Decimal
import stripe

from .models import Story, StoryAccess

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

# ---------------- STRIPE PAYMENTS ---------------- #



@csrf_exempt
@login_required
def create_story_checkout_session(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    # Prevent free or invalid purchases
    if not story.price or story.price <= 0:
        return redirect('community:story_detail', story_id=story.id)

    # Prevent duplicate purchases
    if StoryAccess.objects.filter(user=request.user, story=story).exists():
        return redirect('community:story_detail', story_id=story.id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {'name': story.title},
                'unit_amount': int(story.price * 100),
            },
            'quantity': 1,
        }],
        success_url=request.build_absolute_uri(
            reverse('community:story_success', kwargs={'story_id': story.id})
        ),
        cancel_url=request.build_absolute_uri(
            reverse('community:story_cancel', kwargs={'story_id': story.id})
        ),
        customer_email=request.user.email,
        metadata={
            'story_id': str(story.id),
            'user_id': str(request.user.id),
            'payment_type': 'story',
        }
    )

    return redirect(session.url)


from fundraisers.models import Fundraiser
from decimal import Decimal

@csrf_exempt
def stripe_webhook(request):
 
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] != 'checkout.session.completed':
        return HttpResponse(status=200)

    session = event['data']['object']
    metadata = session.get('metadata', {})
    payment_type = metadata.get('payment_type')

    # ---------------- STORY PAYMENT ----------------
    if payment_type == 'story':
        user_id = metadata.get('user_id')
        story_id = metadata.get('story_id')
        payment_intent = session.get('payment_intent')

        if not all([user_id, story_id, payment_intent]):
            return HttpResponse(status=200)

        try:
            user = User.objects.get(pk=user_id)
            story = Story.objects.get(pk=story_id)
        except (User.DoesNotExist, Story.DoesNotExist):
            return HttpResponse(status=200)

        StoryAccess.objects.get_or_create(
            user=user,
            story=story,
            defaults={'stripe_payment_intent': payment_intent}
        )

    # ---------------- FUNDRAISER PAYMENT ----------------
    elif payment_type == 'fundraiser':
        fundraiser_id = metadata.get('fundraiser_id')

        if not fundraiser_id:
            return HttpResponse(status=200)

        try:
            fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
        except Fundraiser.DoesNotExist:
            return HttpResponse(status=200)

        amount_paid = Decimal(session['amount_total']) / Decimal('100')
        fundraiser.total_raised += amount_paid
        fundraiser.save()

    return HttpResponse(status=200)

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except (ValueError, stripe.error.SignatureVerificationError):
#         return HttpResponse(status=400)

#     # Only care about completed checkout sessions
#     if event['type'] != 'checkout.session.completed':
#         return HttpResponse(status=200)

#     session = event['data']['object']
#     metadata = session.get('metadata', {})

#     # Ignore non-story payments
#     if metadata.get('payment_type') != 'story':
#         return HttpResponse(status=200)

#     user_id = metadata.get('user_id')
#     story_id = metadata.get('story_id')
#     payment_intent = session.get('payment_intent')

#     if not all([user_id, story_id, payment_intent]):
#         return HttpResponse(status=200)

#     try:
#         user = User.objects.get(pk=user_id)
#         story = Story.objects.get(pk=story_id)
#     except (User.DoesNotExist, Story.DoesNotExist):
#         return HttpResponse(status=200)

#     # Idempotent write
#     StoryAccess.objects.get_or_create(
#         user=user,
#         story=story,
#         defaults={
#             'stripe_payment_intent': payment_intent
#         }
#     )

#     return HttpResponse(status=200)


@login_required
def story_success(request, story_id):
    """
    After successful payment, redirect to story_detail.
    """
    return redirect('community:story_detail', story_id=story_id)


@login_required
def story_cancel(request, story_id):
    """
    Display a cancel page if payment is cancelled.
    """
    story = get_object_or_404(Story, id=story_id)
    return render(request, 'community/story_cancel.html', {'story': story})


@login_required
def story_detail(request, story_id):
    """
    Show story content only if user has access or is author/staff.
    """
    story = get_object_or_404(Story, id=story_id)

    # Check if user has access
    has_paid = StoryAccess.objects.filter(user=request.user, story=story).exists()

    context = {
        'story': story,
        'has_paid': has_paid,
        'user': request.user,
    }

    return render(request, 'community/story_detail.html', context)
