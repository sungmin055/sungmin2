from django.urls import path
from views import base_views

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),
]