from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from .models import Player, Team

class PlayerSerializer(ModelSerializer):
    ''' Base Player Serializer '''

    class Meta:
        model = Player
        fields = '__all__'

class TeamSerializer(ModelSerializer):
    ''' Base Team Serializer '''

    class Meta:
        model = Team
        fields = '__all__'

class PopulatedTeamSerializer(TeamSerializer):
    ''' Populated Serializer for read/write teams '''

    goalkeeper = PlayerSerializer()
    defenders = PlayerSerializer(many=True)
    midfielders = PlayerSerializer(many=True)
    forwards = PlayerSerializer(many=True)

    def to_representation(self, instance):
        '''
        Totals all players in a teams "total_points" and adds a total_ponts
        key to the team response
        '''

        rep = super().to_representation(instance)
        total_points = 0
        total_points += instance.goalkeeper.totalPoints
        dfs = instance.defenders.all()
        mfs = instance.midfielders.all()
        fwds = instance.forwards.all()

        for player in dfs:
            total_points += player.totalPoints
        for player in mfs:
            total_points += player.totalPoints
        for player in fwds:
            total_points += player.totalPoints

        rep['total_points'] = total_points
        rep['formation'] = f'{len(dfs)}-{len(mfs)}-{len(fwds)}'
        return rep

    def validate(self, attrs):
        ''' Validates Team for correct players in position and size '''

        gk = attrs.get('goalkeeper')
        if gk['position'] != 'GK':
            raise ValidationError(detail='Incorrect Position GK')

        dfs = attrs.get('defenders')
        if len(dfs) < 3 or len(dfs) > 5:
            raise ValidationError(detail='Must have between 3 - 5 Defenders')
        for player in dfs:
            if player['position'] != 'DF':
                raise ValidationError(detail='Incorrect Position DF')

        mfs = attrs.get('midfielders')
        if len(mfs) < 3 or len(mfs) > 5:
            raise ValidationError(detail='Must have between 3 - 5 Midfielders')
        for player in mfs:
            if player['position'] != 'MF':
                raise ValidationError(detail='Incorrect Position MF')

        fwds = attrs.get('forwards')
        for player in fwds:
            if player['position'] != 'FW':
                raise ValidationError(detail='Incorrect Position FW')
        if len(fwds) < 1 or len(fwds) > 3:
            raise ValidationError(detail='Must have between 1 - 3 Forwards')

        total_players = 1 + len(dfs) + len(mfs) + len(fwds)
        if total_players != 11:
            raise ValidationError(detail='Incorrect Squad Size')

        return attrs

    def create(self, validated_data):
        ''' Allows POST request with populated players '''

        goalkeeper_data = validated_data.pop('goalkeeper')
        defenders_data = validated_data.pop('defenders')
        midfielders_data = validated_data.pop('midfielders')
        forwards_data = validated_data.pop('forwards')

        team = Team.objects.create(**validated_data)

        goalkeeper = Player.objects.get(**goalkeeper_data)
        defenders = [Player.objects.get(**data) for data in defenders_data]
        midfielders = [Player.objects.get(**data) for data in midfielders_data]
        forwards = [Player.objects.get(**data) for data in forwards_data]

        team.goalkeeper = goalkeeper
        team.defenders.set(defenders)
        team.midfielders.set(midfielders)
        team.forwards.set(forwards)

        team.save()

        return team
