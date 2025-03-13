import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import MainCategiry, LastCategiry
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def authenticated_client(db):
    """Создание суперпользователя"""

    user = User.objects.create_superuser(username='admin', password='password')
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_get_main_categiry_list(authenticated_client):
    """Тест get метода MainCategiry"""

    MainCategiry.objects.create(
        name='Test Category',
        slug='test-category',
        image='path/to/image.jpg'
    )
    url = reverse('api:mcategories-list')
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert MainCategiry.objects.count() == 1


@pytest.mark.django_db
def test_post_main_categiry(authenticated_client):
    """Тест post метода MainCategiry"""

    data = {
        "name": "New Category",
        "slug": "new-category",
        "image": (
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABiey"
            "waAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACk"
            "lEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
        ),
    }
    url = reverse('api:mcategories-list')
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert MainCategiry.objects.count() == 1
    assert MainCategiry.objects.get().name == 'New Category'


@pytest.mark.django_db
def test_get_last_categiry_list(authenticated_client):
    """Тест get метода LastCategiry"""

    main_category = MainCategiry.objects.create(
        name='Main Category',
        slug='main-category',
        image='path/to/image.jpg'
    )
    LastCategiry.objects.create(
        name='Test Subcategory',
        slug='test-subcategory',
        image='path/to/image.jpg',
        main_categiry=main_category
    )
    url = reverse('api:lcategories-list',
                  kwargs={'category_id': main_category.id})
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert LastCategiry.objects.count() == 1


@pytest.mark.django_db
def test_post_last_categiry(authenticated_client):
    """Тест post метода LastCategiry"""

    main_category = MainCategiry.objects.create(
        name='Main Category', slug='main-category', image='path/to/image.jpg')

    data = {
        "name": "New Subcategory",
        "slug": "new-subcategory",
        "image": (
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABiey"
            "waAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACk"
            "lEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
        ),
    }
    url = reverse('api:lcategories-list',
                  kwargs={'category_id': main_category.id})
    response = authenticated_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert LastCategiry.objects.count() == 1
    assert LastCategiry.objects.get().name == 'New Subcategory'
