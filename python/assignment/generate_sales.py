import csv
import random
from datetime import datetime, timedelta

def generate_sample_data(num_records=100, output_file='sales_data.csv'):
    # Danh sách sản phẩm mẫu
    products = ["Sản phẩm A", "Sản phẩm B", "Sản phẩm C", "Sản phẩm D", "Sản phẩm E"]
    # Tạo ngày bắt đầu (30 ngày trước)
    start_date = datetime.now() - timedelta(days=30)
    data = []
    for _ in range(num_records):
        # Sinh ngẫu nhiên ngày trong khoảng 30 ngày qua
        random_date = start_date + timedelta(days=random.randint(0, 30))
        date_str = random_date.strftime("%Y-%m-%d")
        product = random.choice(products)
        quantity = random.randint(1, 20)
        unit_price = random.randint(50, 500)  # Đơn giá (có thể tính theo đơn vị tiền tệ)
        revenue = quantity * unit_price
        data.append([date_str, product, quantity, unit_price, revenue])
        
    # Ghi dữ liệu vào file CSV
    header = ['date', 'product', 'quantity', 'unit_price', 'revenue']
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print(f"Đã tạo file dữ liệu mẫu: {output_file}")

if __name__ == "__main__":
    generate_sample_data()
