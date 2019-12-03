from django.urls import path
from . import views

urlpatterns = [
    path('all_notes', views.get_notes),
    path("notes/<int:subject>", views.get_notes_by_subject),
    path("get_subjects", views.get_subjects)
]