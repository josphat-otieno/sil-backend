from rest_framework import serializers
from .models import Customer
import re

class UpdateCustomerPhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True) 

    class Meta:
        model = Customer
        fields = ["phone"]

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        if not re.match(r"^2547\d{8}$", value):
            raise serializers.ValidationError("Phone must be in format 2547XXXXXXXX")
        return value