from typing import Any
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from NaviTestServer.models import *
from NaviTestServer.serializers import *

class ApiRoot(generics.GenericAPIView):
    name="api-root"
    def get(self,request,*args,**kwargs):
        return Response({
            "nodes": reverse(Nodes.name,request=request)
        })


class Nodes(generics.ListAPIView):
    name = "nodes"
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if (not serializer.is_valid()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    #def delete(self,request,*args,**kwargs):
        