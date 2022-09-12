from django.db.models import Q
from rest_framework.authtoken.models import Token
import logging
from low_level_services.interfaces.cache import AbstractCacheService
from .dataclasses import CustomerRegisterRequest
from .exceptions import BadRequest
from .models import Customer, User
from apps.core.utils import correct_latin_number

logger = logging.getLogger(__name__)


class CustomerAuthService:
    def __init__(self, cache_service: AbstractCacheService):
        self.cache = cache_service

    def login(self, email, password):
        try:
            customer = Customer.objects.get(user__email=email)
            if customer.user.check_password(raw_password=password):
                token, created = Token.objects.get_or_create(user=customer.user)
                logger.info('Login successful')
                return token.key
            logger.debug('Password is wrong')
            raise BadRequest('login failed')
        except Customer.DoesNotExist:
            logger.debug('User not found')
            raise BadRequest('login failed')

    def logout(self, token):
        raise NotImplementedError

    def create_customer(self, customer: CustomerRegisterRequest) -> None:
        """
        gets a customer dataclass from views and creates a new customer if validations pass

        args: customer (CustomerRegisterRequest (dataclass))

        raises: BadRequest if validations fail or user with these credentials exists
        """
        mobile = self.validate_mobile_number(customer.phone_number)
        self.check_password(customer.password, customer.confirm_password)
        is_customer_existing = self.check_customer_exists(customer)
        if is_customer_existing:
            raise BadRequest('user already existing with these credentials')
        user = User.objects.create(email=customer.email, first_name=customer.first_name,
                                        last_name=customer.last_name)
        user.set_password(customer.password)
        user.save()
        customer = Customer.objects.create(user=user, phone_number=mobile)
        logger.debug(f'customer "{customer.phone_number}" created successfully')

    @staticmethod
    def validate_mobile_number(mobile: str) -> str:
        """
            gets unvalidated mobile number and validates it

            args: mobile (str)

            returns : validated mobile (str)

            raises : BadRequest if phone number is not valid
        """
        try:
            mobile = correct_latin_number(mobile)
            if len(mobile) != 11:
                raise BadRequest('phone no should be 11 characters')
            if not mobile.startswith('09'):
                raise BadRequest('phone no should start with 09')
            return mobile
        except ValueError as e:  # correct_latin_number may raise ValueError
            raise BadRequest('phone number should be numbers')

    @staticmethod
    def check_password(password: str, confirm: str) -> None:  # for customner registration
        if password != confirm:
            raise BadRequest('passwords does not match')
    @staticmethod
    def check_customer_e4xists(customer: CustomerRegisterRequest) -> bool:  # for customer registration
        return Customer.objects.filter(Q(user__email=customer.email) |
                                       Q(phone_number=customer.phone_number)).exists()


class CustomerService:
    pass
