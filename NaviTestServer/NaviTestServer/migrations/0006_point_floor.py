# Generated by Django 5.0.3 on 2024-04-03 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NaviTestServer', '0005_point_remove_floor_z_remove_node_x_remove_node_y_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='floor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='NaviTestServer.floor'),
            preserve_default=False,
        ),
    ]
