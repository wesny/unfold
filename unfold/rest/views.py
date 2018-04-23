from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status, generics
from django.db.models import Q
from rest_framework_rules.mixins import PermissionRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from mama_cas.cas import validate_service_ticket
from mama_cas.exceptions import ValidationError

from .serializers import *

User = get_user_model()
from unfold.transactions.models import Purchase, Article

def bad_request(message):
    return Response({
        'status': 'error',
        'message': message,
    }, status=status.HTTP_400_BAD_REQUEST)

def bad_credentials(message):
    return Response({
        'status': 'error',
        'message': message,
    }, status=status.HTTP_401_UNAUTHORIZED)

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

    def get(self, request):
        try:
            external_id = self.request.query_params['id']
        except:
            return bad_request('Required parameter missing: id')
        username = self.request.query_params.get('username', None)
        token = self.request.query_params.get('token', None)
        if not username and not token:
            return bad_request('Must include either username or token')
        if token:
            try:
                st, attributes, pgt = validate_service_ticket(request.user.get_username() + '.com', token)
                token_username = st.user.get_username()
            except ValidationError:
                return bad_credentials("Token is invalid or expired")
            if username and username != token_username:
                return bad_request("Username must match token username")
            else:
                username = token_username
        authorized = Purchase.objects.filter(buyer__username=username, article__publisher=request.user, article__external_id=external_id).exists()
        return Response({ "result": authorized })

class ValidateSSOToken(APIView):
    permission_classes = (permissions.IsAuthenticated, IsPublisher,)

    def get(self, request):
        try:
            token = self.request.query_params['token']
        except:
            return bad_request('Required parameter missing: token')
        try:
            st, attributes, pgt = validate_service_ticket(request.user.get_username() + '.com', token)
            result = {'valid' : True, 'username' : st.user.get_username()}
        except ValidationError:
            result = {'valid' : False}
        return Response(result)

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
            art = serializer.create(serializer.validated_data)
            return Response(self.serializer_class(art).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



