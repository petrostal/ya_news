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


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, form_in_context',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_form_for_different_users(parametrized_client, form_in_context, detail_url):
    response = parametrized_client.get(detail_url)
    assert ('form' in response.context) is form_in_context


@pytest.mark.django_db
def test_comments_order(comment, client, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created
