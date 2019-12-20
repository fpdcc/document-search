import pytest
from django.contrib.auth.models import User

from docsearch import models

DOCUMENTS = [
    (models.Book, {'township': 'foo', 'range': 'bar', 'section': 'baz'}),
    (models.ControlMonumentMap, {
        'township': 1, 'range': 2, 'section': [3, 4], 'part_of_section': 'bam'
    }),
    (models.SurplusParcel, {'surplus_parcel': 'foo', 'description': 'bar'}),
    (models.DeepTunnel, {'description': 'foobarbaz'}),
    (models.Dossier, {'file_number': 'foo', 'document_number': 'bar'}),
    (models.Easement, {'easement_number': 'foo'}),
    (models.FlatDrawing, {
        'area': 1, 'section': 2, 'map_number': 'foo', 'location': 'bar',
        'description': 'baz', 'job_number': 'foo', 'number_of_sheets': 'bar',
        'date': 'baz', 'cross_ref_area': 1, 'cross_ref_section': 2,
        'cross_ref_map_number': 'foo', 'hash': 'bar'
    }),
    (models.IndexCard, {
        'monument_number': 'foo', 'township': 'foo', 'corner': 'bar', 'section': 'baz'
    }),
    (models.License, {'license_number': 'foo'}),
    (models.ProjectFile, {
        'area': 1, 'section': 2, 'job_number': 'foo', 'job_name': 'bar',
        'description': 'baz', 'cabinet_number': 'foo', 'drawer_number': 'bar',
    }),
    (models.RightOfWay, {'folder_tab': 'foo'}),
    (models.Survey, {
        'township': [1], 'section': [2], 'range': [3], 'map_number': 'foo', 'location': 'bar',
        'description': 'baz', 'job_number': 'foo', 'number_of_sheets': 'bar',
        'date': 'baz', 'cross_ref_area': 1, 'cross_ref_section': 2,
        'cross_ref_map_number': 'foo', 'hash': 'bar'
    }),
    (models.Title, {'control_number': 'foo'}),
]


@pytest.fixture
def user():
    return User.objects.create(username='testuser', password='foobarbaz')


@pytest.fixture(params=DOCUMENTS)
def document_and_fields(request):
    Model, fields = request.param
    fields['source_file'] = 'foobarbaz.pdf'
    return Model.objects.create(**fields), fields
