from django.urls import path
from rest_framework.routers import DefaultRouter
from Subscriptions.views.subscription_view import SubscriptionView

urlpatterns = [path("subscriptions/", SubscriptionView.as_view())]
