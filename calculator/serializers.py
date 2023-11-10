from rest_framework import serializers

from calculator.models import Operator


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("operator",)
