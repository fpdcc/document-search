import json

import pytest
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import GEOSGeometry
from django.core.management import call_command
from haystack.query import EmptySearchQuerySet

from docsearch import models

DOCUMENTS = [
    (models.Book, {'township': '[1,1]', 'range': '[2,4]', 'section': '[3,5]'}),
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
    (models.License, {
        'license_number': 'foo',
        'township': [42],
        'section': [30],
        'range': [12],
        'geometry': json.dumps({
            "type": "GeometryCollection",
            "geometries": [{"type": "Point", "coordinates": [0, 0]}]
        }),
    }),
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
def superuser():
    return User.objects.create_superuser('testuser', 'test@example.com', 'foobarbaz')


@pytest.fixture
def staff_user():
    return User.objects.create(username='staff_user', password='foobarbaz', is_staff=True)


@pytest.fixture
def permission_groups():
    call_command('create_permission_groups')


@pytest.fixture
def read_only_user(permission_groups):
    group = Group.objects.get(name='Read Only')
    user = User.objects.create(username='read_only', password='foobarbaz')
    user.groups.add(group)
    user.save()
    return user


@pytest.fixture
def read_write_user(permission_groups):
    group = Group.objects.get(name='Read/Write')
    user = User.objects.create(username='read_write', password='foobarbaz')
    user.groups.add(group)
    user.save()
    return user


@pytest.fixture(params=DOCUMENTS)
def document_and_fields(request):
    Model, fields = request.param
    fields['source_file'] = 'foobarbaz.pdf'
    updated_fields = fields.copy()
    if fields.get('geometry'):
        updated_fields['geometry'] = GEOSGeometry(fields['geometry'])
    return Model.objects.create(**updated_fields), fields


@pytest.fixture
def mock_get_queryset(mocker):
    """
    Mock the BaseSearchView.get_queryset method to prevent search views from
    actually querying Solr.
    """
    return mocker.patch(
        f'docsearch.views.base.BaseSearchView.get_queryset',
        return_value=EmptySearchQuerySet()
    )
