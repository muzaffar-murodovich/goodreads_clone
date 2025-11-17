from django.urls import path, include
from users.views import RegisterView, LoginView


urlpatterns = [
    path("register.html", RegisterView.as_view(), name="register"),
    path("login.html", LoginView.as_view(), name="login"),
]
