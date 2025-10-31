from django.urls import path

from .views import ShuffledFileView, UploadFileView

urlpatterns = [
    path("", UploadFileView.as_view(), name="upload-file"),
    path("shuffled-file/", ShuffledFileView.as_view(), name="shuffled-file"),
]
