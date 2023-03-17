from django.urls import path

from .views import apiAPIView, apisAPIView, DoneapiAPIView, DoneapisAPIView

urlpatterns = [
    path('api/', apisAPIView.as_view()),
    path('api/<int:pk>/', apiAPIView.as_view()),
    path('done/', DoneapisAPIView.as_view()),
    path('done/<int:pk>/', DoneapiAPIView.as_view()),
]