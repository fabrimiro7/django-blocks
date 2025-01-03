from django.urls import path

from .views import SingleTestElementListCreateView

urlpatterns = [
    path("element/", SingleTestElementListCreateView.as_view(), name="test"),
]
