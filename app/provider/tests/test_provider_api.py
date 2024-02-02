"""
Test for provider apis.
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Provider

from provider.serializers import ProviderSerializer


provider_URL = reverse("provider:provider-list")


def detail_url(provider_id):
    """Return provider detail URL"""
    return reverse("provider:provider-detail", args=[provider_id])


class ProviderApiTests(TestCase):
    """Test the provider API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_provider_list(self):
        """Test retrieving a list of provider"""
        Provider.objects.create(provider_name="Provider1")
        Provider.objects.create(provider_name="Provider2")

        res = self.client.get(provider_URL)

        provider = Provider.objects.all().order_by("-provider_no")
        serializer = ProviderSerializer(provider, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_provider_detail(self):
        """Test retrieving a provider detail"""
        provider = Provider.objects.create(provider_name="Provider1")
        url = detail_url(provider.provider_no)
        res = self.client.get(url)

        serializer = ProviderSerializer(provider)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_invalid_provider_detail(self):
        """Test retrieving a invalid provider detail"""
        url = detail_url(999)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_provider(self):
        """Test creating provider"""
        payload = {"provider_name": "Provider1"}
        self.client.post(provider_URL, payload)

        exists = Provider.objects.filter(
            provider_name=payload["provider_name"]
        ).exists()
        self.assertTrue(exists)

    def test_create_provider_duplicate(self):
        """Test creating provider with duplicate name"""
        payload = {"provider_name": "Provider1"}
        self.client.post(provider_URL, payload)
        res = self.client.post(provider_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_provider_invalid(self):
        """Test creating new provider with invalid payload"""
        payload = {"provider_name": ""}
        res = self.client.post(provider_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_provider(self):
        """Test updating provider with patch"""
        provider = Provider.objects.create(provider_name="Provider1")
        payload = {"provider_name": "Provider2"}
        url = detail_url(provider.provider_no)
        self.client.patch(url, payload)

        provider.refresh_from_db()
        self.assertEqual(provider.provider_name, payload["provider_name"])

    def test_update_provider_invalid(self):
        """Test updating provider with invalid payload"""
        provider = Provider.objects.create(provider_name="Provider1")
        payload = {"provider_name": ""}
        url = detail_url(provider.provider_no)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_provider(self):
        """Test updating invalid provider"""
        payload = {"provider_name": "Provider1"}
        url = detail_url(999)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_provider(self):
        """Test deleting provider"""
        provider = Provider.objects.create(provider_name="Provider1")
        url = detail_url(provider.provider_no)
        self.client.delete(url)

        exists = Provider.objects.filter(provider_name=provider.provider_name).exists()
        self.assertFalse(exists)

    def test_delete_invalid_provider(self):
        """Test deleting invalid provider"""
        url = detail_url(999)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
