from rest_framework import serializers


class CustomerAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(max_length=50, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=50, write_only=True, required=True)

