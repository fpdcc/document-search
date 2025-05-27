from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres import fields as pg_fields
from django.contrib.postgres import forms as pg_forms
from django.contrib.gis.db import models as gis_models
from django.core.validators import FileExtensionValidator

from .validators import validate_positive_int, validate_int_btwn, validate_int_range,  validate_int_array, validate_date


class InclusiveIntegerRangeFormField(pg_forms.IntegerRangeField):
    """
    Adjust the built-in Postgres range field so that its upper bound is
    inclusive instead of exclusive. See:
    https://code.djangoproject.com/ticket/27147#comment:5
    """
    _unit_value = 1

    def compress(self, values):
        range_value = super().compress(values)
        if range_value:
            return self.range_type(range_value.lower, range_value.upper, bounds='[]')

    def prepare_value(self, value):
        value = super().prepare_value(value)
        # We need to clean both fields
        value = [field.clean(val) for field, val in zip(self.fields, value)]
        if value[1] is not None:
            value[1] = value[1] - self._unit_value
        return value


class InclusiveIntegerRangeField(pg_fields.IntegerRangeField):
    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': InclusiveIntegerRangeFormField,
            **kwargs,
        })


class ActionLog(models.Model):

    class Action:
        CREATE = 'create'
        UPDATE = 'update'
        CHOICES = ((CREATE, CREATE), (UPDATE, UPDATE))

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=6, choices=Action.CHOICES)
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
    def get_plural_slug(cls):
        """
        Return a plural version of this model's slug.

        Override this method if the model name has an irregular plural form.
        """
        return f'{cls.get_slug()}s'

    @classmethod
    def get_create_url(cls):
        """
        Return the canonical URL referring to this object's CreateView.
        """
        return reverse(f'{cls.get_slug()}-create')

    @classmethod
    def get_search_url(cls):
        """
        Return the canonical URL referring to this object's Search view.
        """
        return reverse(f'{cls.get_slug()}-search')

    @classmethod
    def get_data_url(cls):
        """
        Return the canonical URL referring to this object's DocumentData view
        (for returning DataTables search results).
        """
        return reverse(f'{cls.get_slug()}-data')

    def get_absolute_url(self):
        """
        Return the canonical URL referring to this object's DetailView.
        """
        return reverse(f'{self.get_slug()}-detail', args=(self.pk,))

    def get_update_url(self):
        """
        Return the canonical URL referring to this object's UpdateView.
        """
        return reverse(f'{self.get_slug()}-update', args=(self.pk,))

    def get_delete_url(self):
        """
        Return the canonical URL referring to this object's UpdateView.
        """
        return reverse(f'{self.get_slug()}-delete', args=(self.pk,))


RANGE_FIELD_HELP_TEXT = (
    'Specify the lower and upper bounds for the range of values represented '
    'by this field. If this field only has one value, set it as both the '
    'lower and upper bounds.'
)


ARRAY_FIELD_HELP_TEXT = (
    'Set multiple values for this field by separating them with commas. E.g. '
    'to save the values 1, 2, and 3, record them as 1,2,3.'
)

DATE_FIELD_HELP_TEXT = ('Enter the date as "YYYY-MM-DD"')


class Book(BaseDocumentModel):
    township = InclusiveIntegerRangeField(
        max_length=255,
        null=True,
        blank=True,
        help_text=RANGE_FIELD_HELP_TEXT)
    range = InclusiveIntegerRangeField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_int_range(min=9, max=15)],
        help_text=RANGE_FIELD_HELP_TEXT)
    section = InclusiveIntegerRangeField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_int_range(min=1, max=36)],
        help_text=RANGE_FIELD_HELP_TEXT)
    source_file = models.FileField(upload_to='BOOKS', validators=[FileExtensionValidator(['pdf'])])


class ControlMonumentMap(BaseDocumentModel):
    PART_OF_SECTION_CHOICES = [
        ("E1/2", "E1/2"),
        ("W1/2", "W1/2")
    ]

    township = models.PositiveIntegerField(
        null=True,
    )
    range = models.PositiveIntegerField(
        null=True,
        validators=[validate_int_btwn(9, 15)]
    )
    section = pg_fields.ArrayField(
        models.PositiveIntegerField(null=True),
        validators=[validate_int_array(1, 36)],
        help_text=ARRAY_FIELD_HELP_TEXT
    )
    part_of_section = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        choices=PART_OF_SECTION_CHOICES,
    )
    source_file = models.FileField(upload_to='CONTROL_MONUMENT_MAPS', validators=[FileExtensionValidator(['pdf'])])


class SurplusParcel(BaseDocumentModel):
    surplus_parcel = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    source_file = models.FileField(upload_to='DEEP_PARCEL_SURPLUS', validators=[FileExtensionValidator(['pdf'])])


class DeepTunnel(BaseDocumentModel):
    description = models.TextField()
    source_file = models.FileField(upload_to='DEEP_PARCEL_SURPLUS', validators=[FileExtensionValidator(['pdf'])])


class Dossier(BaseDocumentModel):
    file_number = models.CharField(max_length=255, validators=[validate_positive_int])
    document_number = models.CharField(max_length=3, validators=[validate_positive_int])
    source_file = models.FileField(
        upload_to='DOSSIER_FILES',
        validators=[FileExtensionValidator(['pdf'])]
    )


class Easement(BaseDocumentModel):
    easement_number = models.CharField(max_length=255, validators=[validate_positive_int], null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    source_file = models.FileField(upload_to='EASEMENTS', validators=[FileExtensionValidator(['pdf'])])


class FlatDrawing(BaseDocumentModel):
    area = models.PositiveIntegerField(null=True, blank=True, validators=[validate_int_btwn(1, 33)])
    section = models.PositiveIntegerField(null=True, blank=True)
    map_number = models.CharField(max_length=255, null=True, blank=True)
    location = models.TextField(blank=True, null=True)
    building_id = models.IntegerField(verbose_name='Building ID', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    job_number = models.CharField(max_length=255, blank=True, null=True)
    number_of_sheets = models.CharField(max_length=255, null=True, blank=True, validators=[validate_positive_int])
    date = models.CharField(max_length=255, null=True, blank=True, validators=[validate_date], help_text=DATE_FIELD_HELP_TEXT)
    cross_ref_area = models.PositiveIntegerField(null=True, blank=True, validators=[validate_int_btwn(1, 33)])
    cross_ref_section = models.PositiveIntegerField(null=True, blank=True, validators=[validate_int_btwn(1, 36)])
    cross_ref_map_number = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    hash = models.CharField(max_length=255, null=True, blank=True)
    cad_file = models.FileField(
        'CAD file',
        null=True,
        blank=True,
        validators=[FileExtensionValidator([
            'dwg',
            'dxf',
            'dgn',
            'stl'
        ])],
    )
    source_file = models.FileField(upload_to='FLAT_DRAWINGS', validators=[FileExtensionValidator(['pdf'])])


class IndexCard(BaseDocumentModel):
    monument_number = models.CharField(max_length=255, blank=True, null=True)
    township = models.CharField(max_length=255)
    section = models.CharField(max_length=255, null=True, blank=True)
    corner = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField(upload_to='INDEX_CARDS', validators=[FileExtensionValidator(['pdf'])])


class License(BaseDocumentModel):
    TYPE_CHOICES = [
        ("combined_sewer", "Combined Sewer"),
        ("electric", "Electric"),
        ("gas", "Gas"),
        ("pipeline", "Pipeline"),
        ("sanitary_sewer", "Sanitary Sewer"),
        ("storm sewer", "Storm Sewer"),
        ("telecom", "Telecom"),
        ("water main", "Water Main"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("TBD", "TBD"),
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("continuous", "Continuous"),
        ("expired", "Expired"),
        ("indefinite", "Indefinite"),
        ("perpetual", "Perpetual"),
    ]

    license_number = models.CharField(
        max_length=255,
        null=True, blank=True,
    )
    description = models.TextField(null=True, blank=True)
    geometry = gis_models.GeometryCollectionField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, null=True, blank=True)
    entity = models.CharField(max_length=255, null=True, blank=True)
    diameter = models.PositiveIntegerField(null=True, blank=True, validators=[validate_positive_int])
    material = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_date],
        help_text=DATE_FIELD_HELP_TEXT
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=True, blank=True)
    agreement_type = models.CharField(max_length=255, null=True, blank=True)
    township = pg_fields.ArrayField(
        models.PositiveIntegerField(null=True),
        help_text=ARRAY_FIELD_HELP_TEXT,
        default=list
    )
    range = pg_fields.ArrayField(
        models.PositiveIntegerField(null=True),
        validators=[validate_int_array(9, 15)],
        help_text=ARRAY_FIELD_HELP_TEXT,
        default=list
    )
    section = pg_fields.ArrayField(
        models.PositiveIntegerField(null=True),
        validators=[validate_int_array(1, 36)],
        help_text=ARRAY_FIELD_HELP_TEXT,
        default=list
    )
    source_file = models.FileField(upload_to='LICENSES', validators=[FileExtensionValidator(['pdf'])])


class ProjectFile(BaseDocumentModel):
    area = models.PositiveIntegerField(null=True, blank=True, validators=[validate_int_btwn(1, 33)])
    section = models.PositiveIntegerField(null=True, blank=True, validators=[validate_int_btwn(1, 36)])
    job_number = models.CharField(max_length=255, null=True, blank=True)
    job_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cabinet_number = models.CharField(max_length=255, null=True, blank=True, validators=[validate_int_btwn(1, 10)])
    drawer_number = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField(upload_to='PROJECT_FILES', validators=[FileExtensionValidator(['pdf'])])


class RightOfWay(BaseDocumentModel):
    folder_tab = models.CharField(max_length=255)
    source_file = models.FileField(upload_to='RIGHT_OF_WAY', validators=[FileExtensionValidator(['pdf'])])

    class Meta:
        verbose_name_plural = 'rights of way'

    @classmethod
    def get_plural_slug(cls):
        return 'rightsofway'


class Survey(BaseDocumentModel):
    township = pg_fields.ArrayField(
        models.PositiveIntegerField(null=True, blank=True),
        help_text=ARRAY_FIELD_HELP_TEXT
    )
    section = pg_fields.ArrayField(
        models.PositiveIntegerField(null=True, blank=True),
        validators=[validate_int_array(1, 36)],
        help_text=ARRAY_FIELD_HELP_TEXT
    )
    range = pg_fields.ArrayField(
        models.PositiveIntegerField(null=True, blank=True),
        validators=[validate_int_array(9, 15)],
        help_text=ARRAY_FIELD_HELP_TEXT
    )
    map_number = models.CharField(max_length=255, null=True, blank=True)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    job_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="control number")
    number_of_sheets = models.CharField(max_length=255, blank=True, null=True, validators=[validate_positive_int])
    date = models.CharField(max_length=255, blank=True, null=True, validators=[validate_date], help_text=DATE_FIELD_HELP_TEXT)
    cross_ref_area = models.PositiveIntegerField(blank=True, null=True, validators=[validate_int_btwn(1, 33)])
    cross_ref_section = models.PositiveIntegerField(blank=True, null=True, validators=[validate_int_btwn(1, 36)])
    cross_ref_map_number = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    hash = models.CharField(max_length=255, null=True, blank=True)
    source_file = models.FileField(upload_to='SURVEYS', validators=[FileExtensionValidator(['pdf'])])


class Title(BaseDocumentModel):
    control_number = models.CharField(max_length=255, validators=[validate_positive_int])
    source_file = models.FileField(upload_to='TITLES', validators=[FileExtensionValidator(['pdf'])])


class NotificationSubscription(models.Model):
    notification_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
