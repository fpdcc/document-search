# Generated by Django 2.2.8 on 2019-12-20 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsearch', '0006_deeptunnel'),
    ]

    operations = [
        migrations.AddField(
            model_name='easement',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='license',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='easement',
            name='easement_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='license_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
