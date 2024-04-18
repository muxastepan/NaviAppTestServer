from rest_framework import serializers
from NaviTestServer.models import *

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id','title','node','area']
    
    def create(self, validated_data):
        if(validated_data['node'] and validated_data['area']):
            shop,res = Shop.objects.get_or_create(title=validated_data['title'], 
                                                          node=validated_data['node'],area=validated_data['area'])
        elif(validated_data['node']):
            shop,res = Shop.objects.get_or_create(title=validated_data['title'], 
                                                          node=validated_data['node'])
        elif(validated_data['area']):
            shop,res = Shop.objects.get_or_create(title=validated_data['title'], 
                                                          area=validated_data['area'])
        else:
            shop,res = Shop.objects.get_or_create(title=validated_data['title'])
        return shop

class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ['id','title','node']
    
    def create(self, validated_data):
        if(validated_data['node']):
            terminal,res = Terminal.objects.get_or_create(title=validated_data['title'], 
                                                          node=validated_data['node'])
        else:
            terminal,res = Terminal.objects.get_or_create(title=validated_data['title'])
        return terminal

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = (
            "id",
            "name",
            "map_image",
        )



class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        read_only_fields = (
            "id",
        )
        fields = (
            "x",
            "y",
            "floor"
        )
    
    def create(self, validated_data):
        point,res = Point.objects.get_or_create(
            x = validated_data.pop("x"),
            y = validated_data.pop("y"),
            floor = validated_data.pop("floor")
        )
        return point

class NodeSerializer(serializers.ModelSerializer):
    point = PointSerializer()
    class Meta:
        model = Node
        read_only_fields = (
            "id",
        )
        fields = (
            "id",
            "point",
            "nodes"
        )
    def create(self, validated_data):
        validated_point = validated_data.pop('point')
        point,res = Point.objects.get_or_create(**validated_point)
        node,res = Node.objects.get_or_create(point = point)
        return node
    
    def update(self, instance, validated_data):
        if(instance in validated_data['nodes']):
            raise serializers.ValidationError("Node can't reference itself")
        instance.nodes.set(validated_data['nodes'])
        point,res = Point.objects.get_or_create(**validated_data['point'])
        instance.point = point

        instance.save()
        return instance

class AreaSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)
    class Meta:
        model = Area
        read_only_fields = (
            "id",
        )
        fields = (
            "id",
            "points",
            "floor"
        )
    def create(self, validated_data):
        validated_points = validated_data.pop('points')
        points = []
        for validated_point in validated_points:
            point,res = Point.objects.get_or_create(**validated_point)
            points.append(point)
        
        area = Area.objects.create(floor = validated_data.pop('floor'))
        area.points.set(points)
        return area
    
    def update(self, instance, validated_data):
        for i,point in enumerate(instance.points.all()):
            point.x = validated_data['points'][i]['x']
            point.y = validated_data['points'][i]['y']
            point.floor = validated_data['floor']
            point.save()

        floor = Floor.objects.get(id=validated_data['floor'].id)
        instance.floor =floor

        instance.save()
        return instance