# Generated by Django 2.2.8 on 2020-01-24 21:54

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docsearch', '0010_inclusive_integer_range_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryCollectionField(blank=True, null=True, srid=4326),
        ),
    ]