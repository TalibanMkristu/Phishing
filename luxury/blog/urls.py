from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.posts, name="posts"),
    path('blog/<str:pk>/', views.individual_posts, name="indposts"),
    path('msrTest/', views.msrTest, name='msrtest')
    
]