import pytest

from news.models import News, Comment

from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from datetime import datetime, timedelta


@pytest.fixture
def login_url():
    return settings.LOGIN_URL


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='tit-le',
        text='text',
    )
    return news


@pytest.fixture
def news_id(news):
    return news.id,


@pytest.fixture
def comment(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return Comment.objects.first()


@pytest.fixture
def comment_id(comment):
    return comment.id,


@pytest.fixture
def bulk_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def detail_url(news_id):
    return reverse('news:detail', args=news_id)
