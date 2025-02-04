from django.urls import path
from core_modules.testing.views import SingleTestElementListCreateView, AggiungiTaskAddView, AggiungiTaskStampaView

urlpatterns = [
    path('element/', SingleTestElementListCreateView.as_view(), name="test"),
    path('aggiungi_task/add', AggiungiTaskAddView.as_view(), name="task_add"),
    path('aggiungi_task/stampa', AggiungiTaskStampaView.as_view(), name="task_stampa"),

