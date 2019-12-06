from django.db import models


class ControlMonumentMap(models.Model):
    section = models.CharField(max_length=255)
    township = models.TextField(null=True, blank=True)
    range = models.TextField(null=True, blank=True)
    part_of_section = models.CharField(max_length=4, null=True, blank=True)
    source_file = models.FileField()


class SurplusParcel(models.Model):
    surplus_parcel = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    source_file = models.FileField()


class Dossier(models.Model):
    file_number = models.CharField(max_length=255)
    document_number = models.CharField(max_length=3)
    source_file = models.FileField()


class Easement(models.Model):
    easement_number = models.CharField(max_length=255)
    source_file = models.FileField()


class FlatDrawing(models.Model):
    area = models.PositiveIntegerField(null=True, blank=True)
    section = models.PositiveIntegerField(null=True, blank=True)
    map_number = models.CharField(max_length=255, null=True, blank=True)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    job_number = models.CharField(max_length=255, blank=True, null=True)
    number_of_sheets = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True)
    cross_ref_area = models.PositiveIntegerField(null=True, blank=True)
    cross_ref_section = models.PositiveIntegerField(null=True, blank=True)
    cross_ref_map_number = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    hash = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField()


class IndexCard(models.Model):
    monument_number = models.CharField(max_length=255, blank=True, null=True)
    township = models.CharField(max_length=255)
    section = models.CharField(max_length=255, null=True, blank=True)
    corner = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField()


class License(models.Model):
    license_number = models.CharField(max_length=255)
    source_file = models.FileField()


class ProjectFile(models.Model):
    area = models.PositiveIntegerField(null=True, blank=True)
    section = models.PositiveIntegerField(null=True, blank=True)
    job_number = models.CharField(max_length=255, null=True, blank=True)
    job_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cabinet_number = models.CharField(max_length=255, null=True, blank=True)
    drawer_number = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField()


class RightOfWay(models.Model):
    folder_tab = models.CharField(max_length=255)
    source_file = models.FileField()


class Survey(models.Model):
    area = models.PositiveIntegerField(null=True, blank=True)
    section = models.PositiveIntegerField(null=True, blank=True)
    map_number = models.CharField(max_length=255, null=True, blank=True)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    job_number = models.CharField(max_length=255, blank=True, null=True)
    number_of_sheets = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    cross_ref_area = models.PositiveIntegerField(blank=True, null=True)
    cross_ref_section = models.PositiveIntegerField(blank=True, null=True)
    cross_ref_map_number = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    hash = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField()


class Title(models.Model):
    control_number = models.CharField(max_length=255)
    source_file = models.FileField()
