"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from youtube_api import views as youtube_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('videos/', youtube_views.get_all_videos_data, name='list_videos'),
    path('search-videos/', youtube_views.search_videos, name='seach_videos_with_title_desc'),
    path('fetch-store-videos/', youtube_views.cron_fetch_and_store, name='cron_fetch_and_store')
]
