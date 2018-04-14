from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from django.utils.http import is_safe_url
from rest_framework import status, generics
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from mama_cas.models import ServiceTicket
from mama_cas.utils import redirect as cas_redirect
from mama_cas.utils import to_bool
from rest_framework.response import Response
from decimal import Decimal
import urllib
from pinax.stripe.actions import customers, charges
from pinax.stripe.mixins import CustomerMixin
from pinax.stripe.models import Charge

from unfold.transactions.models import Purchase, Article
from unfold.transactions.admin import PurchaseForm
from unfold.users.models import User

def bad_request(message):
    return Response({
        'status': 'error',
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)

class PurchaseView(LoginRequiredMixin, View):
    template_name = "pages/purchase_article.html"
    form_class = PurchaseForm

    # def test_func(self):
    #     return self.request.user.is_publisher

    def get(self, request, *args, **kwargs):
        publisherusername = request.GET.get('publisher', None)
        external_id = request.GET.get('id', None)
        new_token = to_bool(request.GET.get('new_token', None))
        if publisherusername == None or external_id == None:
            return bad_request("Invalid Parameters")
        try:
            article = Article.objects.get(publisher__username=publisherusername, external_id=external_id)
        except ObjectDoesNotExist:
            return bad_request("Article referenced does not exist")
        purchase = Purchase.objects.filter(article=article, buyer=request.user)
        if purchase.exists():
            if new_token != None:
                publisher = User.objects.get(username=publisherusername)
                st = ServiceTicket.objects.create_ticket(service=publisherusername + '.com', user=request.user)
                return cas_redirect(article.url, params={'token': st.ticket})
            else:
                return redirect(article.url)
        try:
            publisher = User.objects.get(username=publisherusername)
        except ObjectDoesNotExist:
            return bad_request("Publisher does not exist")
        next_url = ''
        if article.price > request.user.balance:
            next_url = urllib.parse.quote(request.get_full_path(), safe='~()*!.\'')
        form = self.form_class(initial={
                'external_id': external_id,
                'publisher': publisherusername,
                'price': article.price
            })
        data = {
            'form': form,
            'price': article.price,
            'publisher': publisher.name,
            'title': article.title,
            'balance': request.user.balance,
            'next': next_url or ''
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            external_id = form.cleaned_data['external_id']
            publisherusername = form.cleaned_data['publisher']
            price = form.cleaned_data['price']
            new_token = to_bool(request.GET.get('new_token', None))
            try:
                article = Article.objects.get(publisher__username=publisherusername, external_id=external_id)
            except ObjectDoesNotExist:
                return bad_request("Article referenced does not exist")
            if article.price != price:
                return bad_request("Price has changed since submission")
            purchase = Purchase(article=article, price=price, buyer=request.user)
            purchase.save()
            request.user.balance = request.user.balance - purchase.price
            request.user.save()
            publisher = User.get(username=publisherusername)
            publisher.balance = publisher.balance + purchase.price
            publisher.save()
            if new_token != None:
                st = ServiceTicket.objects.create_ticket(service=publisherusername + '.com', user=request.user)
                return cas_redirect(article.url, params={'token': st.ticket})
            else:
                return redirect(article.url)
        return render(request, self.template_name, {'form': form})

class ReloadView(LoginRequiredMixin, View):
    template_name = "pages/refill_account.html"

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(
            'next',
            self.request.GET.get('next', '')
        )
        url_is_safe = is_safe_url(url=redirect_to)
        return redirect_to if url_is_safe else ''

    def get(self, request, *args, **kwargs):
        customer = customers.get_customer_for_user(self.request.user)
        can_charge = True
        balance = request.user.balance
        data = {
            'balance': balance,
            'can_charge': can_charge
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        add_on = Decimal(request.POST.get('amount'))
        user = User.objects.get(username=request.user.username)
        user.balance = user.balance + add_on
        charges.create(amount=add_on, customer=request.user.customer.stripe_id)
        user.save()
        url = self.get_redirect_url() or '/'
        return redirect(url)

class StripeAccountFromCustomerMixin(object):
    @property
    def stripe_account(self):
        customer = getattr(self, "customer", None)
        return customer.stripe_account if customer else None

    @property
    def stripe_account_stripe_id(self):
        return self.stripe_account.stripe_id if self.stripe_account else None
    stripe_account_stripe_id.fget.short_description = "Stripe Account"

class ChargeListView(LoginRequiredMixin, CustomerMixin, ListView):
    model = Charge
    context_object_name = "charge_list"
    template_name = "pinax/stripe/charge_list.html"

    def get_queryset(self):
        return super(ChargeListView, self).get_queryset().order_by("charge_created")

