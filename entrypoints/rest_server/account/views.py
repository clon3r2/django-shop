from rest_framework import views, response
from .serializers import CustomerLoginSerializer
from ...bootstrap import get_customer_auth_service
from apps.account.exceptions import BadRequest
from rest_framework import exceptions as drf_exceptions


class CustomerLoginView(views.APIView):
    serializer_class = CustomerLoginSerializer
    service = get_customer_auth_service()

    def post(self, request, *args, **kwargs):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            email = serializer_data.validated_data['email']
            password = serializer_data.validated_data['password']

            try:
                token = self.service.login(email=email, password=password)
                return response.Response({"token": token})
            except BadRequest as e:
                raise drf_exceptions.ParseError(e)
