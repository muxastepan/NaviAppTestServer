from django.db import models

class Node(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    nodes = models.ManyToManyField('Node',related_name='neighbours',blank=True)
    