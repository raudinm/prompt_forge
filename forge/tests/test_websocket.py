from django.test import TestCase
from unittest.mock import patch, MagicMock


class WebSocketUtilsTest(TestCase):
    """Test cases for WebSocket utilities"""


class PromptConsumerTest(TestCase):
    """Test cases for PromptConsumer WebSocket consumer"""

    def setUp(self):
        self.consumer = None  # Will be set in individual tests

    @patch('forge.consumer.AsyncWebsocketConsumer.__init__')
    def test_consumer_initialization(self, mock_init):
        """Test consumer initialization"""
        from forge.consumer import PromptConsumer
        scope = {'user': MagicMock()}
        consumer = PromptConsumer(scope)
        mock_init.assert_called_once_with(scope)
