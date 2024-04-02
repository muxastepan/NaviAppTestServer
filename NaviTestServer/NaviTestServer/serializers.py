from rest_framework import serializers
from NaviTestServer.models import *

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        read_only_fields = (
            "id",
        )
        fields = (
            "id",
            "x",
            "y",
            "z",
            "nodes"
        )
    def create(self, validated_data):
        node,res = Node.objects.get_or_create(x=validated_data.pop('x'),
                                              y=validated_data.pop('y'),
                                              z=validated_data.pop('z'))
        return node
    
    def update(self, instance, validated_data):
        if(instance in validated_data['nodes']):
            raise serializers.ValidationError("Node can't reference itself")
        instance.nodes.set(validated_data['nodes'])
        instance.x = validated_data['x']
        instance.y = validated_data['y']
        instance.z = validated_data['z']

        instance.save()
        return instance

class PointSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    z = serializers.FloatField()