# BAI 1
employees = []

def add_employee(name):
    employees.append(name)
    print(f"Đã thêm nhân viên: {name}")

def remove_employee(name):
    if name in employees:
        employees.remove(name)
        print(f"Đã xóa nhân viên: {name}")
    else:
        print("Nhân viên không tồn tại!")

def list_employees():
    print("Danh sách nhân viên:")
    for emp in employees:
        print("-", emp)

# Test chương trình
add_employee("Nguyễn Văn A")
add_employee("Trần Thị B")
list_employees()
remove_employee("Nguyễn Văn A")
list_employees()



#BAI 2
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

prime_numbers = tuple(n for n in range(1, 51) if is_prime(n))
print("Danh sách số nguyên tố:", prime_numbers)



#Bai 3
products = set()

def add_product(name):
    products.add(name)
    print(f"Đã thêm sản phẩm: {name}")

def list_products():
    print("Danh sách sản phẩm:")
    for product in products:
        print("-", product)

# Test chương trình
add_product("Bánh mì")
add_product("Sữa tươi")
add_product("Bánh mì")  # Không bị trùng
list_products()



#BAI 4
students = [("An", 8.5), ("Bình", 9.0), ("Châu", 7.5), ("Dũng", 8.0)]

students.sort(key=lambda x: x[1], reverse=True)

print("Danh sách học sinh theo điểm:")
for name, score in students:
    print(name, "-", score)



#BAI 5
# text = input("Nhập đoạn văn: ").lower()
# words = text.split()
# word_count = {}

# for word in words:
#     word_count[word] = word_count.get(word, 0) + 1

# print("Số lần xuất hiện của từng từ:")
# for word, count in word_count.items():
#     print(word, "-", count)





#BAI 6
access_logs = [
    "192.168.1.1", "192.168.1.2", "192.168.1.1", "192.168.1.3", "192.168.1.2"
]

unique_ips = set(access_logs)
print("Danh sách IP duy nhất:", unique_ips)





#BAI 7 
from collections import deque

queue = deque()

def add_customer(name):
    queue.append(name)
    print(f"Khách hàng {name} đã vào hàng đợi.")

def serve_customer():
    if queue:
        name = queue.popleft()
        print(f"Đang phục vụ: {name}")
    else:
        print("Hàng đợi trống!")

# Test chương trình
add_customer("Minh")
add_customer("Lan")
serve_customer()
serve_customer()
serve_customer()


#BAI 8
tasks = [("Làm bài tập", 2), ("Đi siêu thị", 3), ("Họp nhóm", 1)]

tasks.sort(key=lambda x: x[1])

print("Danh sách công việc theo mức độ ưu tiên:")
for task, priority in tasks:
    print(priority, "-", task)





#BAI 9
students = [("An", 8.5), ("Bình", 9.0), ("Châu", 7.5)]
student_dict = dict(students)

print("Từ điển học sinh:", student_dict)


#BAIA 10:
sold_products = ["Sữa", "Bánh mì", "Sữa", "Bánh", "Sữa", "Bánh mì"]

product_count = {}

for product in sold_products:
    product_count[product] = product_count.get(product, 0) + 1

print("Số lượng sản phẩm bán ra:")
for product, count in product_count.items():
    print(product, "-", count)
