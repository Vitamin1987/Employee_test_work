import pytest
from employee import Employee


@pytest.mark.parametrize("hours, rate, expected", [
    (160, 50, 8000),
    (150, 40, 6000),
    (170, 60, 10200),
])
def test_employee_calculate_payout(hours, rate, expected):
    employee = Employee(1, "test@example.com", "Test User", "Test", hours, rate)
    assert employee.calculate_payout() == expected


@pytest.mark.parametrize("hours, rate", [
    (-10, 40),
    (160, -50),
])
def test_employee_negative_values(hours, rate):
    with pytest.raises(ValueError):
        Employee(2, "test@example.com", "Test User", "Test", hours, rate)
