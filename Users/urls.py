from django.urls import path

from Users.views import RegisterView, PruebaView, LoginView, LogoutView, UpdatePerfilView

urlpatterns = [
    path("registro/", RegisterView.as_view()), # http://localhost:8000/api/registro/
    path("usuarios/", PruebaView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("update-perfil/", UpdatePerfilView.as_view(), name="update-perfil"),
]