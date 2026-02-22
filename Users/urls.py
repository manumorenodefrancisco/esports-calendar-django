from django.urls import path

from Users.views import RegisterView, PruebaView, LoginView, LogoutView, UpdateNotiTokenView

urlpatterns = [
    path("registro/", RegisterView.as_view()), # http://localhost:8000/api/registro/
    path("usuarios/", PruebaView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("update-token/", UpdateNotiTokenView.as_view(), name="update-token"),
]