# fundraisers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import stripe
from notifications.utils import create_notification
from .models import *
from .forms import FundraiserForm
from decimal import Decimal
from django.contrib.auth import get_user_model
User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_fundraiser(request):
    if request.method == 'POST':
        form = FundraiserForm(request.POST)
        if form.is_valid():
            fundraiser = form.save(commit=False)
            fundraiser.creator = request.user
            create_notification(title="New Event", message="Check out the new fundraiser!", school=request.user.school)
            fundraiser.save()
            return redirect('fundraisers:fundraiser_detail', fundraiser.id)
    else:
        form = FundraiserForm()
    return render(request, 'fundraisers/create.html', {'form': form})

def fundraiser_list(request):
    fundraisers = Fundraiser.objects.all().order_by('-created_at')
    return render(request, 'fundraisers/list.html', {'fundraisers': fundraisers})

def fundraiser_detail(request, fundraiser_id):
    fundraiser = get_object_or_404(Fundraiser, id=fundraiser_id)
    return render(request, 'fundraisers/detail.html', {
        'fundraiser': fundraiser,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })

@csrf_exempt
@login_required
def create_checkout_session(request, fundraiser_id):
    fundraiser = get_object_or_404(Fundraiser, id=fundraiser_id)
    amount = int(request.POST.get('amount', 0))

    if amount <= 0:
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    mode='payment',
    line_items=[{
        'price_data': {
            'currency': 'gbp',
            'product_data': {'name': fundraiser.title},
            'unit_amount': amount * 100,
        },
        'quantity': 1,
    }],
    success_url=request.build_absolute_uri('/fundraisers/success/'),
    cancel_url=request.build_absolute_uri('/fundraisers/cancel/'),
    customer_email=request.user.email,
    metadata={
        'fundraiser_id': str(fundraiser.id),
        'user_id': str(request.user.id),
    }
    )

    return JsonResponse({'id': session.id})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session['metadata']
        print("SESSION METADATA:", session.get('metadata'))
        user = User.objects.get(pk=metadata['user_id'])
        payment_amount = Decimal(session['amount_total']) / Decimal('100')

        if metadata.get('payment_type') == 'story':
            from community.models import Story
            story = Story.objects.get(pk=metadata['story_id'])
            Payment.objects.create(
                story=story,
                user=user,
                amount=payment_amount,
                stripe_payment_intent=session['payment_intent']
            )
        else:
            fundraiser = Fundraiser.objects.get(pk=metadata['fundraiser_id'])
            Payment.objects.create(
                fundraiser=fundraiser,
                user=user,
                amount=payment_amount,
                stripe_payment_intent=session['payment_intent']
            )
            fundraiser.total_raised += payment_amount
            fundraiser.save()
        if payment_amount >= 2:
            yo = UnlockStories.objects.create(user=user, paid = True)
    return HttpResponse(status=200)

def success(request):
    return render(request, 'fundraisers/success.html')

def cancel(request):
    return render(request, 'fundraisers/cancel.html')


from community.models import *
@csrf_exempt
@login_required
def create_story_checkout_session(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    amount = story.price  # assume Story model has a `price` field

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {'name': story.title},
                'unit_amount': int(amount),
            },
            'quantity': 1,
        }],
        success_url=request.build_absolute_uri('/stories/success/'),
        cancel_url=request.build_absolute_uri('/stories/cancel/'),
        customer_email=request.user.email,
        metadata={
            'story_id': str(story.id),
            'user_id': str(request.user.id),
            'payment_type': 'story'
        }
    )

    return JsonResponse({'id': session.id})



def handle_checkout_success(session):
    """Mark payment as complete and grant access."""
    try:
        payment = Payment.objects.get(stripe_checkout_id=session.get('id'))
        payment.paid = True
        payment.save()
        # Now grant story/fundraiser access etc.
    except Payment.DoesNotExist:
        pass