from abc import ABC, abstractmethod
from typing import List
from employee import Employee


class Report(ABC):
    """Абстрактный класс для отчётов."""
    @abstractmethod
    def generate(self, employees: List[Employee]) -> str:
        """Генерирует отчёт."""
        pass


class PayoutReport(Report):
    """Отчёт по выплатам сотрудников."""
    def generate(self, employees: List[Employee]) -> str:
        """
        Генерирует отчёт payout: список сотрудников с их зарплатами.
        Формат с выравниванием:
        Employee: Alice Johnson    Department: Marketing    Payout: $8000
        """
        output: List[str] = []
        total_payout: float = 0.0

        if not employees:
            return "Total payout: $0"

        max_name_length: int = max(len(emp.name) for emp in employees)
        max_dept_length: int = max(len(emp.department) for emp in employees)

        for employee in employees:
            payout: float = employee.calculate_payout()
            total_payout += payout
            name_field: str = f"{employee.name:<{max_name_length}}"
            dept_field: str = f"{employee.department:<{max_dept_length}}"
            line: str = (f"Employee: {name_field}    Department: {dept_field}    Payout: ${payout:.0f}")
            output.append(line)

        output.append(f"Total payout: ${total_payout:.0f}")
        return "\n".join(output)


# Словарь для регистрации отчётов
REPORTS: dict[str, Report] = {
    "payout": PayoutReport(),
}

def generate_report(report_type: str, employees: List[Employee]) -> str:
    """Генерирует отчёт указанного типа."""
    if report_type not in REPORTS:
        raise ValueError(f"Неизвестный тип отчёта: {report_type}")
    return REPORTS[report_type].generate(employees)