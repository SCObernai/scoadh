from django.urls import path
from adh import views


urlpatterns = [
    path("", views.index, name="index"),
    path('json_activite/', views.json_activite_list),
    path('json_activite/<str:slug>/', views.json_activite_detail),
]