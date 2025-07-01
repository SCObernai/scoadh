from django.urls import path
from hab import views


from act import views


urlpatterns = [
    path('json_activites/', views.json_activite_list),
    path('json_activite/<str:slug>/', views.json_activite_detail),
]