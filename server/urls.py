"""pokerstats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from pokerstats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),

    # API
    path('api/token-auth/', obtain_jwt_token),
    path('api/player/', views.PlayerDetailView.as_view()),
    path('api/game/<int:pk>/', views.GameDetailView.as_view()),
    path('api/games/', views.GameListView.as_view()),
    path('api/rebuy_create/', views.RebuyCreateView.as_view()),
    path('api/game_create/', views.GameCreateView.as_view()),
    path('api/game_finish/', views.GameFinishView.as_view()),
    path('api/round_update/<int:pk>/', views.RoundUpdateView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]