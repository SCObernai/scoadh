from django.urls import path
from glo import views


urlpatterns = [
    path("debug", views.debug, name="debug"),
    path("test", views.test, name="test"),
    path("system.js", views.system_js, name="system_js"),
]