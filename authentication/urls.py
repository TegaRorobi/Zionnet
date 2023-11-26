from django.urls import path
from authentication.views import RegisterView, LoginAPIView


urlpatterns = [
    path('signup/', RegisterView.as_view(), name="sinup"),
    path('login/', LoginAPIView.as_view(), name="login")
]