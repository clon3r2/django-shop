from apps.account.services import CustomerAuthService
from low_level_services.cache import CacheService


def get_customer_auth_service(**kwargs):
    cache_service = kwargs.get('cache_service', CacheService(prefix='customer_'))
    return CustomerAuthService(cache_service=cache_service)
