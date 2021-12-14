from django.urls import path
from .views import AuthenticationView, TestView

app_name="authentication"

urlpatterns = [
    path('', AuthenticationView.as_view(), name='index'),
    path('<str:service>', AuthenticationView.as_view(), name="auth"),
    path('test/', TestView.as_view(), name="test"),
]