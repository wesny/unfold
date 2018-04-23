from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from pinax.stripe.actions import customers, sources, charges
from .models import User
from rest_framework_jwt.settings import api_settings
import stripe
from django.utils.encoding import smart_str
from decimal import Decimal

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('name',)}),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'name', 'is_superuser')
    search_fields = ['name']

class SignupForm(forms.Form):

    name = forms.CharField(max_length=150, label='Name', widget=forms.TextInput(attrs={'placeholder': 'Name'}))

    def init(self, *args, **kwargs):
        super(SignupForm, self).init(*args, **kwargs)

    def signup(self, request, user):
        user.name = self.cleaned_data['name']
        if 'publisher' in request.path:
            user.is_publisher = True
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.token = token
        else:
            try:
                customer = customers.create(user)
                sources.create_card(customer, request.POST.get("stripeToken"))
                add_on = request.POST.get('amount')
                if add_on != '':
                    add_on = Decimal(add_on)
                    charges.create(amount=add_on, customer=user.customer.stripe_id)
                    user.balance = user.balance + add_on
            except stripe.CardError as e:
                user.delete()
                raise forms.ValidationError(smart_str(e))
        user.save()

    class Meta:
        model = User
        fields = ('name',)
