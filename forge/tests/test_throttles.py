from django.test import TestCase
from unittest.mock import patch, MagicMock
from forge.throttles import CustomBurstRateThrottle, CustomSustainedRateThrottle


class ThrottlesTest(TestCase):
    """Test cases for custom throttles"""

    def setUp(self):
        self.burst_throttle = CustomBurstRateThrottle()
        self.sustained_throttle = CustomSustainedRateThrottle()

    def test_burst_throttle_scope(self):
        """Test burst throttle scope"""
        self.assertEqual(self.burst_throttle.scope, 'burst')

    def test_sustained_throttle_scope(self):
        """Test sustained throttle scope"""
        self.assertEqual(self.sustained_throttle.scope, 'sustained')

    @patch('rest_framework.throttling.UserRateThrottle.allow_request')
    def test_burst_throttle_allow_request(self, mock_allow):
        """Test burst throttle allow_request method"""
        mock_allow.return_value = True
        request = MagicMock()
        view = MagicMock()

        result = self.burst_throttle.allow_request(request, view)
        self.assertTrue(result)
        mock_allow.assert_called_once_with(request, view)

    @patch('rest_framework.throttling.UserRateThrottle.allow_request')
    def test_sustained_throttle_allow_request(self, mock_allow):
        """Test sustained throttle allow_request method"""
        mock_allow.return_value = False
        request = MagicMock()
        view = MagicMock()

        result = self.sustained_throttle.allow_request(request, view)
        self.assertFalse(result)
        mock_allow.assert_called_once_with(request, view)
