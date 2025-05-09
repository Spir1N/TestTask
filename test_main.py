import pytest
from io import StringIO
from main import EmployeeData, PayoutReport, ReportGenerator

@pytest.fixture
def sample_csv_data():
    return StringIO("""id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
3,carol@example.com,Carol Williams,Design,170,60
""")

def test_employee_data_loading(tmp_path, sample_csv_data):
    file_path = tmp_path / "test.csv"
    file_path.write_text(sample_csv_data.getvalue())
    
    data = EmployeeData([str(file_path)])
    assert len(data.employees) == 3
    assert data.employees[0]['name'] == 'Alice Johnson'
    assert data.employees[1]['hourly_rate'] == 40.0

def test_payout_report_generation(tmp_path, sample_csv_data):
    file_path = tmp_path / "test.csv"
    file_path.write_text(sample_csv_data.getvalue())
    
    data = EmployeeData([str(file_path)])
    report = PayoutReport.generate(data.employees)
    
    assert 'Design' in report
    assert 'Marketing' in report
    assert report['Design']['total_payout'] == 150*40 + 170*60
    assert len(report['Design']['employees']) == 2

def test_report_generator():
    employees = [{
        'name': 'Test',
        'department': 'Test',
        'hours_worked': 10,
        'hourly_rate': 10
    }]
    
    report = ReportGenerator.generate('payout', employees)
    assert 'Test' in report
    assert report['Test']['total_payout'] == 100
    
    with pytest.raises(ValueError):
        ReportGenerator.generate('unknown', employees)