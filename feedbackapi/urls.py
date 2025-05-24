from django.urls import path
from .views import analyze, list_feedbacks, home

urlpatterns = [
    path('analyze/', analyze, name='analyze'),
    path('list/', list_feedbacks, name='list_feedbacks'),
    
]