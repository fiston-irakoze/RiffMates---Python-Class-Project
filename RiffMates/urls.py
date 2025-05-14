"""
URL configuration for RiffMates project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from home import views as home_views
from band import views as bandViews
from band import views as restricted_page
from band import views as musician_restricted



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('django.contrib.auth.urls')),
    path("",home_views.homepage, name="home"),
    path('credits/', home_views.credits),
    path('about/', home_views.about,name="about"),
    path('news/', home_views.news, name='news'),
    path("musicians/",bandViews.viewAllBands, name="musician_list"),
    path('musician/<int:id>/', bandViews.viewMusicianDetails, name='musician_detail'),
    path('bands/', bandViews.band_list, name='band_list'),
    path('band/<int:id>/', bandViews.band_detail, name='band_detail'),
    path('venues/', bandViews.venue_list, name='venue_list'),
    path('restricted_page/',bandViews.restricted_page, name='restricted_page'),
    path('musician_restricted/<int:musician_id>/',bandViews.musician_restricted, name='musician_restricted')
]
