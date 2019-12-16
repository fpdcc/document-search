import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_home(client, user):
    client.force_login(user)
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_search(client, user, document_and_fields):
    client.force_login(user)
    document, _ = document_and_fields

    Model = type(document)
    doctype_plural = Model._meta.verbose_name_plural.title()

    url = Model.get_search_url()
    response = client.get(url)

    assert response.status_code == 200
    assert f'Search for {doctype_plural}' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_create(client, user, document_and_fields):
    client.force_login(user)
    document, fields = document_and_fields
    # Mock out a file for upload
    fields['source_file'] = SimpleUploadedFile(
        'foobarbaz.png',
        b'content',
        content_type='image/png'
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

    assert most_recent_action.user == user
    assert most_recent_action.action == 'create'


@pytest.mark.django_db
def test_detail(client, user, document_and_fields):
    client.force_login(user)
    document, _ = document_and_fields

    response = client.get(document.get_absolute_url())

    assert response.status_code == 200


@pytest.mark.django_db
def test_update(client, user, document_and_fields):
    client.force_login(user)
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

    assert most_recent_action.user == user
    assert most_recent_action.action == 'update'


@pytest.mark.django_db
def test_delete(client, user, document_and_fields):
    client.force_login(user)
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
