from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from django_filters.rest_framework import DjangoFilterBackend
from .models import Team, Player
from .serializers import PopulatedTeamSerializer, PlayerSerializer

class TeamListView(ListCreateAPIView):
    ''' GET/POST View /teams '''

    queryset = Team.objects.all()
    serializer_class = PopulatedTeamSerializer

class TeamDetailView(RetrieveUpdateDestroyAPIView):
    ''' GET View /teams/team_id '''

    queryset = Team.objects.all()
    serializer_class = PopulatedTeamSerializer

class PlayerListView(ListAPIView):
    ''' GET View /players'''

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['position']
