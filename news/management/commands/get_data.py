import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import deepl


# initialization of environmental variables
web = os.environ.get('NEWS_WEB')
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

deepl_api_key = os.environ.get('DEEPL_API_KEY')
translator = deepl.Translator(deepl_api_key)
URL = requests.get(web)



class Article:
    def __init__(self, url):
        self.content = ''
        self.url = url
        self.summary = ''
        self.translated_summary = ''
        self.title = ''
        self.translated_title = ''
        self.date = ''
        self.image = ''


# functions for getting links and content from the website
def get_links_list(data):
    soup = BeautifulSoup(data.content, "lxml")
    articles = []
    url_list = []

    for a in soup.find_all('a', href=True):
        if "/artikel/" in a['href']:
            webdata = os.environ.get('NEWS_WEB')
            full_url = webdata + a['href']
            if full_url not in url_list:
                url_list.append(full_url)
                article = Article(webdata + a['href'])
                articles.append(article)

    return articles[:5]


def get_content(articles):
    for article in articles:
        response = requests.get(article.url)
        soup = BeautifulSoup(response.content, "lxml")
        article.title = soup.title.string
        print(f"Title: {article.title}")

        time_tag = soup.find('time')
        if time_tag:
            datetime_value = time_tag['datetime']
        else:
            datetime_value = None
        article.date = datetime_value

        content_text = []
        for p in soup.select('main > div > p'):
            content_text.append(p.string)
        article.content = [''.join(str(item) for item in content_text)]
        print('Content is loaded')


# sending content of articles to ChatGPT which summarize them
def summarize_articles(articles):
    for article in articles:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Summarize the article in up to 2 sentences to make a preview for my news website. Don't use words "
                   f"like 'this article', make it smooth: {article.content}",
            max_tokens=500)
        main_idea = response.choices[0].text.strip()
        main_idea = main_idea.replace('"', '')
        main_idea = main_idea.replace('[', '')
        main_idea = main_idea.replace(']', '')
        article.summary = main_idea
        print(f"Summary dutch is loaded")


# sending summarised articles to deeple to translate them
def translate_article(articles):
    for article in articles:
        article.translated_summary = str(translator.translate_text(article.summary, target_lang="EN-US"))
        article.translated_title = str(translator.translate_text(article.title, target_lang="EN-US"))
        print(f"Translated summary: {article.translated_summary}")
        print(f"Translated title: {article.translated_title}")


def get_image(articles):
    for article in articles:
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"""You are a newspaper illustrator. Your primary responsibility is to create compelling digital 
                       artwork that complements and enhances the ARTICLE. Adherence to the following guidelines is
                       crucial: Content Sensitivity: You must always respect our policy against depicting violence,
                       gore, sexual content, eroticism, pornography, suicide, discrimination, blood, or any NSFW
                       elements. If an article contains sensitive topics, you should employ allegory and
                       abstraction to convey the message respectfully and thoughtfully. Creativity and Originality:
                       You should strive to produce original, witty, and ingenious illustrations. Your artwork must
                       not only reflect the essence of the ARTICLE SUMMARY but also be memorable and engaging to
                       our readers. Professionalism and Politeness: All illustrations must maintain a high standard
                       of professionalism. They should be polite and suitable for a diverse audience, reflecting
                       our commitment to inclusivity and respect for all readers. Adherence to Article Summary:
                       Your illustrations must be closely aligned with the ARTICLE SUMMARY, capturing its key
                       themes and messages. You should use your artistic judgment to highlight the most relevant
                       aspects of the story in your visual interpretation. Style Consistency: While creativity is
                       encouraged, you must also maintain a consistent digital art style that aligns with our
                       publication\'s aesthetic and branding. Ethical Representation: You should avoid stereotypes
                       and ensure that representations of individuals or groups are fair, balanced, and respectful.
                       NEVER ADD TEXT TO YOUR IMAGES! NO TEXT! \nARTICLE SUMMARY:\n{article.translated_summary}""",
                n=1,
                size="1024x1024",
                quality="standard",
            )
            article.image = response.data[0].url
            print("Image created")
        except Exception as e:
            print(f"Image generation failed due to safety system: {e}")


# final function
def get_articles():
    print('Application started')
    articles = get_links_list(URL)
    get_content(articles)
    summarize_articles(articles)
    translate_article(articles)
    get_image(articles)

    return articles




