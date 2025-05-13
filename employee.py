from dataclasses import dataclass


@dataclass
class Employee:
    """Класс, представляющий сотрудника."""
    id: int
    email: str
    name: str
    department: str
    hours_worked: float
    hourly_rate: float

    def __post_init__(self) -> None:
        """Проверяет данные после создания объекта."""
        if self.hours_worked < 0:
            raise ValueError("Количество отработанных часов не может быть отрицательным")
        if self.hourly_rate < 0:
            raise ValueError("Часовая ставка не может быть отрицательной")

    def calculate_payout(self) -> float:
        """Рассчитывает зарплату сотрудника."""
        return self.hours_worked * self.hourly_rate