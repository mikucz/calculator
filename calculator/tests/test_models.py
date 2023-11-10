import operator

import pytest
from django.db import IntegrityError

from calculator.models import OPERATORS, Operator


@pytest.mark.django_db
def test_new_operator_not_specified():
    count = Operator.objects.count()
    with pytest.raises(IntegrityError):
        Operator.objects.create(operator="^")
        assert count == Operator.objects.count()


@pytest.mark.django_db
def test_create_exising_operator():
    exising = Operator.objects.first()
    with pytest.raises(IntegrityError):
        Operator.objects.create(operator=exising.operator)


@pytest.mark.django_db
def test_order_by_operator():
    Operator.objects.all().delete()
    operators = list(OPERATORS.keys())
    operators.reverse()
    Operator.objects.bulk_create([Operator(operator=op) for op in operators])
    assert list(Operator.objects.values_list("operator", flat=True)) == operators
    assert list(
        Operator.objects.order_by_operator().values_list("operator", flat=True)
    ) == list(OPERATORS.keys())


@pytest.mark.django_db
def test_operator_functions():
    Operator.objects.all().delete()
    Operator.objects.bulk_create([Operator(operator=op) for op in ("*", "-")])
    op_func = Operator.get_operator_functions()
    assert len(op_func.keys()) == 2
    assert op_func["*"] == operator.mul
    assert op_func["-"] == operator.sub
