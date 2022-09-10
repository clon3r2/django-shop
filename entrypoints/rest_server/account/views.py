from rest_framework import views, response, viewsets, status
from apps.account.models import Customer
from .serializers import CustomerLoginSerializer, CustomerSerializer, CustomerRegisterRequestSerializer
from ...bootstrap import get_customer_auth_service
from apps.account.exceptions import BadRequest
from apps.account.dataclasses import CustomerRegisterRequest
from rest_framework import exceptions as drf_exceptions


class CustomerLoginView(views.APIView):
    serializer_class = CustomerLoginSerializer
    service = get_customer_auth_service()

    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            email = serializer_data.validated_data['email']
            password = serializer_data.validated_data['password']

            try:
                token = self.service.login(email=email, password=password)
                return response.Response({"token": token})
            except BadRequest as e:
                raise drf_exceptions.ParseError(e)


class CustomerRegisterView(views.APIView):
    serializer_class = CustomerRegisterRequestSerializer
    service = get_customer_auth_service()

    def post(self, request):
        try:
            serializer_data = self.serializer_class(data=request.data)
            if serializer_data.is_valid(raise_exception=True):
                customer = CustomerRegisterRequest(
                    email=serializer_data.validated_data['email'],
                    first_name=serializer_data.validated_data['first_name'],
                    last_name=serializer_data.validated_data['last_name'],
                    phone_number=serializer_data.validated_data['phone_number'],
                    password=serializer_data.validated_data['password'],
                    confirm_password=serializer_data.validated_data['confirm_password'],
                )
                self.service.create_customer(customer=customer)
                return response.Response(status=status.HTTP_200_OK)

        except BadRequest as e:
            raise drf_exceptions.ParseError(e)
