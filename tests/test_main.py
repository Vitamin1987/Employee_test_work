import pytest

from main import read_csv_file, PayrollError


def test_read_csv_file_missing_field(tmp_path):
    # Создаём временный CSV-файл с отсутствующим полем
    csv_content = "id,email,name,department,hours_worked\n1,alice@example.com,Alice Johnson,Marketing,160"
    file_path = tmp_path / "invalid.csv"
    file_path.write_text(csv_content, encoding='utf-8')

    with pytest.raises(PayrollError, match="отсутствуют обязательные поля"):
        read_csv_file(str(file_path))


def test_read_csv_file_invalid_format(tmp_path):
    # Создаём временный CSV-файл с некорректным количеством полей
    csv_content = "id,email,name,department,hours_worked,hourly_rate\n1,alice@example.com,Alice Johnson,Marketing,160"
    file_path = tmp_path / "invalid_format.csv"
    file_path.write_text(csv_content, encoding='utf-8')

    with pytest.raises(PayrollError, match="Некорректный формат строки"):
        read_csv_file(str(file_path))
