from django.db import models


class Node(models.Model):
    point = models.ForeignKey("Point",on_delete = models.CASCADE,verbose_name="Точка")
    nodes = models.ManyToManyField('Node',related_name='neighbours',blank=True,verbose_name='Соседние узлы')

class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    floor = models.ForeignKey("Floor",on_delete = models.CASCADE,verbose_name="Этаж")

    def __str__(self) -> str:
        return f"{self.x} {self.y}"

class Floor(models.Model):
    name = models.CharField(max_length = 255,verbose_name='Наименование')
    mapImage = models.ImageField(upload_to='maps/',verbose_name='Карта',blank=True)
    
    def __str__(self) -> str:
        return self.name

class Area(models.Model):
    points = models.ManyToManyField("Point")
    floor = models.ForeignKey("Floor",on_delete = models.CASCADE,verbose_name="Этаж")