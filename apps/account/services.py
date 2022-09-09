from rest_framework.authtoken.models import Token

from low_level_services.interfaces.cache import AbstractCacheService
from .exceptions import BadRequest
from .models import Customer, User


class CustomerAuthService:
    def __init__(self, cache_service: AbstractCacheService):
        self.cache = cache_service

    def login(self, email, password):
        try:
            customer = Customer.objects.get(user__email=email)
            if customer.user.check_password(raw_password=password):
                token = Token.objects.create(user=customer.user)
                return token.key
            raise BadRequest('password is wrong')
        except Customer.DoesNotExist:
            raise BadRequest('user not found')

    def logout(self, token):
        raise NotImplementedError

    def create_customer(self):
        raise NotImplementedError


class CustomerService:
    pass
