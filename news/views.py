from django.core.paginator import Paginator
from django.shortcuts import render
from .models import News


def get_news(request):
    articles = News.objects.all()
    articles = list(reversed(articles))
    context = {
         'articles': articles
    }
    return render(request, 'news.html', context)

    # paginator = Paginator(articles, 5)  # Show 5 articles per page.
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    # first_articles, second_articles, third_articles, forth_articles, fifth_articles = [], [], [], [], []
    # for index, article in enumerate(articles):
    #     if index == 0:  # For the very first article
    #         first_articles.append(article)
    #     # elif index % 5 == 0:
    #     #     second_articles.append(article)
    #     elif index % 4 == 1:
    #         second_articles.append(article)
    #     elif index % 4 == 2:
    #         third_articles.append(article)
    #     elif index % 4 == 3:
    #         forth_articles.append(article)
    #     elif index % 4 == 0:
    #         fifth_articles.append(article)
    #
    # context = {
    #     'first_articles': first_articles,
    #     'second_articles': second_articles,
    #     'third_articles': third_articles,
    #     'forth_articles': forth_articles,
    #     'fifth_articles': fifth_articles
    #     # 'page_obj': page_obj
    # }
    # return render(request, 'news.html', context)


def get_article(request, num):
    articles = News.objects.all()
    for article in articles:
        if article.id == num:
            return render(request, 'news_page.html', {'article': article})


def get_disclaimer(request):
    return render(request, 'disclaimer.html')


def get_main(request):
    return render(request, 'main.html')
