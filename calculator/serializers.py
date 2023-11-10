from django.core.exceptions import ValidationError
from rest_framework import serializers

from calculator.models import OPERATORS, Operator


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("operator",)


class CalculatorInput(serializers.Serializer):
    numbers = serializers.ListField(
        child=serializers.DecimalField(
            max_digits=10, decimal_places=5, coerce_to_string=False
        ),
        min_length=2,
        max_length=2,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamicly create operators field with max_length=numbers.max_length-1
        self.fields["operators"] = serializers.ListField(
            child=serializers.ChoiceField(
                choices=[(op_char, label) for op_char, (_, label) in OPERATORS.items()],
            ),
            min_length=1,
            max_length=self.fields["numbers"].max_length - 1,
        )

    def validate(self, attrs: any) -> any:
        validated = super().validate(attrs)
        if len(validated.get("operators")) != len(validated.get("numbers")) - 1:
            raise ValidationError(
                "Count of operators must equals to count of numbers-1"
            )
        return validated


class CalculatorOutput(serializers.Serializer):
    result = serializers.DecimalField(
        max_digits=20, decimal_places=5, coerce_to_string=False
    )
