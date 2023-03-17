from rest_framework import serializers
from .models import api


class apiSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = api
        fields = ('id', 'title', 'complete', 'important')


class apiDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = api
        fields = ('id', 'title', 'description', 'created', 'complete',
                  'important')


class apiCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = api
        fields = ('title', 'description')