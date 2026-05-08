# fundraisers/views.py
try:
    from django.shortcuts import render, redirect, get_object_or_404
    from django.conf import settings
    from django.http import JsonResponse, HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    from django.contrib.auth.decorators import login_required
    from notifications.utils import create_notification
    from .models import *
    from .forms import FundraiserForm
    from decimal import Decimal
    from django.contrib.auth import get_user_model
    import stripe
except ImportError as e:
    print(f"\nError: Django not available.\n{e}")

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

import logging
logger = logging.getLogger(__name__)

from .models import Fundraiser
# ----------------- FUNDRAISER PAGES -----------------

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


@login_required
def fundraiser_detail(request, fundraiser_id):
    fundraiser = get_object_or_404(Fundraiser, id=fundraiser_id)
    return render(request, 'fundraisers/detail.html', {
        'fundraiser': fundraiser
    })

# ----------------- FUNDRAISER CHECKOUT -----------------
@csrf_exempt
@login_required
def create_checkout_session(request, fundraiser_id):
    fundraiser = get_object_or_404(Fundraiser, id=fundraiser_id)

    amount = int(request.POST.get('amount', 0))
    if amount <= 0:
        return redirect('fundraisers:fundraiser_detail', fundraiser_id)

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
            'payment_type': 'fundraiser',
            'fundraiser_id': str(fundraiser.id),
            'user_id': str(request.user.id),
        }
    )

    return redirect(session.url)



# # ----------------- WEBHOOK -----------------

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except (ValueError, stripe.error.SignatureVerificationError):
#         return HttpResponse(status=400)

#     if event['type'] != 'checkout.session.completed':
#         return HttpResponse(status=200)

#     session = event['data']['object']
#     metadata = session.get('metadata', {})
#     payment_type = metadata.get('payment_type')

#     if payment_type != 'fundraiser':
#         return HttpResponse(status=200)

#     user_id = metadata.get('user_id')
#     fundraiser_id = metadata.get('fundraiser_id')
#     if not all([user_id, fundraiser_id]):
#         return HttpResponse(status=200)

#     try:
#         user = User.objects.get(pk=user_id)
#         fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
#     except (User.DoesNotExist, Fundraiser.DoesNotExist):
#         return HttpResponse(status=200)

#     amount_paid = Decimal(session['amount_total']) / Decimal('100')
#     fundraiser.total_raised += amount_paid
#     fundraiser.save()

#     return HttpResponse(status=200)

# ----------------- SUCCESS / CANCEL -----------------

def success(request):
    return render(request, 'fundraisers/success.html')


def cancel(request):
    return render(request, 'fundraisers/cancel.html')
