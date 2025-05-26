# Скрипт подсчёта зарплаты сотрудников

Добро пожаловать в наш проект "Скрипт подсчёта зарплаты сотрудников"! Это консольное приложение на Python, которое читает данные сотрудников из CSV-файлов и генерирует отчёты, такие как выплаты. Мы сделали проект расширяемым, добавили тесты и обработку ошибок, чтобы он был надёжным и удобным. 😄

## Описание проекта

### Что делает скрипт?
- Читает данные сотрудников из одного или нескольких CSV-файлов.
- Генерирует отчёт `payout` с выровненным списком зарплат и общей суммой.
- Поддерживает добавление новых типов отчётов через объектно-ориентированный подход.
- Обрабатывает ошибки и записывает их в лог-файл `payroll.log`.

### Пример CSV-файла (`data1.csv`):
id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60

### Пример вывода отчёта `payout`:
Employee: Alice Johnson    Department: Marketing    Payout: $8000
Employee: Bob Smith        Department: Design       Payout: $6000
Employee: Carol Williams   Department: Design       Payout: $10200
Total payout: $24200


## Требования

### Функциональные требования:
- Скрипт принимает пути к CSV-файлам через аргументы командной строки.
- Тип отчёта задаётся с помощью `--report` (сейчас поддерживается только `payout`).
- Валидация аргументов выполняется с помощью `argparse` (с использованием `choices` и кастомного `action`).

### Нефункциональные требования:
- Использует стандартные библиотеки Python (кроме тестов: `pytest`, `flake8`).
- Код соответствует стандартам PEP 8 и использует аннотации типов.
- Покрыт тестами с параметризацией (`pytest.mark.parametrize`).

### Дополнительные возможности:
- Проверка существования файлов и корректности данных.
- Логирование ошибок и событий в `payroll.log`.
- Расширяемость через абстрактный класс `Report` и словарь `REPORTS`.

## Структура проекта
pythonProject/
├── main.py               # Главный скрипт с обработкой аргументов и логированием
├── employee.py           # Класс Employee с валидацией данных
├── report.py             # Модуль отчётов с ООП (абстрактный класс Report)
├── tests/                # Папка с тестами
│   ├── test_employee.py  # Тесты для Employee (включая параметризацию)
│   ├── test_main.py      # Тесты для обработки CSV
│   └── test_report.py    # Тесты для отчётов
├── data1.csv             # Пример CSV-файла
├── requirements.txt      # Зависимости (pytest, flake8)
├── .gitignore            # Игнорирование ненужных файлов
└── README.md             # Эта документация

### Описание файлов:
- **`main.py`**: Точка входа, парсит аргументы, читает CSV и генерирует отчёты. Использует кастомное исключение `PayrollError`.
- **`employee.py`**: Класс `Employee` с атрибутами (id, email, name, department, hours_worked, hourly_rate) и методом `calculate_payout`.
- **`report.py`**: Содержит абстрактный класс `Report` и класс `PayoutReport` для генерации отчётов.
- **`tests/`**: Папка с тестами, покрывающими ключевые функции.

## Установка

1. Убедись, что установлен Python 3.11.9 или новее.
2. Склонируй репозиторий:
git clone <твой-репозиторий>
cd pythonProject
3. Создай виртуальное окружение (опционально):
python -m venv .venv
.venv\Scripts\activate  # Windows
4. Установи зависимости:
pip install -r requirements.txt

## Запуск

1. Подготовь CSV-файл с данными (например, `data1.csv`).
2. Запусти скрипт:
python main.py data1.csv --report payout


### Аргументы командной строки:
- `files`: Путь(и) к CSV-файлам (обязательно, можно указать несколько через пробел, проверка существования через `FileExistsAction`).
- `--report`: Тип отчёта (обязательно, поддерживается `payout`, валидация через `choices`).

Пример с несколькими файлами:
python main.py data1.csv data2.csv --report payout

## Тестирование

Проект покрыт 9 тестами с использованием `pytest`. Чтобы запустить тесты:
1. Убедись, что зависимости установлены.
2. Выполни команду:
python -m pytest tests/
Ожидаемый вывод:
collected 9 items

tests\test_employee.py .....                                                   [ 55%]
tests\test_main.py ..                                                          [ 77%]
tests\test_report.py ..                                                        [100%]
=============================== 9 passed in 0.11s ===============================


## Расширение функционала

### Добавление нового отчёта
Проект построен с использованием ООП. Чтобы добавить новый тип отчёта (например, средняя ставка по отделам):
1. Создай новый класс в `report.py`, наследующийся от `Report`:
```python
class AverageRateReport(Report):
    def generate(self, employees: List[Employee]) -> str:
        if not employees:
            return "No data for average rate."
        departments: Dict[str, List[float]] = {}
        for emp in employees:
            if emp.department not in departments:
                departments[emp.department] = []
            departments[emp.department].append(emp.hourly_rate)
        output = []
        for dept, rates in departments.items():
            avg_rate = sum(rates) / len(rates)
            output.append(f"Department: {dept}, Average Hourly Rate: ${avg_rate:.2f}")
        return "\n".join(output)

2. Зарегистрируй новый отчёт в REPORTS
REPORTS["average_rate"] = AverageRateReport()

3. Используй новый отчёт:
python main.py data1.csv --report average_rate

Обработка ошибок
Скрипт обрабатывает:
Несуществующие файлы: Выводит сообщение и завершает работу.
Ошибка: Файл nonexistent.csv не найден.

Неверный тип отчёта: Показывает доступные варианты.
usage: main.py [-h] [--report {payout}] files [files ...]
main.py: error: argument --report: invalid choice: 'invalid' (choose from 'payout')
Некорректные данные: Вызывает PayrollError (например, отрицательные часы или отсутствие полей).
 Логи записываются в payroll.log.

Ограничения и улучшения
Ограничения:
Поддерживается только отчёт payout.
CSV-файлы должны быть валидными (правильное количество колонок).
Возможные улучшения:
Поддержка JSON или других форматов данных.
Дополнительные отчёты (например, статистика по отделам).
Улучшенное форматирование отчётов (таблицы).
Более детальное логирование.
