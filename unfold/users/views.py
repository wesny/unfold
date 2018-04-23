from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.shortcuts import get_object_or_404 
from allauth.account.views import SignupView
from pinax.stripe.mixins import CustomerMixin, PaymentsContextMixin
from django.conf import settings


from .models import User

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    # slug_field = 'username'
    #slug_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail')


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail')

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context.update({
            "PINAX_STRIPE_PUBLIC_KEY": settings.PINAX_STRIPE_PUBLIC_KEY
        })
        return context
