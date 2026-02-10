from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('upload/', views.upload_csv),
    path('datasets/', views.get_datasets),
    path('datasets/<int:dataset_id>/', views.get_dataset),
    path('datasets/<int:dataset_id>/pdf/', views.generate_pdf),
]
