from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('teams.urls')),
    path('', admin.site.urls)
]
