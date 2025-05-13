import argparse
import sys
from typing import List, Dict, Any
from employee import Employee
from report import generate_report, REPORTS


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из CSV-файла без использования библиотеки csv.
    Возвращает список словарей с данными сотрудников.
    """
    employees_data: List[Dict[str, Any]] = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Читаем первую строку (заголовки)
            headers: List[str] = f.readline().strip().split(',')

            # Читаем остальные строки
            for line in f:
                values: List[str] = line.strip().split(',')
                if len(values) != len(headers):
                    raise ValueError(f"Некорректный формат строки в файле {file_path}")
                employee_data: Dict[str, Any] = dict(zip(headers, values))
                employees_data.append(employee_data)
        return employees_data
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        sys.exit(1)


def main() -> None:
    """Основная функция: парсит аргументы и формирует отчёт."""
    parser = argparse.ArgumentParser(description="Скрипт для формирования отчётов по сотрудникам.")
    parser.add_argument('files', nargs='+', help="Пути к CSV-файлам с данными сотрудников.")
    parser.add_argument('--report', required=True, help="Тип отчёта (например, payout).")

    args = parser.parse_args()

    # Проверяем, что указан существующий отчёт
    if args.report not in REPORTS:
        print(f"Ошибка: Неизвестный тип отчёта '{args.report}'. Доступные отчёты: {list(REPORTS.keys())}")
        sys.exit(1)

    # Читаем данные из всех файлов
    all_employees: List[Employee] = []
    for file_path in args.files:
        employees_data: List[Dict[str, Any]] = read_csv_file(file_path)
        for data in employees_data:
            try:
                employee = Employee(
                    id=int(data['id']),
                    email=data['email'],
                    name=data['name'],
                    department=data['department'],
                    hours_worked=float(data['hours_worked']),
                    hourly_rate=float(data['hourly_rate'])
                )
                all_employees.append(employee)
            except (KeyError, ValueError) as e:
                print(f"Ошибка в данных файла {file_path}: {e}")
                sys.exit(1)

    # Генерируем отчёт
    report_func = REPORTS[args.report]
    report_output: str = report_func(all_employees)
    print(report_output)


if __name__ == "__main__":
    main()