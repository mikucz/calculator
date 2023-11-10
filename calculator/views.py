from rest_framework import mixins, viewsets

from calculator.models import Operator
from calculator.serializers import OperatorSerializer


class OperatorViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    This endpoint represents currently available Operator types sorted by
    execution order.
    """

    queryset = Operator.objects.order_by_operator()
    serializer_class = OperatorSerializer
