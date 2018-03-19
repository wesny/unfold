from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from django.db.models import Q
from rest_framework_rules.mixins import PermissionRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import *

User = get_user_model()
from unfold.transactions.models import Purchase, Article

def bad_request(message):
    return Response({
        'status': 'error',
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)

class IsPublisher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_publisher

    def has_object_permission(self, request, view, obj):
        return obj.publiisher == request.user

class PurchaseList(APIView):

    def get(self, request, format=None):
        if request.user.is_superuser:
            purchases = Purchase.objects.all()
        elif request.user.is_publisher:
            try:
                buyer = self.request.query_params['buyer']
            except:
                return bad_request('Required parameter missing: buyer')
            purchases = Purchase.objects.filter(buyer__username=buyer, publisher=request.user)
        else:
            try:
                publisher = self.request.query_params['publisher']
            except:
                return bad_request('Required parameter missing: publisher')
            purchases = Purchase.objects.filter(buyer=request.user, publisher__username=publisher)
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     purchase = PurchaseSerializer(data=request.DATA)
    #     if purchase.is_valid():
    #         purchase.save()
    #         return Response(purchase.data, status=status.HTTP_201_CREATED)
    #     return Response(purchase.errors, status=status.HTTP_400_BAD_REQUEST)

class CanAccessArticle(APIView):
    permission_classes = (permissions.IsAuthenticated, IsPublisher,)

    def get(self, request, format=None):
        try:
            username = self.request.query_params['username']
        except:
            return bad_request('Required parameter missing: username')
        try:
            external_id = self.request.query_params['id']
        except:
            return bad_request('Required parameter missing: id')
        authorized = Purchase.objects.filter(buyer__username=username, publisher=request.user, article__external_id=external_id).exists()

        return Response({ "result": authorized })

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    paginate_by = 25

# class PurchaseList(generics.ListAPIView):
#     queryset = transaction_models.Purchase.objects.all()
#     serializer_class = PurchaseSerializer

class ArticleList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsPublisher,)
    serializer_class = ArticleSerializer
    paginate_by = 25

    def get_queryset(self):
        return transaction_models.Article.objects.filter(publisher=self.request.user)

    def create(self, request, *args, **kwargs):
        art=Article(publisher=request.user)
        serializer = self.serializer_class(art, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



