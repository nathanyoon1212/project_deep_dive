from django.urls import path
from petsitters.views import PetsitterListView, PetsitterDetailView, PetsitterRegisterView

urlpatterns = [
    path('/list', PetsitterListView.as_view()),
    path('/detail/<int:petsitter_id>', PetsitterDetailView.as_view()),
    path('/register', PetsitterRegisterView.as_view()),
]