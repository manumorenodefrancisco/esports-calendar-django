from django.urls import path
from Anotaciones.views.anotacion_view import AnotacionView

urlpatterns = [
    path('anotaciones/', AnotacionView.as_view())
]