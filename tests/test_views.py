import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_home(client, superuser):
    client.force_login(superuser)
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_search(client, superuser, document_and_fields, mock_get_queryset):
    client.force_login(superuser)
    document, _ = document_and_fields

    Model = type(document)
    doctype_plural = Model._meta.verbose_name_plural.title()

    url = Model.get_search_url()
    response = client.get(url)

    assert response.status_code == 200
    assert f'Search for {doctype_plural}' in response.content.decode('utf-8')
    mock_get_queryset.assert_called_once()


@pytest.mark.django_db
def test_create(client, superuser, document_and_fields):
    client.force_login(superuser)
    document, fields = document_and_fields
    # Mock out a file for upload
    fields['source_file'] = SimpleUploadedFile(
        'foobarbaz.pdf',
        b'content',
        content_type='application/pdf'
    )

    Model = type(document)
    doctype = Model._meta.verbose_name.title()

    url = Model.get_create_url()
    get_response = client.get(url)

    assert get_response.status_code == 200
    assert f'Add new {doctype}' in get_response.content.decode('utf-8')

    post_response = client.post(url, data=fields)

    assert post_response.status_code == 302

    new_doc = Model.objects.last()
    assert new_doc != document
    most_recent_action = new_doc.actions.first()

    assert most_recent_action.user == superuser
    assert most_recent_action.action == 'create'


@pytest.mark.django_db
def test_detail(client, superuser, document_and_fields):
    client.force_login(superuser)
    document, _ = document_and_fields

    response = client.get(document.get_absolute_url())

    assert response.status_code == 200


@pytest.mark.django_db
def test_update(client, superuser, document_and_fields):
    client.force_login(superuser)
    document, fields = document_and_fields

    Model = type(document)
    doctype = Model._meta.verbose_name.title()

    url = document.get_update_url()
    get_response = client.get(url)

    assert get_response.status_code == 200
    assert f'Edit {doctype}' in get_response.content.decode('utf-8')

    post_response = client.post(url, data=fields)

    assert post_response.status_code == 302

    document.refresh_from_db()
    most_recent_action = document.actions.first()

    assert most_recent_action.user == superuser
    assert most_recent_action.action == 'update'


@pytest.mark.django_db
def test_delete(client, superuser, document_and_fields):
    client.force_login(superuser)
    document, _ = document_and_fields

    Model = type(document)
    url = document.get_delete_url()
    get_response = client.get(url)

    assert get_response.status_code == 200

    response_content = get_response.content.decode('utf-8')
    expected_string = f'Are you sure you want to delete this {Model._meta.verbose_name.title()}?'
    assert expected_string in response_content

    post_response = client.post(url)

    assert post_response.status_code == 302

    Model = type(document)
    with pytest.raises(Model.DoesNotExist):
        type(document).objects.get(id=document.id)


@pytest.mark.django_db
def test_version_history(client, superuser, document_and_fields):
    client.force_login(superuser)
    document, fields = document_and_fields

    # Post an update to create an ActionLog for this document
    client.post(document.get_update_url(), data=fields)
    document.refresh_from_db()
    assert document.actions.count() == 1

    # Test the detail view
    detail_response = client.get(document.get_absolute_url())
    assert detail_response.status_code == 200
    assert 'Version history' in detail_response.content.decode('utf-8')

    # Test the DataTables API endpoint for the detail view
    detail_data_response = client.get(document.get_data_url())
    assert detail_data_response.status_code == 200
    assert detail_data_response.json()['recordsTotal'] == 1

    # Test the global activity view
    activity_response = client.get(reverse('activity'))
    assert activity_response.status_code == 200

    # Test the DataTables API endpoint for the global activity view
    activity_data_response = client.get(reverse('activity-data'))
    assert activity_data_response.status_code == 200
    assert activity_data_response.json()['recordsTotal'] == 1
