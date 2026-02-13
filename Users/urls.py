from django.urls import path

from Users.views import RegisterView, PruebaView, LoginView

urlpatterns = [
    path("registro/", RegisterView.as_view()), # http://localhost:8000/api/registro/
    path("usuarios/", PruebaView.as_view()),
    path("login/", LoginView.as_view()),
]