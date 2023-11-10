import operator
from collections import OrderedDict
from collections.abc import Callable

from django.db import models

# All operations will be executed in same order as order of OPERATORS
OPERATORS: OrderedDict[str, tuple[Callable, str]] = OrderedDict(
    [
        ("*", (operator.mul, "MULTIPLICATION")),
        ("/", (operator.truediv, "DIVISION")),
        ("+", (operator.add, "ADDITION")),
        ("-", (operator.sub, "SUBTRACTION")),
    ]
)


class OperatorQuerySet(models.QuerySet):
    def order_by_operator(self):
        return self.annotate(
            operator_order=models.Case(
                *[
                    models.When(operator=o, then=models.Value(i))
                    for i, o in enumerate(OPERATORS.keys(), 1)
                ],
                default=models.Value(1),
                output_field=models.IntegerField(),
            )
        ).order_by("operator_order")


class Operator(models.Model):
    operator = models.CharField(
        max_length=1,
        choices=[(op_char, label) for op_char, (_, label) in OPERATORS.items()],
        unique=True,
    )
    objects = OperatorQuerySet.as_manager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="operator_valid",
                check=models.Q(operator__in=list(OPERATORS.keys())),
            )
        ]

    def __str__(self):
        return self.operator

    @staticmethod
    def get_operator_functions() -> OrderedDict[str, Callable]:
        """Get all operators from db with corresponding math functions

        Returns:
            list[tuple(str, Callable)] - where str is operator char (OperatorOptions),
                and Callable is math function that takes 2 number args
        """
        operators = Operator.objects.order_by_operator().values_list(
            "operator", flat=True
        )
        return OrderedDict([(o, OPERATORS[o][0]) for o in operators])
