  
from datetime import datetime,timedelta
from collections import defaultdict
import math

def calculate_active_days(start_date, stop_date, target_month):
    target_start = datetime.strptime(target_month + "-01", "%Y-%m-%d")
    target_end = datetime.strptime(target_month + "-01", "%Y-%m-%d") + timedelta(days=32)
    target_end = target_end.replace(day=1) - timedelta(days=1)
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    stop_date = datetime.strptime(stop_date, "%Y-%m-%d")
    
    overlap_start = max(start_date, target_start)
    overlap_end = min(stop_date, target_end)
    
    if overlap_start <= overlap_end:
        return (overlap_end - overlap_start).days + 1
    return 0

def generate_monthly_bill(item_list, target_month):
    line_items = defaultdict(lambda: {'qty': 0, 'amount': 0.0, 'billing_period': "", 'item_code': "", 'rate': 0.0})

    total_revenue = 0.0

    for item in item_list:
        item_code = item['item_code']
        qty = int(item['qty'])
        rate = float(item['rate'])
        amount = float(item['amount'])
        start_date = item['start_date']
        stop_date = item['stop_date']
        
        active_days = calculate_active_days(start_date, stop_date, target_month)

        if active_days > 0:
            billing_period = f"{target_month}-01 to {target_month}-{"target_end.day"}"
            
            # Update the grouped line items dictionary
            line_items[(item_code, rate, billing_period)]['qty'] += qty
            line_items[(item_code, rate, billing_period)]['amount'] += rate * qty * active_days / 30.0
            line_items[(item_code, rate, billing_period)]['item_code'] = item_code
            line_items[(item_code, rate, billing_period)]['rate'] = rate
            line_items[(item_code, rate, billing_period)]['billing_period'] = billing_period

   
    final_line_items = []
    for key, value in line_items.items():
        if value['amount'] > 0: 
            final_line_items.append({
                "item_code": value['item_code'],
                "rate": value['rate'],
                "qty": value['qty'],
                "amount": value['amount'],
                "billing_period": value['billing_period']
            })
            total_revenue += value['amount']

    return {"line_items": final_line_items, "total_revenue": total_revenue}

item_list = [
    {"idx": 1, "item_code": "Executive Desk (4*2)", "sales_description": "Dedicated Executive Desk", "qty": 10, "rate": "1000", "amount": "10000", "start_date": "2023-11-01", "stop_date": "2024-10-17"},
    {"idx": 2, "item_code": "Executive Desk (4*2)", "qty": "10", "rate": "1080", "amount": "10800", "start_date": "2024-10-18", "stop_date": "2025-10-31"},
    {"idx": 3, "item_code": "Executive Desk (4*2)", "qty": 15, "rate": "1080", "amount": "16200", "start_date": "2024-11-01", "stop_date": "2025-10-31"},
    {"idx": 4, "item_code": "Executive Desk (4*2)", "qty": 5, "rate": "1000", "amount": "5000", "start_date": "2024-11-01", "stop_date": "2025-10-31"},
    {"idx": 5, "item_code": "Manager Cabin", "qty": 5, "rate": 5000, "amount": 25000, "start_date": "2024-11-01", "stop_date": "2025-10-31"},
    {"idx": 6, "item_code": "Manager Cabin", "qty": 7, "rate": "5000", "amount": "35000", "start_date": "2024-12-15", "stop_date": "2025-10-31"},
    {"idx": 7, "item_code": "Manager Cabin", "qty": 10, "rate": 4600, "amount": 46000, "start_date": "2023-11-01", "stop_date": "2024-10-17"},
    {"idx": 8, "item_code": "Parking (2S)", "qty": 10, "rate": 1000, "amount": 10000, "start_date": "2024-11-01", "stop_date": "2025-10-31"},
    {"idx": 9, "item_code": "Parking (2S)", "qty": 10, "rate": 0, "amount": 0, "start_date": "2024-11-01", "stop_date": "2025-10-31"},
    {"idx": 10, "item_code": "Executive Desk (4*2)", "qty": "8", "rate": "1100", "amount": "8800", "start_date": "2024-11-15", "stop_date": "2025-01-31"},
    {"idx": 11, "item_code": "Manager Cabin", "qty": "3", "rate": "5200", "amount": "15600", "start_date": "2024-10-10", "stop_date": "2024-11-10"},
    {"idx": 12, "item_code": "Conference Table", "qty": 1, "rate": "20000", "amount": "20000", "start_date": "2024-11-05", "stop_date": "2024-11-20"},
    {"idx": 13, "item_code": "Parking (2S)", "qty": 5, "rate": "1000", "amount": "5000", "start_date": "2024-11-15", "stop_date": "2025-02-28"},
    {"idx": 14, "item_code": "Reception Desk", "qty": 2, "rate": "7000", "amount": "14000", "start_date": "2024-11-01", "stop_date": "2025-03-31"},
    {"idx": 15, "item_code": "Reception Desk", "qty": 1, "rate": "7000", "amount": "7000", "start_date": "2024-11-10", "stop_date": "2024-11-25"},
    {"idx": 16, "item_code": "Breakout Area", "qty": 3, "rate": "3000", "amount": "9000", "start_date": "2024-01-01", "stop_date": "2024-01-31"}
]

target_month = "2024-11"
result = generate_monthly_bill(item_list, target_month)
print(result)
