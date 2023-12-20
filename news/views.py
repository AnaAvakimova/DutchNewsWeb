from django.core.paginator import Paginator
from django.shortcuts import render
from .models import News
from django.http import JsonResponse


def get_news(request):
    # articles = News.objects.all()
    # articles = list(reversed(articles))
    # context = {
    #     'articles': articles
    # }
    # return render(request, 'news.html', context)

    articles = News.objects.all().order_by('-created_at')
    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': articles,
        'page_obj': page_obj
    }
    return render(request, 'news.html', context)


def get_article(request, num):
    articles = News.objects.all()
    for article in articles:
        if article.id == num:
            return render(request, 'news_page.html', {'article': article})


def get_disclaimer(request):
    return render(request, 'disclaimer.html')


def get_main(request):
    return render(request, 'main.html')
