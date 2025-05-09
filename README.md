# Employee Salary Calculation Script

Скрипт для генерации отчётов по зарплатам сотрудников на основе CSV-файлов. Поддерживает различные форматы входных данных и позволяет легко добавлять новые типы отчётов.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Spir1N/TestTask.git
   cd employee-reports
   ```

2. Установите зависимости для тестов:
   ```bash
   pip install pytest
   ```

## Использование

### Основной синтаксис
```bash
python main.py <файлы.csv> --report <тип_отчёта>
```

### Примеры запуска
1. **Отчёт по зарплатам (payout):**
   ```bash
   python main.py data1.csv data2.csv --report payout
   ```
   Вывод (JSON):
   ```json
   {
     "Design": {
       "employees": [
         {
           "name": "Bob Smith",
           "hours": 150,
           "rate": 40,
           "payout": 6000
         }
       ],
       "total_hours": 150,
       "total_payout": 6000
     }
   }
   ```

2. **Запуск с несколькими файлами:**
   ```bash
   python main.py *.csv --report payout
   ```

### Тестирование
```bash
pytest test_main.py -v
```

## Добавление новых отчётов

1. Создайте новый класс в `main.py` по образцу:
   ```python
   class CustomReport:
       @staticmethod
       def generate(employees: List[Dict[str, Any]]) -> Dict[str, Any]:
           # Ваша логика здесь
           return {"key": "value"}
   ```

2. Добавьте обработку в `ReportGenerator.generate()`:
   ```python
   if report_type == 'custom':
       return CustomReport.generate(employees)
   ```

3. Теперь можно вызывать:
   ```bash
   python main.py data.csv --report custom
   ```

## Поддерживаемые форматы CSV

Скрипт автоматически распознаёт столбцы с зарплатой, даже если они названы по-разному:
- `hourly_rate`
- `rate`
- `salary`

Пример CSV:
```csv
id,name,department,hours_worked,hourly_rate
1,Alice,Marketing,160,50
```

## Обработка ошибок

Скрипт проверяет:
- Наличие обязательного аргумента `--report`
- Корректность путей к CSV-файлам
- Соответствие структуры CSV ожидаемым полям

Пример ошибки:
```bash
Error: File not found: invalid.csv
```

## Пример вывода (payout)

Для данных:
```csv
name,department,hours_worked,hourly_rate
Alice,Marketing,160,50
Bob,Design,150,40
```

Вывод будет:
```json
{
  "Marketing": {
    "employees": [
      {
        "name": "Alice",
        "hours": 160,
        "rate": 50,
        "payout": 8000
      }
    ],
    "total_hours": 160,
    "total_payout": 8000
  },
  "Design": {
    ...
  }
}
```
