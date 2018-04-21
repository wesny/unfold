from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token

from unfold.users.views import CustomSignupView

from pinax.stripe.views import (
    InvoiceListView,
    PaymentMethodCreateView,
    PaymentMethodDeleteView,
    PaymentMethodListView,
    PaymentMethodUpdateView,
)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^user/?', include('unfold.users.urls', namespace='users')),
    url(r'^publisher/signup/?$', CustomSignupView.as_view(), name='publisher_signup'),
    url(r'^accounts/signup/?$', CustomSignupView.as_view(), name='account_signup'),
    url(r'^accounts/', include('allauth.urls')),

    url(r"^payment-methods/?$", PaymentMethodListView.as_view(), name="pinax_stripe_payment_method_list"),
    url(r"^payment-methods/create/?$", PaymentMethodCreateView.as_view(), name="pinax_stripe_payment_method_create"),
    url(r"^payment-methods/(?P<pk>\d+)/delete/?$", PaymentMethodDeleteView.as_view(), name="pinax_stripe_payment_method_delete"),
    url(r"^payment-methods/(?P<pk>\d+)/update/?$", PaymentMethodUpdateView.as_view(), name="pinax_stripe_payment_method_update"),

    # Your stuff: custom urls includes go here
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^', include('transactions.urls')),
    url(r'^api/', include('rest.urls')),
    url(r'^api-token-auth/?$', obtain_jwt_token),
    url(r'^cas/', include('mama_cas.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
