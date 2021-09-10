from django.urls import path
from .views import TeamListView, TeamDetailView,PlayerListView

urlpatterns = [
    path('teams/', TeamListView.as_view()),
    path('teams/<int:pk>/', TeamDetailView.as_view()),
    path('players/', PlayerListView.as_view())
]
