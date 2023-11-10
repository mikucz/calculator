import operator
from functools import reduce

import pytest
from rest_framework.test import APIClient

from calculator.models import Operator
from calculator.serializers import CalculatorInput


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_single_operators(api_client):
    equantion_numbers = 2
    numbers = [i for i in range(1, equantion_numbers + 1)]
    for op, func in (
        ("+", operator.add),
        ("-", operator.sub),
        ("/", operator.truediv),
        ("*", operator.mul),
    ):
        data = {
            "numbers": numbers,
            "operators": [op for _ in range(equantion_numbers - 1)],
        }

        resp = api_client.post("/api/v1/calculator/", data, format="json")
        assert resp.status_code == 200
        result = reduce(func, data["numbers"])
        assert resp.json().get("result") == pytest.approx(result, 0.0001)


@pytest.mark.django_db
def test_too_many_operators(api_client):
    numbers = CalculatorInput._declared_fields["numbers"].max_length
    data = {
        "numbers": [i for i in range(numbers)],
        "operators": ["+" for _ in range(numbers)],
    }

    resp = api_client.post("/api/v1/calculator/", data, format="json")
    assert resp.status_code == 400
    assert "operators" in resp.json()


@pytest.mark.django_db
def test_too_many_numbers(api_client):
    numbers_limit = CalculatorInput._declared_fields["numbers"].max_length
    data = {
        "numbers": [i for i in range(numbers_limit + 1)],
        "operators": ["+" for _ in range(numbers_limit - 1)],
    }

    resp = api_client.post("/api/v1/calculator/", data, format="json")
    assert resp.status_code == 400
    assert "numbers" in resp.json()


@pytest.mark.django_db
def test_wrong_operator(api_client):
    assert not Operator.objects.filter(operator="%").exists()
    data = {
        "numbers": [1, 2],
        "operators": ["%"],
    }
    resp = api_client.post("/api/v1/calculator/", data, format="json")
    assert resp.status_code == 400
    assert "operators" in resp.json()


@pytest.mark.django_db
def test_wrong_number(api_client):
    assert not Operator.objects.filter(operator="%").exists()
    data = {
        "numbers": [1, "a"],
        "operators": ["+"],
    }
    resp = api_client.post("/api/v1/calculator/", data, format="json")
    assert resp.status_code == 400
    assert "numbers" in resp.json()
