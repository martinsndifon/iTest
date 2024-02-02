"""
Test for article apis.
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Article, Provider

from article.serializers import ArticleSerializer


ARTICLE_URL = reverse("article:article-list")
PRICE_FILTER_URL = reverse("article:price-filter-list")


def detail_url(article_id):
    """Return article detail URL"""
    return reverse("article:article-detail", args=[article_id])


def create_provider():
    """Create and return a sample provider"""
    return Provider.objects.create(provider_name="Provider1")


def create_many_articles(provider, number):
    """Create and return a {number} of sample articles"""
    for i in range(number):
        Article.objects.create(
            article_name=f"Article{i}", price=100 * (i + 1), provider_no=provider
        )


class ArticleApiTests(TestCase):
    """Test the article API"""

    def setUp(self):
        self.client = APIClient()
        self.provider = create_provider()

    def test_retrieve_article_list(self):
        """Test retrieving a list of article"""
        create_many_articles(self.provider, 4)

        res = self.client.get(ARTICLE_URL)

        article = Article.objects.all().order_by("-article_no")
        serializer = ArticleSerializer(article, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_article_detail(self):
        """Test retrieving a article detail"""
        article = Article.objects.create(
            article_name="Article1", price=1234, provider_no=self.provider
        )

        url = detail_url(article.article_no)
        res = self.client.get(url)

        serializer = ArticleSerializer(article)
        self.assertEqual(res.data, serializer.data)

    def test_create_article(self):
        """Test creating article"""
        payload = {
            "article_name": "Article1",
            "price": 1234,
            "provider_no": self.provider.provider_no,
        }
        self.client.post(ARTICLE_URL, payload)

        exists = Article.objects.filter(article_name=payload["article_name"]).exists()
        self.assertTrue(exists)

    def test_create_article_duplicate(self):
        """Test creating article with duplicate details"""
        payload = {
            "article_name": "Article1",
            "price": 1234,
            "provider_no": self.provider.provider_no,
        }
        self.client.post(ARTICLE_URL, payload)
        res = self.client.post(ARTICLE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_invalid(self):
        """Test creating article with invalid payload"""
        payload = {}
        res = self.client.post(ARTICLE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def create_article_with_invalid_provider(self):
        """Test creating article with invalid provider"""
        payload = {
            "article_name": "Article1",
            "price": 1234,
            "provider_no": 9999,
        }
        res = self.client.post(ARTICLE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_article(self):
        """Test updating a article with patch"""
        article = Article.objects.create(
            article_name="Article1", price=1234, provider_no=self.provider
        )
        payload = {"article_name": "Article2"}
        url = detail_url(article.article_no)
        self.client.patch(url, payload)

        article.refresh_from_db()
        self.assertEqual(article.article_name, payload["article_name"])

    def test_partial_update_article_invalid(self):
        """Test updating a article with invalid payload"""
        article = Article.objects.create(
            article_name="Article1", price=1234, provider_no=self.provider
        )
        payload = {"article_name": ""}
        url = detail_url(article.article_no)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_invalid_article(self):
        """Test updating invalid article"""
        payload = {"article_name": "Article1"}
        url = detail_url(999)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_full_update_article(self):
        """Test updating a article with put"""
        article = Article.objects.create(
            article_name="Article1", price=1234, provider_no=self.provider
        )
        payload = {
            "article_name": "Article2",
            "price": 4321,
            "provider_no": self.provider.provider_no,
        }
        url = detail_url(article.article_no)
        self.client.put(url, payload)

        article.refresh_from_db()
        self.assertEqual(article.article_name, payload["article_name"])
        self.assertEqual(article.price, payload["price"])

    def test_full_update_article_invalid(self):
        """Test updating a article with invalid payload"""
        article = Article.objects.create(
            article_name="Article1", price=1234, provider_no=self.provider
        )
        payload = {"article_name": "", "price": 4321}
        url = detail_url(article.article_no)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update_invalid_article(self):
        """Test updating invalid article"""
        payload = {"article_name": "Article1", "price": 4321}
        url = detail_url(999)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_article(self):
        """Test deleting a article"""
        article = Article.objects.create(
            article_name="Article1", price=1234, provider_no=self.provider
        )
        url = detail_url(article.article_no)
        self.client.delete(url)

        exists = Article.objects.filter(article_name=article.article_name).exists()
        self.assertFalse(exists)

    def test_delete_invalid_article(self):
        """Test deleting invalid article"""
        url = detail_url(999)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_filtering_by_min_and_max_price_only(self):
        """Test filtering articles by min and max price only"""
        create_many_articles(self.provider, 5)

        res = self.client.get(PRICE_FILTER_URL, {"min": 200, "max": 450})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_filtering_by_min_price_only(self):
        """Test filtering articles by min price only"""
        create_many_articles(self.provider, 5)

        res = self.client.get(PRICE_FILTER_URL, {"min": 200})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_filtering_by_max_price_only(self):
        """Test filtering articles by max price only"""
        create_many_articles(self.provider, 5)

        res = self.client.get(PRICE_FILTER_URL, {"max": 250})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
