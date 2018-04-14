from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.conf.urls import url
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'rest'

urlpatterns = [
    url(r'^users/?$', views.UserList.as_view(), name='user-list'),
    url(r'^purchases/?$', views.PurchaseList.as_view()),
    url(r'^has-access/?$', views.CanAccessArticle.as_view()),
    url(r'^validate-token/?$', views.ValidateSSOToken.as_view()),
    url(r'^articles/?$', views.ArticleList.as_view(), name='article-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
