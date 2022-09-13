from rest_framework import serializers
import bleach

from apps.account.models import Customer


class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(max_length=50, write_only=True, required=True)

    def validate_password(self, value):
        if isinstance(value, str):
            return bleach.clean(value)

    def validate_email(self, value):
        if isinstance(value, str):
            return bleach.clean(value)


class CustomerRegisterRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=50, write_only=True, required=True)

    def validate_password(self, value):
        if isinstance(value, str):
            return bleach.clean(value)

    def validate_email(self, value):
        if isinstance(value, str):
            return bleach.clean(value)

    def validate_confirm_password(self, value):
        if isinstance(value, str):
            return bleach.clean(value)

    def validate_first_name(self, value):
        if isinstance(value, str):
            return bleach.clean(value)

    def validate_last_name(self, value):
        if isinstance(value, str):
            return bleach.clean(value)

    def validate_phone_number(self, value):
        if isinstance(value, str):
            return bleach.clean(value)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
