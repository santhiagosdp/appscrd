
from django.contrib import admin
from django.urls import path, include
import os

urlpatterns = [
    #path('sdp/', admin.site.urls),
    path('admin/', admin.site.urls),
    #path('home', include('institucional.urls')),
    path('', include('startgame.urls')),
    path('startgame', include('startgame.urls')),
]