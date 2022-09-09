from rest_framework import serializers


class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(max_length=50, write_only=True, required=True)
