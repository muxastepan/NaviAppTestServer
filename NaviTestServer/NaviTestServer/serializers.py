from rest_framework import serializers
from NaviTestServer.models import *

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'
    
    def create(self, validated_data):
        node, res = Node.objects.get_or_create(x=validated_data['x'],y=validated_data['y'],z=validated_data['z'])
        return  node