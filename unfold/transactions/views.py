from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect, render

from unfold.transactions.models import Purchase, Article
from unfold.transactions.admin import PurchaseForm
from unfold.users.models import User

class PurchaseView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "pages/purchase_article.html"
    form_class = PurchaseForm

    def test_func(self):
        return self.request.user.is_publisher

    def get(self, request, *args, **kwargs):
        publisherusername = request.GET.get('publisher', None)
        external_id = request.GET.get('id', None)
        if publisherusername == None or external_id == None:
            raise Http404("Invalid Parameters")
        try:
            article = Article.objects.get(publisher__username=publisherusername, external_id=external_id)
        except ObjectDoesNotExist:
            raise Http404("Article referenced does not exist")
        purchase = Purchase.objects.filter(article=article, buyer=request.user)
        if purchase.exists():
            return redirect(article.url)
        try:
            publisher = User.objects.get(username=publisherusername)
        except ObjectDoesNotExist:
            raise Http404("Publisher does not exist")
        form = self.form_class(initial={
                'external_id': external_id,
                'publisher': publisherusername,
                'price': article.price,
            })
        data = {
            'form': form,
            'price': article.price,
            'publisher': publisher.name,
            'title': article.title
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            external_id = form.cleaned_data['external_id']
            publisherusername = form.cleaned_data['publisher']
            price = form.cleaned_data['price']
            try:
                article = Article.objects.get(publisher__username=publisherusername, external_id=external_id)
            except ObjectDoesNotExist:
                raise Http404("Article referenced does not exist")
            if article.price != price:
                raise Http404("Price has changed since submission")
            purchase = Purchase(article=article, price=price, buyer=request.user)
            purchase.save()
            return redirect(article.url)
        return render(request, self.template_name, {'form': form})
