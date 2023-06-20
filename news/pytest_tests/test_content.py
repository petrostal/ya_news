from django.conf import settings
from http import HTTPStatus
import pytest

from pytest_django.asserts import assertRedirects

from django.urls import reverse


HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, bulk_news):
    response = client.get(HOME_URL)
    news_count = len(response.context['object_list'])
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, bulk_news):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates
