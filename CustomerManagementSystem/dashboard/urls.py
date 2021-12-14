from django.urls import path
from .views import DashboardView, AccountView, pdfGenerator

app_name="home"

urlpatterns = [
    path("home/", DashboardView.as_view(), name="dashboard"),
    path("account/", AccountView.as_view(), name="account"),
    path("export/", pdfGenerator, name="pdfGenerator")
]