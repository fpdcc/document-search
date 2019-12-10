from django.apps import apps
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class ActionLog(models.Model):

    class Action(models.TextChoices):
        CREATE = 'create'
        UPDATE = 'update'

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=6, choices=Action.choices)
    # Configure generic relations
    # See: https://docs.djangoproject.com/en/3.0/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']

    def get_action_string(self):
        verb = 'created' if self.action == self.Action.CREATE else 'updated'
        user = self.user or 'Unknown'
        local_time = timezone.localtime(self.timestamp)
        timestamp = local_time.strftime("%b %-d, %Y, %-I:%M %p")
        return f'{verb} by {user} on {timestamp}'

    def __str__(self):
        return f'{self.content_object} {self.get_action_string()}'


class BaseDocumentModel(models.Model):
    source_file = models.FileField()
    actions = GenericRelation(ActionLog)

    class Meta:
        abstract = True

    @classmethod
    def get_slug(cls):
        """
        Return a canonical slug referring to this model by parsing its label.

        Example:
            ControlMonumentMap().get_slug() -> controlmonumentmap
        """
        # Models are namespaced by app, e.g. 'docsearch.controlmonumentmap'
        return cls._meta.label_lower.split('.')[-1]

    @classmethod
    def get_create_url(self):
        """
        Return the canonical URL referring to this object's CreateView.
        """
        return reverse(f'{self.get_slug()}-create')

    def get_absolute_url(self):
        """
        Return the canonical URL referring to this object's DetailView.
        """
        return reverse(f'{self.get_slug()}-detail', args=(self.pk,))


class Book(BaseDocumentModel):
    s3_prefix = 'BOOKS'
    township = models.CharField(max_length=255)
    range = models.CharField(max_length=255)
    section = models.CharField(max_length=255, null=True, blank=True)


class ControlMonumentMap(BaseDocumentModel):
    s3_prefix = 'CONTROL_MONUMENT_MAPS'
    township = models.CharField(max_length=255, null=True, blank=True)
    range = models.CharField(max_length=255, null=True, blank=True)
    section = models.CharField(max_length=255)
    part_of_section = models.CharField(max_length=255, null=True, blank=True)


class SurplusParcel(BaseDocumentModel):
    s3_prefix = 'DEEP_PARCEL_SURPLUS'
    surplus_parcel = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Dossier(BaseDocumentModel):
    s3_prefix = 'DOSSIER_FILES'
    file_number = models.CharField(max_length=255)
    document_number = models.CharField(max_length=3)


class Easement(BaseDocumentModel):
    s3_prefix = 'EASEMENTS'
    easement_number = models.CharField(max_length=255)


class FlatDrawing(BaseDocumentModel):
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
    cad_file = models.FileField('CAD file', null=True, blank=True)


class IndexCard(BaseDocumentModel):
    s3_prefix = 'INDEX_CARDS'
    monument_number = models.CharField(max_length=255, blank=True, null=True)
    township = models.CharField(max_length=255)
    section = models.CharField(max_length=255, null=True, blank=True)
    corner = models.CharField(max_length=255, null=True, blank=True)


class License(BaseDocumentModel):
    s3_prefix = 'LICENSES'
    license_number = models.CharField(max_length=255)


class ProjectFile(BaseDocumentModel):
    s3_prefix = 'PROJECT_FILES'
    area = models.PositiveIntegerField(null=True, blank=True)
    section = models.PositiveIntegerField(null=True, blank=True)
    job_number = models.CharField(max_length=255, null=True, blank=True)
    job_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cabinet_number = models.CharField(max_length=255, null=True, blank=True)
    drawer_number = models.CharField(max_length=255, null=True, blank=True)


class RightOfWay(BaseDocumentModel):
    s3_prefix = 'RIGHT_OF_WAY'
    folder_tab = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'rights of way'


class Survey(BaseDocumentModel):
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


class Title(BaseDocumentModel):
    s3_prefix = 'TITLES'
    control_number = models.CharField(max_length=255)


class InvalidSlugException(ValueError):
    pass


def get_model_from_plural_slug(slug):
    """
    Given a plural slug of a model, return the corresponding model class.

    Example:
        get_model_from_plural_slug(controlmonumentmaps) -> ControlMonumentMap
    """
    if not slug.endswith('s'):
        raise InvalidSlugException(f'slug "{slug}"" must be plural')
    singular_slug = slug[:-1]
    for Model in apps.get_app_config('docsearch').get_models():
        if issubclass(Model, BaseDocumentModel):
            model_slug = Model.get_slug()
            if model_slug == singular_slug:
                return Model
    raise InvalidSlugException(f'No Model found for slug "{slug}"')
