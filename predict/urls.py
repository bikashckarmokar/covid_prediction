from predict import views
from django.urls import path

app_name = 'predict'

urlpatterns = [
    path('', views.Predict.as_view()),
]
