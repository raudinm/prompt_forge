from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import MagicMock
from forge.serializers import PromptSerializer, PromptEmbeddingSerializer, PromptMetadataSerializer


class PromptSerializerTest(TestCase):
    """Test cases for PromptSerializer"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_serializer_with_valid_data(self):
        """Test serializer with valid data"""
        data = {
            'text': 'Test prompt',
            'response': 'Test response'
        }
        serializer = PromptSerializer(
            data=data, context={'request': MagicMock(user=self.user)})
        self.assertTrue(serializer.is_valid())


class PromptEmbeddingSerializerTest(TestCase):
    """Test cases for PromptEmbeddingSerializer"""

    def test_embedding_serializer_valid_data(self):
        """Test embedding serializer with valid data"""
        data = {
            'model_name': 'text-embedding-3-small',
            'vector': [0.1, 0.2, 0.3, 0.4, 0.5]
        }
        serializer = PromptEmbeddingSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_embedding_serializer_empty_vector(self):
        """Test embedding serializer with empty vector"""
        data = {
            'model_name': 'text-embedding-3-small',
            'vector': []
        }
        serializer = PromptEmbeddingSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class PromptMetadataSerializerTest(TestCase):
    """Test cases for PromptMetadataSerializer"""

    def test_metadata_serializer_valid_data(self):
        """Test metadata serializer with valid data"""
        data = {
            'model_used': 'GPT-2',
            'sent_via_websocket': True,
            'extra_info': {'temperature': 0.7}
        }
        serializer = PromptMetadataSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_metadata_serializer_minimal_data(self):
        """Test metadata serializer with minimal data"""
        data = {
            'model_used': 'all-MiniLM-L6-v2'
        }
        serializer = PromptMetadataSerializer(data=data)
        self.assertTrue(serializer.is_valid())
