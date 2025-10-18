from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.conf import settings


class JwtAuthMiddlewareTest(TestCase):
    """Test cases for JWT authentication middleware"""

    def setUp(self):
        from forge.middleware.jwt_auth import JwtAuthMiddleware
        self.middleware = JwtAuthMiddleware(MagicMock())
