from django.urls import path
from hab import views


urlpatterns = [
    # path("", views.index, name="index"),
    path('json_habilete/', views.json_habiletes_list),
    # path('json_activite/<str:slug>', views.json_habiletes_list),
]