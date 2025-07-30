from django.urls import path
from . import views

app_name = 'pract'

urlpatterns = [
    path('forms/', views.MyAjaxForms.as_view(), name='ajax-forms'),
]