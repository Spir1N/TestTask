import argparse
import json
from collections import defaultdict
from typing import List, Dict, Any

class EmployeeData:
    def __init__(self, file_paths: List[str]):
        self.employees = []
        self._load_data(file_paths)
    
    def _load_data(self, file_paths: List[str]):
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                headers = [h.strip() for h in lines[0].split(',')]
                
                for line in lines[1:]:
                    values = [v.strip() for v in line.split(',')]
                    employee = dict(zip(headers, values))
                    
                    # Нормализация назвнаий полей
                    employee['hourly_rate'] = float(
                        employee.get('hourly_rate') or 
                        employee.get('rate') or 
                        employee.get('salary')
                    )
                    
                    employee['hours_worked'] = float(employee['hours_worked'])
                    
                    self.employees.append(employee)

class ReportGenerator:
    @staticmethod
    def generate(report_type: str, employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        if report_type == 'payout':
            return PayoutReport.generate(employees)
        else:
            raise ValueError(f"Unknown report type: {report_type}")

class PayoutReport:
    @staticmethod
    def generate(employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        department_data = defaultdict(lambda: {
            'employees': [],
            'total_hours': 0,
            'total_payout': 0
        })
        
        for emp in employees:
            payout = emp['hours_worked'] * emp['hourly_rate']
            dept = emp['department']
            
            department_data[dept]['employees'].append({
                'name': emp['name'],
                'hours': emp['hours_worked'],
                'rate': emp['hourly_rate'],
                'payout': payout
            })
            
            department_data[dept]['total_hours'] += emp['hours_worked']
            department_data[dept]['total_payout'] += payout
        
        return dict(department_data)

def main():
    parser = argparse.ArgumentParser(description='Employee report generator')
    parser.add_argument('files', nargs='+', help='CSV files with employee data')
    parser.add_argument('--report', required=True, help='Type of report to generate')
    args = parser.parse_args()
    
    try:
        data = EmployeeData(args.files)
        report = ReportGenerator.generate(args.report, data.employees)
        print(json.dumps(report, indent=2))
        with open('payout.json', 'w') as file:
            json.dump(report, file, indent=2)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()