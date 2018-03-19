from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.fields import CurrentUserDefault


User = get_user_model()
from unfold.transactions import models as transaction_models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'balance', 'is_publisher')
        depth = 1

class UserPurchaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
        depth = 1

class PurchaseSerializer(serializers.ModelSerializer):
    publisher = UserPurchaseSerializer(source="article.publisher")
    buyer = UserPurchaseSerializer()

    class Meta:
        model = transaction_models.Purchase
        fields = ('buyer', 'publisher', 'price', 'article')
        depth = 1

class ArticleSerializer(serializers.ModelSerializer):
    publisher = UserSerializer(required=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = transaction_models.Article
        fields = ('external_id', 'publisher', 'url', 'price', 'title')
        depth = 1
        validators = []

    def save(self):
        validated_data = self.validated_data
        external_id=validated_data['external_id']
        url=validated_data['url'] 
        price=validated_data['price']
        title=validated_data['title']
        publisher=self.context['request'].user
        article, created = transaction_models.Article.objects.update_or_create(
          external_id=external_id, 
          publisher=publisher,
          defaults={
            'price':price,
            'url':url,
            'title':title
          }
        )
        return article
