from django.db import models

class Player(models.Model):
    POSITIONS = (
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    )

    name = models.CharField(max_length=40)
    position = models.CharField(max_length=2, choices=POSITIONS)
    totalPoints = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    goalkeeper = models.ForeignKey(
        Player,
        related_name='gk_teams',
        on_delete=models.DO_NOTHING,
        null=True
    )
    defenders = models.ManyToManyField(
        Player,
        related_name='df_teams'
    )
    midfielders = models.ManyToManyField(
        Player,
        related_name='mf_teams'
    )
    forwards = models.ManyToManyField(
        Player,
        related_name='fw_teams'
    )

    def __str__(self):
        return f'{self.name}'
