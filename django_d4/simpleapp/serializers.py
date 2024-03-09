from .models import *
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# class SubscriptionsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Subscriptions
#         field = ['id', 'user', 'category']
