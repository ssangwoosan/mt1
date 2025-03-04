from django.urls import path
from . import views

urlpatterns = [
    path("", views.reservation_create, name="reservation_create"),
    path("<int:id>/", views.reservation_detail, name="reservation_detail"),
    path("user/<int:user_id>/", views.user_reservations, name="user_reservations"),
    path("<int:id>/update/", views.reservation_update, name="reservation_update"),
    path("<int:id>/delete/", views.reservation_delete, name="reservation_delete"),
]