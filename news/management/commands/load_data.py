from django.core.management.base import BaseCommand
from annoying.functions import get_object_or_None
from news.models import News
from .get_data import get_articles


class Command(BaseCommand):
    help = 'Add articles (title, content, link, image) from dutch websites'

    def handle(self, *args, **kwargs):
        articles = get_articles()
        for article in articles:
            article_object = get_object_or_None(News, link=article.url)
            if article_object is None:
                article_object = News()
                article_object.title = article.translated_title
                article_object.text = article.translated_summary
                article_object.link = article.url
                article_object.image_url = article.image
                article_object.save()

                print('All articles updated')