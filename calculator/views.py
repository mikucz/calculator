from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, views, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from calculator.models import Operator
from calculator.serializers import CalculatorInput, CalculatorOutput, OperatorSerializer


class OperatorViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    This endpoint represents currently available Operator types sorted by
    execution order.
    """

    queryset = Operator.objects.order_by_operator()
    serializer_class = OperatorSerializer


class CalculatorView(views.APIView):
    """
    This endpoint allows to perform basic arithmetic operations.
    Supported operations available in appropriate /calculator/operators/ endpoint
    sorted by execution order.
    """

    @extend_schema(
        request=CalculatorInput, responses={status.HTTP_200_OK: CalculatorOutput}
    )
    def post(self, request):
        serializer = CalculatorInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_operators = Operator.get_operator_functions()

        operators = serializer.validated_data.get("operators")
        numbers = serializer.validated_data.get("numbers")

        # iterate over operators sorted by execution order
        # perform math operation and reduce list of provided numbers and operators
        # until that operation no longer exists
        # should reduce to 1 number
        for operator, func in db_operators.items():
            while operator in operators:
                i = operators.index(operator)
                result = func(numbers[i], numbers[i + 1])
                numbers[i] = result
                numbers.pop(i + 1)
                operators.pop(i)
        if len(numbers) > 1:
            raise APIException()
        decimal_places = CalculatorOutput._declared_fields["result"].decimal_places
        resp = CalculatorOutput(data={"result": round(numbers[0], decimal_places)})
        if not resp.is_valid():
            ValidationError
            raise ValidationError(
                {
                    "result": [
                        "Operation result out of range. Limit of "
                        f"{CalculatorOutput._declared_fields['result'].max_digits} "
                        "digits has been exceeded."
                    ]
                }
            )
        return Response(resp.data)
