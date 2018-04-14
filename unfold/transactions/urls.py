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

app_name = 'transactions'

urlpatterns = [
    url(r'^purchase/?$', views.PurchaseView.as_view(), name='purchase-view'),
    url(r'^reload/?$', views.ReloadView.as_view(), name='reload-view'),
    url(r'^stripe/charges/?$', views.ChargeListView.as_view(), name='reload-view')
]

urlpatterns = format_suffix_patterns(urlpatterns)
