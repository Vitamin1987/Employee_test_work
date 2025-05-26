import pytest
from employee import Employee
from report import generate_report


@pytest.fixture
def sample_employees():
    return [
        Employee(1, "alice@example.com", "Alice Johnson", "Marketing", 160, 50),
        Employee(2, "bob@example.com", "Bob Smith", "Design", 150, 40),
    ]


def test_payout_report(sample_employees):
    report = generate_report("payout", sample_employees)
    expected = (
        "Employee: Alice Johnson    Department: Marketing    Payout: $8000\n"
        "Employee: Bob Smith        Department: Design       Payout: $6000\n"
        "Total payout: $14000"
    )
    assert report == expected


def test_payout_report_empty():
    report = generate_report("payout", [])
    assert report == "Total payout: $0"