from django.db import models


class Book(models.Model):
    s3_prefix = 'BOOKS'
    township = models.CharField(max_length=255)
    range = models.CharField(max_length=255)
    section = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField()


class ControlMonumentMap(models.Model):
    s3_prefix = 'CONTROL_MONUMENT_MAPS'
    township = models.CharField(max_length=255, null=True, blank=True)
    range = models.CharField(max_length=255, null=True, blank=True)
    section = models.CharField(max_length=255)
    part_of_section = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField()


class SurplusParcel(models.Model):
    s3_prefix = 'DEEP_PARCEL_SURPLUS'
    surplus_parcel = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    source_file = models.FileField()


class Dossier(models.Model):
    s3_prefix = 'DOSSIER_FILES'
    file_number = models.CharField(max_length=255)
    document_number = models.CharField(max_length=3)
    source_file = models.FileField()


class Easement(models.Model):
    s3_prefix = 'EASEMENTS'
    easement_number = models.CharField(max_length=255)
    source_file = models.FileField()


class FlatDrawing(models.Model):
    s3_prefix = 'FLAT_DRAWINGS'
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
    cad_file = models.FileField('CAD file', null=True, blank=True)


class IndexCard(models.Model):
    s3_prefix = 'INDEX_CARDS'
    monument_number = models.CharField(max_length=255, blank=True, null=True)
    township = models.CharField(max_length=255)
    section = models.CharField(max_length=255, null=True, blank=True)
    corner = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField()


class License(models.Model):
    s3_prefix = 'LICENSES'
    license_number = models.CharField(max_length=255)
    source_file = models.FileField()


class ProjectFile(models.Model):
    s3_prefix = 'PROJECT_FILES'
    area = models.PositiveIntegerField(null=True, blank=True)
    section = models.PositiveIntegerField(null=True, blank=True)
    job_number = models.CharField(max_length=255, null=True, blank=True)
    job_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cabinet_number = models.CharField(max_length=255, null=True, blank=True)
    drawer_number = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField()


class RightOfWay(models.Model):
    s3_prefix = 'RIGHT_OF_WAY'
    folder_tab = models.CharField(max_length=255)
    source_file = models.FileField()

    class Meta:
        verbose_name_plural = 'rights of way'


class Survey(models.Model):
    s3_prefix = 'SURVEYS'
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
    s3_prefix = 'TITLES'
    control_number = models.CharField(max_length=255)
    source_file = models.FileField()
