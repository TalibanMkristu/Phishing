from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import stripe.error
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import uuid
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def home(request):
    template_name = 'kcof/home.html'
    title = 'Buy Taliban Coffee'
    context = {}
    return render(request, template_name, context)

class DonationsView(TemplateView):
    template_name = 'kcof/donations.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context = {
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY, 
        }
        return context
    
    def post(self, request, *a, **kwargs):

        context = {}
        return JsonResponse(context)

def checkOut(request):
    amount = 200 #request.POST.get()
    email = 'admin@gmail.com' #request.POST.get()
    YOUR_DOMAIN = f"{request.scheme}://{request.get_host()}"

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': amount * 100,
                'product_data': {
                    'name': 'donations',
                }
            },
            'quantity': 1,
        }],
        metadata = {
            'doner_email': email,
            'donation_amount': str(amount)
        },
    mode='payment',

    success_url= YOUR_DOMAIN + f'/payment-success/',
    cancel_url=YOUR_DOMAIN + f'/donations/',
    )
    return redirect(checkout_session.url)

def paymentSuccess(request):
    return render(request, 'kcof/paymentSuccess.html', )

@csrf_exempt
def stripe_webhook(request):
    event =None 
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.signatureVerificatioError as e:
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        doner_email = session['metadata']['email']
        donated_amount = session['metadata']['donation_amount']
    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        doner_email = session['metadata']['email']
        donated_amount = session['metadata']['donation_amount']
        #save to database

    else:
        print("Unhandled event type {}".format(event['type']))
    return HttpResponse(status=200)

def paypalCheck(request):
    product = 'bag'
    amount = '100'
    host = request.get_host()

    paypal_checkout = {
        'bussiness': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': amount,
        'item_name': product,
        'invoice': uuid.uuid4(),
        'currency-code': 'USD',
        'notify_url': f"http://{host}{reverse("paypal-ipn")}",
        'return_url': f"http://{host}{reverse('kcof:payment-success')}",
        'cancel_url': f"http://{host}{reverse('kcof:home')}"
    }
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    context = {}
    return