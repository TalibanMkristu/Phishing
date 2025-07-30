from django.urls import path
from . import views

app_name = 'kcof'

urlpatterns = [
    path('',  views.home ,name='home'),
    path('donations/', views.DonationsView.as_view(), name='donations'),
    path('checkout/', views.checkOut, name='checkout'),
    path('payment-success/', views.paymentSuccess, name='payment-success'),
    path('stripewebhook/', views.paymentSuccess, name='stripe-webhook'),

]