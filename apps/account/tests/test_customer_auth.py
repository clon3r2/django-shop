from .fake_modules import FakeCacheService
from entrypoints.bootstrap import get_customer_auth_service
from django.test import TestCase
from apps.account.dataclasses import CustomerRegisterRequest
from apps.account.models import User, Customer


class CustomerAuthTestCase(TestCase):
    def setUp(self) -> None:
        self.password_1 = '123456'
        self.phone_number_valid_1 = "09123456789"
        self.phone_number_valid_2 = "۰۹۱۲۳۴۵۶۷۸۹"
        self.phone_number_invalid_1 = "3456789"
        self.phone_number_invalid_2 = "hello"
        self.email_1 = 'test1@test.com'
        self.email_2 = 'test2@test.com'
        self.email_3 = 'test3@test.com'
        self.cache = FakeCacheService(prefix="customer_")
        self.service = get_customer_auth_service(cache_service=self.cache)
        self.customer_reg_req_valid_1 = CustomerRegisterRequest(email=self.email_1, first_name='fn1',
                                                                last_name='ln1', phone_number=self.phone_number_valid_1,
                                                                password=self.password_1,
                                                                confirm_password=self.password_1)
        self.customer_reg_req_valid_2 = CustomerRegisterRequest(email=self.email_2, first_name='fn2',
                                                                last_name='ln2', phone_number=self.phone_number_valid_2,
                                                                password=self.password_1,
                                                                confirm_password=self.password_1)
        # self.customer_reg_req_valid_3 = CustomerRegisterRequest(email=self.email_3, first_name='fn1',
        #                                                 last_name='ln1', phone_number=self.phone_number_valid_2,
        #                                                 password=self.password_1, confirm_password=self.password_1)

    def test_happy_register(self):
        self.service.create_customer(customer=self.customer_reg_req_valid_1)
        customer = Customer.objects.get(user__email=self.email_1)
        self.assertEqual(customer.user.first_name, 'fn1')
        self.assertEqual(customer.user.last_name, 'ln1')
        self.assertEqual(customer.phone_number, self.phone_number_valid_1)
        self.assertEqual(len(Customer.objects.all()), 1)
        self.assertEqual(len(User.objects.all()), 1)
