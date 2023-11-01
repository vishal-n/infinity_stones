from django.urls import path
from .views import LoginView, RegisterView, ActivateView, activate_stone_async

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/', ActivateView.as_view(), name='activate-stone'),
    path('activate-async/', activate_stone_async, name='activate_async'),
]
