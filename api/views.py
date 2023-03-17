from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets

from .models import api
from .serializers import apiSimpleSerializer, apiDetailSerializer, apiCreateSerializer


class apisAPIView(APIView):
    def get(self, request):
        apis = api.objects.filter(complete=False)
        serializer = apiSimpleSerializer(apis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = apiCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class apiAPIView(APIView):
    def get(self, request, pk):
        api = get_object_or_404(api, id=pk)
        serializer = apiDetailSerializer(api)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        api = get_object_or_404(api, id=pk)
        serializer = apiCreateSerializer(api, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoneapisAPIView(APIView):
    def get(self, request):
        dones = api.objects.filter(complete=True)
        serializer = apiSimpleSerializer(dones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoneapiAPIView(APIView):
    def get(self, request, pk):
        done = get_object_or_404(api, id=pk)
        done.complete = True
        done.save()
        serializer = apiDetailSerializer(done)
        return Response(status=status.HTTP_200_OK)