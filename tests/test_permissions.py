import pytest
from django.conf import settings
from django.urls import reverse


def get_read_urls_from_document(document):
    """
    Given a model instance representing a document, return the read
    URLs (AKA search and detail).
    """
    Model = type(document)
    search_url = Model.get_search_url()
    detail_url = document.get_absolute_url()
    return search_url, detail_url


def get_write_urls_from_document(document):
    """
    Given a modeul instance representing a document, return the write
    URLs (AKA create, update, and delete).
    """
    Model = type(document)
    create_url = Model.get_create_url()
    update_url = document.get_update_url()
    return (create_url, update_url)


@pytest.mark.django_db
def test_anonymous_users_cannot_read(client, document_and_fields):
    document, _ = document_and_fields
    for url in get_read_urls_from_document(document):
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith('/' + settings.LOGIN_URL)


@pytest.mark.django_db
def test_anonymous_users_cannot_write(client, document_and_fields):
    document, _ = document_and_fields
    for url in get_write_urls_from_document(document):
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith('/' + settings.LOGIN_URL)


@pytest.mark.django_db
def test_read_only_users_can_read(client, read_only_user, document_and_fields, mock_get_queryset):
    client.force_login(read_only_user)
    document, _ = document_and_fields
    for url in get_read_urls_from_document(document):
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_read_only_users_cannot_write(client, read_only_user, document_and_fields):
    client.force_login(read_only_user)
    document, _ = document_and_fields
    for url in get_write_urls_from_document(document):
        response = client.get(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_read_only_users_cannot_delete(client, read_only_user, document_and_fields):
    client.force_login(read_only_user)
    document, _ = document_and_fields
    url = document.get_delete_url()
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_write_users_can_read(client, read_write_user, document_and_fields, mock_get_queryset):
    client.force_login(read_write_user)
    document, _ = document_and_fields
    for url in get_read_urls_from_document(document):
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_write_users_can_write(client, read_write_user, document_and_fields):
    client.force_login(read_write_user)
    document, _ = document_and_fields
    for url in get_write_urls_from_document(document):
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_write_users_can_delete(client, read_write_user, document_and_fields):
    client.force_login(read_write_user)
    document, _ = document_and_fields
    url = document.get_delete_url()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_staff_users_can_delete(client, staff_user, document_and_fields):
    client.force_login(staff_user)
    document, _ = document_and_fields

    url = document.get_delete_url()
    get_response = client.get(url)
    assert get_response.status_code == 200

    post_response = client.post(url)
    assert post_response.status_code == 302


@pytest.mark.django_db
def test_read_only_users_cannot_see_activity_log(client, read_only_user):
    client.force_login(read_only_user)
    url = reverse('activity')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_write_users_can_see_activity_log(client, read_write_user):
    client.force_login(read_write_user)
    url = reverse('activity')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Activity' in response.content.decode('utf-8')
