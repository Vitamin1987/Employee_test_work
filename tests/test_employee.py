import pytest
from employee import Employee


def test_employee_calculate_payout():
    employee = Employee(
        id=1,
        email="alice@example.com",
        name="Alice Johnson",
        department="Marketing",
        hours_worked=160,
        hourly_rate=50
    )
    assert employee.calculate_payout() == 8000


def test_employee_negative_hours():
    with pytest.raises(ValueError):
        Employee(
            id=2,
            email="bob@example.com",
            name="Bob Smith",
            department="Design",
            hours_worked=-10,
            hourly_rate=40
        )