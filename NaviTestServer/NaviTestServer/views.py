from typing import Any
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework import viewsets

from NaviTestServer.models import *
from NaviTestServer.serializers import *
from NaviTestServer.a_star import *

class Nodes(viewsets.ModelViewSet):
    base_name = "nodes"
    serializer_class = NodeSerializer
    queryset = Node.objects.all()

    def perform_create(self, serializer):
        if (not serializer.is_valid()):
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data['id'],status=status.HTTP_201_CREATED)
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance,request.data,partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def perform_destroy(self, instance):
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class Navigate(viewsets.ViewSet):
    base_name = "navigate"
    serializer_class = PointSerializer

    def list(self,request):
        from_id = request.GET.get('from')
        to_id = request.GET.get('to') 
        if (not from_id or not to_id):
            return Response(data='from or to param is empty',status=status.HTTP_400_BAD_REQUEST)
        try:
            from_node = Node.objects.get(pk=from_id)
            to_node = Node.objects.get(pk = to_id)
        except:
            return Response(data='node not found', status=status.HTTP_400_BAD_REQUEST)
        seializer =  self.serializer_class(AStar.find_path(from_node,to_node),many=True)
        return Response(seializer.data)
    