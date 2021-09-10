from django.contrib import admin
from .models import Team, Player

admin.site.register([Team, Player])
