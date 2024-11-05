from django.urls import path
from core_modules.testing.views import SingleTestElementListCreateView

urlpatterns = [
    path('element/', SingleTestElementListCreateView.as_view(), name="test"),
]
