a = int(input("Nhap so thu nhat: "))
b = int(input("Nhap so thu hai: "))
tong = a + b
print(tong)


a = int(input("Nhap so nguyen bat ki: "))
if(a % 2 == 0) :
    print(a, "la so chan")
else :
    print(a1, "la so le?")

a = float(input("Nhap chieu dai: "))
b = float(input("Nhap chieu rong: "))
S = (a+b)*2
print(S)


def is_prime(n):
    if n < 2 :
        return False
    for i in range(2, int(n**0.5) + 1) :
        if n % i == 0 :
            return False
    return True
n = int(input("Nhap so nguyen to bat ki: "))
if is_prime(n) :
    print(n, "La so nguyen to") 
else: 
    print(n, "khong la so nguyen to")  



a = int(input(" Nhap so bat ki: "))
if a % 3 == 0:
    print(a, "chia het cho 3")
else: 
    print(a, "khong chia het cho 3")


def kiem_tra_so_doi_xung(n):
    so_goc = n  
    dao_nguoc = 0
    while n > 0:
        dao_nguoc = dao_nguoc * 10 + n % 10  
        n //= 10  
    return so_goc == dao_nguoc
n = int(input("Nhập một số: "))
if kiem_tra_so_doi_xung(n):
    print(f"{n} là số đối xứng.")
else:
    print(f"{n} không phải là số đối xứng.")


name = str(input("Nhap ten cua ban : "))
print("Xin chao!", name)



def check_year(year): 
    if year % 400 == 0:
        return True
    return False
year = int(input("Nhap nam :"))
if check_year(year):
    print(year, "la nam nhuan")
else:
    print(year, "khong phai nam nhuan")
 
 
 
10 
def check_max(a, b, c): 
    if a > b and a > c: 
        return a
    if b > c and b > a: 
        return b
    else:
        return c
    
