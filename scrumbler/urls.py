from django.urls import include, path

urlpatterns = [path("", include("shuffler.urls"))]
