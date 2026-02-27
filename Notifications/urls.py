from django.urls import path
from .views import notification_views

urlpatterns = [
    path('register-token/', notification_views.RegisterTokenView.as_view()),
    path('send/', notification_views.SendNotificationView.as_view()),
    path('send/<int:user_id>/', notification_views.SendNotificationToUserView.as_view()),
]
