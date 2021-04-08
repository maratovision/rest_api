from django.urls import path
from .views import *

urlpatterns = [
    path('rates/', RateView.as_view()),
    path('rates/<int:worker_id>/', RateWorkerView.as_view())
]