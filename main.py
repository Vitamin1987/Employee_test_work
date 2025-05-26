import argparse
import sys
import logging
import os
from typing import List, Dict, Any
from employee import Employee
from report import generate_report, REPORTS


# Кастомный action для проверки существования файлов
class FileExistsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for file_path in values:
            if not os.path.exists(file_path):
                raise argparse.ArgumentError(self, f"Файл {file_path} не найден")
        setattr(namespace, self.dest, values)


# Кастомное исключение для ошибок скрипта
class PayrollError(Exception):
    """Кастомное исключение для ошибок скрипта."""
    pass


# Настройка логирования
logging.basicConfig(
    filename='payroll.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из CSV-файла без использования библиотеки csv.
    Возвращает список словарей с данными сотрудников.
    """
    employees_data: List[Dict[str, Any]] = []
    required_fields: set[str] = {'id', 'email', 'name', 'department', 'hours_worked', 'hourly_rate'}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            headers: List[str] = f.readline().strip().split(',')
            if not headers:
                raise PayrollError(f"Файл {file_path} пустой или не содержит заголовков")
            header_set: set[str] = set(headers)

            if not required_fields.issubset(header_set):
                missing_fields = required_fields - header_set
                raise PayrollError(f"В файле {file_path} отсутствуют обязательные поля: {missing_fields}")

            for line_num, line in enumerate(f, start=2):
                values: List[str] = line.strip().split(',')
                if len(values) != len(headers):
                    raise PayrollError(f"Некорректный формат строки {line_num} в файле {file_path}")
                employee_data: Dict[str, Any] = dict(zip(headers, values))
                employees_data.append(employee_data)
        logging.info(f"Успешно прочитан файл {file_path}")
        return employees_data
    except PayrollError as e:
        logging.error(f"PayrollError: {e}")
        raise
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден")
        print(f"Ошибка: Файл {file_path} не найден.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        raise PayrollError(f"Неожиданная ошибка при чтении файла {file_path}: {e}")


def main() -> None:
    """Основная функция: парсит аргументы и формирует отчёт."""
    parser = argparse.ArgumentParser(description="Скрипт для формирования отчётов по сотрудникам.")
    parser.add_argument('files', nargs='+', action=FileExistsAction, help="Пути к CSV-файлам с данными сотрудников.")
    parser.add_argument('--report', required=True, choices=list(REPORTS.keys()), help="Тип отчёта (например, payout).")

    args = parser.parse_args()

    all_employees: List[Employee] = []
    for file_path in args.files:
        try:
            employees_data: List[Dict[str, Any]] = read_csv_file(file_path)
            for data in employees_data:
                try:
                    hours_worked = float(data['hours_worked'])
                    hourly_rate = float(data['hourly_rate'])

                    employee = Employee(
                        id=int(data['id']),
                        email=data['email'],
                        name=data['name'],
                        department=data['department'],
                        hours_worked=hours_worked,
                        hourly_rate=hourly_rate
                    )
                    all_employees.append(employee)
                except (KeyError, ValueError) as e:
                    logging.error(f"Ошибка в данных файла {file_path}: {e}")
                    raise PayrollError(f"Ошибка в данных файла {file_path}: {e}")
        except PayrollError as e:
            print(f"Ошибка: {e}")
            sys.exit(1)

    report_func = REPORTS[args.report]
    report_output: str = report_func.generate(all_employees)
    print(report_output)
    logging.info("Отчёт успешно сформирован")


if __name__ == "__main__":
    main()