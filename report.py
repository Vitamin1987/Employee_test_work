from typing import List, Callable
from employee import Employee


def generate_payout_report(employees: List[Employee]) -> str:
    """
    Генерирует отчёт payout: список сотрудников с их зарплатами.
    Формат:
    Employee: Alice Johnson, Department: Marketing, Payout: $8000
    Employee: Bob Smith, Department: Design, Payout: $6000
    Total payout: $14000
    """
    output: List[str] = []
    total_payout: float = 0.0

    for employee in employees:
        payout: float = employee.calculate_payout()
        total_payout += payout
        line: str = (f"Employee: {employee.name}, "
                    f"Department: {employee.department}, "
                    f"Payout: ${payout:.0f}")
        output.append(line)

    output.append(f"Total payout: ${total_payout:.0f}")
    return "\n".join(output)


# Словарь для регистрации отчётов (для расширяемости)
REPORTS: dict[str, Callable[[List[Employee]], str]] = {
    "payout": generate_payout_report,
}


def generate_report(report_type: str, employees: List[Employee]) -> str:
    """Генерирует отчёт указанного типа."""
    if report_type not in REPORTS:
        raise ValueError(f"Неизвестный тип отчёта: {report_type}")
    return REPORTS[report_type](employees)