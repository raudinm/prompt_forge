from rest_framework.throttling import UserRateThrottle


class CustomBurstRateThrottle(UserRateThrottle):
    """
    Allows 1 API call per second per user.
    Used to prevent rapid repeated submissions.
    """
    scope = 'burst'


class CustomSustainedRateThrottle(UserRateThrottle):
    """
    Allows 10 API calls per minute per user.
    Used to limit overall usage over time.
    """
    scope = 'sustained'
