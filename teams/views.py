from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveAPIView
)
from .models import Team, Player
from .serializers import PopulatedTeamSerializer, PlayerSerializer

class TeamListView(ListCreateAPIView):
    ''' GET/POST View /teams '''

    queryset = Team.objects.all()
    serializer_class = PopulatedTeamSerializer

class TeamDetailView(RetrieveAPIView):
    ''' GET View /teams/team_id '''

    queryset = Team.objects.all()
    serializer_class = PopulatedTeamSerializer

class PlayerListView(ListAPIView):
    ''' GET View /players'''

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
