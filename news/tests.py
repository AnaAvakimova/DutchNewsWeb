from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from news.models import News
import io

class TestLoadDataCommand(TestCase):
    @patch('news.management.commands.load_data.get_articles')
    @patch('news.management.commands.load_data.get_object_or_None')
    @patch('news.models.urlopen')
    def test_handle_new_article(self, mock_urlopen, mock_get_object, mock_get_articles):
        # Setup
        mock_article = MagicMock()
        mock_article.url = 'http://example.com'
        mock_article.translated_title = 'Test Title'
        mock_article.translated_summary = 'Test Summary'
        mock_article.image = 'http://example.com/image.jpg'

        mock_get_articles.return_value = [mock_article]
        mock_get_object.return_value = None

        # Mock the image download
        mock_urlopen.return_value = io.BytesIO(b"fake image data")

        # Execute
        call_command('load_data')

        # Assert
        created_news = News.objects.get(
            link='http://example.com',
            title='Test Title',
            text='Test Summary',
            image_url='http://example.com/image.jpg'
        )
        self.assertIsNotNone(created_news.image)

    @patch('news.management.commands.load_data.get_articles')
    @patch('news.management.commands.load_data.get_object_or_None')
    def test_handle_existing_article(self, mock_get_object, mock_get_articles):
        # Setup
        mock_article = MagicMock()
        mock_article.url = 'http://example.com'

        mock_get_articles.return_value = [mock_article]
        mock_get_object.return_value = MagicMock()

        # Execute
        call_command('load_data')

        # Assert
        mock_get_object.assert_called_once_with(News, link='http://example.com')
        self.assertEqual(News.objects.count(), 0)

    @patch('news.management.commands.load_data.get_articles')
    @patch('news.management.commands.load_data.get_object_or_None')
    def test_handle_no_image(self, mock_get_object, mock_get_articles):
        # Setup
        mock_article = MagicMock()
        mock_article.url = 'http://example.com'
        mock_article.image = None

        mock_get_articles.return_value = [mock_article]
        mock_get_object.return_value = None

        # Execute
        call_command('load_data')

        # Assert
        self.assertEqual(News.objects.count(), 0)

    @patch('news.management.commands.load_data.get_articles')
    def test_handle_empty_articles(self, mock_get_articles):
        # Setup
        mock_get_articles.return_value = []

        # Execute
        call_command('load_data')

        # Assert
        self.assertEqual(News.objects.count(), 0)