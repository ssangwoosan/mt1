from django.urls import path
from . import views

urlpatterns = [
    path("", views.table_list, name="table_list"),              # GET /tables/
    path("create/", views.table_create, name="table_create"),   # POST /tables/
    path("available/", views.available_tables, name="available_tables"),  # GET /tables/available/
]