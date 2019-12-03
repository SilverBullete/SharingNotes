from django.urls import path
from . import views

urlpatterns = [
    path('add_note', views.create_note),
    path('get_note', views.get_note_by_id),
    path('star', views.star),
    path('update_note', views.update_note),
]