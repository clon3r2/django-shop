from rest_framework import views
from .serializers import CustomerAuthSerializer


class CustomerLoginView(views.APIView):
    serializer_class = CustomerAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            pass
