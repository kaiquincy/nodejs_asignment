import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pymongo import MongoClient
from datetime import datetime, date

# Kết nối tới MongoDB
def connect_to_mongodb():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client.medical_service  # sử dụng cơ sở dữ liệu "medical_service"
        return db
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới MongoDB:\n{e}")
        return None

db = connect_to_mongodb()
if db is None:
    exit()

# Các collection
patients_col = db.patients
doctors_col = db.doctors
appointments_col = db.appointments

# Cập nhật danh sách bệnh nhân và bác sĩ cho tab cuộc hẹn
def update_patient_list():
    patients = list(patients_col.find())
    patient_options = []
    for p in patients:
        display = f"{p['full_name']} ({str(p['_id'])[-6:]})"
        patient_options.append((display, p['_id']))
    return patient_options

def update_doctor_list():
    doctors = list(doctors_col.find())
    doctor_options = []
    for d in doctors:
        display = f"{d['full_name']} ({str(d['_id'])[-6:]})"
        doctor_options.append((display, d['_id']))
    return doctor_options

# Hàm thêm bệnh nhân
def add_patient():
    full_name = patient_name_entry.get().strip()
    dob_str = patient_dob_entry.get().strip()
    gender = patient_gender_entry.get().strip()
    address = patient_address_entry.get().strip()
    phone = patient_phone_entry.get().strip()
    email = patient_email_entry.get().strip()
    
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
    except Exception as e:
        messagebox.showerror("Lỗi định dạng", "Ngày sinh phải có định dạng YYYY-MM-DD")
        return
    
    patient = {
        "full_name": full_name,
        "date_of_birth": dob,
        "gender": gender,
        "address": address,
        "phone_number": phone,
        "email": email
    }
    
    try:
        result = patients_col.insert_one(patient)
        messagebox.showinfo("Thành công", f"Thêm bệnh nhân thành công. ID: {result.inserted_id}")
        patient_name_entry.delete(0, tk.END)
        patient_dob_entry.delete(0, tk.END)
        patient_gender_entry.delete(0, tk.END)
        patient_address_entry.delete(0, tk.END)
        patient_phone_entry.delete(0, tk.END)
        patient_email_entry.delete(0, tk.END)
        refresh_appointment_dropdowns()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm bệnh nhân:\n{e}")

# Hàm thêm bác sĩ
def add_doctor():
    full_name = doctor_name_entry.get().strip()
    specialization = doctor_spec_entry.get().strip()
    phone = doctor_phone_entry.get().strip()
    email = doctor_email_entry.get().strip()
    try:
        years_exp = int(doctor_exp_entry.get().strip())
    except:
        messagebox.showerror("Lỗi", "Năm kinh nghiệm phải là số nguyên.")
        return

    doctor = {
        "full_name": full_name,
        "specialization": specialization,
        "phone_number": phone,
        "email": email,
        "years_of_experience": years_exp
    }
    
    try:
        result = doctors_col.insert_one(doctor)
        messagebox.showinfo("Thành công", f"Thêm bác sĩ thành công. ID: {result.inserted_id}")
        doctor_name_entry.delete(0, tk.END)
        doctor_spec_entry.delete(0, tk.END)
        doctor_phone_entry.delete(0, tk.END)
        doctor_email_entry.delete(0, tk.END)
        doctor_exp_entry.delete(0, tk.END)
        refresh_appointment_dropdowns()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm bác sĩ:\n{e}")

# Hàm thêm cuộc hẹn
def add_appointment():
    patient_selection = patient_combo.get()
    doctor_selection = doctor_combo.get()
    if not patient_selection or not doctor_selection:
        messagebox.showerror("Lỗi", "Vui lòng chọn bệnh nhân và bác sĩ.")
        return
    
    patient_id = patient_dict.get(patient_selection)
    doctor_id = doctor_dict.get(doctor_selection)
    
    date_str = appointment_date_entry.get().strip()
    reason = appointment_reason_entry.get().strip()
    try:
        app_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        messagebox.showerror("Lỗi định dạng", "Ngày giờ hẹn phải có định dạng YYYY-MM-DD HH:MM:SS")
        return
    
    appointment = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": app_date,
        "reason": reason,
        "status": "pending"
    }
    
    try:
        result = appointments_col.insert_one(appointment)
        messagebox.showinfo("Thành công", f"Thêm cuộc hẹn thành công. ID: {result.inserted_id}")
        appointment_date_entry.delete(0, tk.END)
        appointment_reason_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm cuộc hẹn:\n{e}")

# Cập nhật dropdown cho bệnh nhân và bác sĩ ở tab cuộc hẹn
def refresh_appointment_dropdowns():
    global patient_dict, doctor_dict
    patient_options = update_patient_list()
    doctor_options = update_doctor_list()
    
    patient_dict = {display: _id for (display, _id) in patient_options}
    doctor_dict = {display: _id for (display, _id) in doctor_options}
    
    patient_combo['values'] = list(patient_dict.keys())
    doctor_combo['values'] = list(doctor_dict.keys())

# Hàm tạo báo cáo đầy đủ (không hiển thị ID)
def generate_full_report():
    pipeline = [
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient_info"
            }
        },
        {
            "$lookup": {
                "from": "doctors",
                "localField": "doctor_id",
                "foreignField": "_id",
                "as": "doctor_info"
            }
        }
    ]
    results = list(appointments_col.aggregate(pipeline))
    
    report_lines = []
    header = "{:<20} {:<12} {:<8} {:<20} {:<20} {:<15} {:<20}".format(
        "Patient Name", "Birthday", "Gender", "Address", "Doctor Name", "Reason", "Date")
    report_lines.append(header)
    for doc in results:
        patient = doc.get("patient_info")
        doctor = doc.get("doctor_info")
        if patient and doctor:
            p = patient[0]
            d = doctor[0]
            birthday = p.get("date_of_birth").strftime("%Y-%m-%d") if isinstance(p.get("date_of_birth"), datetime) else p.get("date_of_birth")
            app_date = doc.get("appointment_date").strftime("%Y-%m-%d %H:%M:%S") if isinstance(doc.get("appointment_date"), datetime) else doc.get("appointment_date")
            line = "{:<20} {:<12} {:<8} {:<20} {:<20} {:<15} {:<20}".format(
                p.get("full_name"), birthday, p.get("gender"), p.get("address"), 
                d.get("full_name"), doc.get("reason"), app_date)
            report_lines.append(line)
    
    report_text.delete(1.0, tk.END)
    report_text.insert(tk.END, "\n".join(report_lines))

# Hàm tạo báo cáo các cuộc hẹn hôm nay (không hiển thị ID)
def generate_today_report():
    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    
    pipeline = [
        {"$match": {"appointment_date": {"$gte": start, "$lte": end}}},
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient_info"
            }
        },
        {
            "$lookup": {
                "from": "doctors",
                "localField": "doctor_id",
                "foreignField": "_id",
                "as": "doctor_info"
            }
        }
    ]
    results = list(appointments_col.aggregate(pipeline))
    
    report_lines = []
    header = "{:<20} {:<20} {:<12} {:<8} {:<20} {:<10} {:<15}".format(
        "Address", "Patient Name", "Birthday", "Gender", "Doctor Name", "Status", "Note")
    report_lines.append(header)
    for doc in results:
        patient = doc.get("patient_info")
        doctor = doc.get("doctor_info")
        if patient and doctor:
            p = patient[0]
            d = doctor[0]
            birthday = p.get("date_of_birth").strftime("%Y-%m-%d") if isinstance(p.get("date_of_birth"), datetime) else p.get("date_of_birth")
            address = p.get("address")
            status = doc.get("status")
            note = doc.get("reason")
            line = "{:<20} {:<20} {:<12} {:<8} {:<20} {:<10} {:<15}".format(
                address, p.get("full_name"), birthday, p.get("gender"), d.get("full_name"), status, note)
            report_lines.append(line)
    
    report_text.delete(1.0, tk.END)
    report_text.insert(tk.END, "\n".join(report_lines))

# Khởi tạo giao diện chính với ttkbootstrap (giao diện hiện đại hơn)
root = ttk.Window(themename="lumen")
root.title("Hệ thống Dịch vụ Y tế - Quản lý Cuộc hẹn")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

# Tab Bệnh nhân
patient_frame = ttk.Frame(notebook, padding=10)
notebook.add(patient_frame, text="Bệnh nhân")

ttk.Label(patient_frame, text="Họ và Tên:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
patient_name_entry = ttk.Entry(patient_frame, width=30)
patient_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(patient_frame, text="Ngày sinh (YYYY-MM-DD):").grid(row=1, column=0, sticky=W, padx=5, pady=5)
patient_dob_entry = ttk.Entry(patient_frame, width=30)
patient_dob_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(patient_frame, text="Giới tính:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
patient_gender_entry = ttk.Entry(patient_frame, width=30)
patient_gender_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(patient_frame, text="Địa chỉ:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
patient_address_entry = ttk.Entry(patient_frame, width=30)
patient_address_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(patient_frame, text="Số điện thoại:").grid(row=4, column=0, sticky=W, padx=5, pady=5)
patient_phone_entry = ttk.Entry(patient_frame, width=30)
patient_phone_entry.grid(row=4, column=1, padx=5, pady=5)

ttk.Label(patient_frame, text="Email:").grid(row=5, column=0, sticky=W, padx=5, pady=5)
patient_email_entry = ttk.Entry(patient_frame, width=30)
patient_email_entry.grid(row=5, column=1, padx=5, pady=5)

ttk.Button(patient_frame, text="Thêm Bệnh nhân", command=add_patient, bootstyle=SUCCESS).grid(row=6, column=0, columnspan=2, pady=10)

# Tab Bác sĩ
doctor_frame = ttk.Frame(notebook, padding=10)
notebook.add(doctor_frame, text="Bác sĩ")

ttk.Label(doctor_frame, text="Họ và Tên:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
doctor_name_entry = ttk.Entry(doctor_frame, width=30)
doctor_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(doctor_frame, text="Chuyên khoa:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
doctor_spec_entry = ttk.Entry(doctor_frame, width=30)
doctor_spec_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(doctor_frame, text="Số điện thoại:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
doctor_phone_entry = ttk.Entry(doctor_frame, width=30)
doctor_phone_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(doctor_frame, text="Email:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
doctor_email_entry = ttk.Entry(doctor_frame, width=30)
doctor_email_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(doctor_frame, text="Năm kinh nghiệm:").grid(row=4, column=0, sticky=W, padx=5, pady=5)
doctor_exp_entry = ttk.Entry(doctor_frame, width=30)
doctor_exp_entry.grid(row=4, column=1, padx=5, pady=5)

ttk.Button(doctor_frame, text="Thêm Bác sĩ", command=add_doctor, bootstyle=SUCCESS).grid(row=5, column=0, columnspan=2, pady=10)

# Tab Cuộc hẹn
appointment_frame = ttk.Frame(notebook, padding=10)
notebook.add(appointment_frame, text="Cuộc hẹn")

ttk.Label(appointment_frame, text="Chọn Bệnh nhân:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
patient_combo = ttk.Combobox(appointment_frame, state="readonly", width=40)
patient_combo.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(appointment_frame, text="Chọn Bác sĩ:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
doctor_combo = ttk.Combobox(appointment_frame, state="readonly", width=40)
doctor_combo.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(appointment_frame, text="Ngày giờ hẹn (YYYY-MM-DD HH:MM:SS):").grid(row=2, column=0, sticky=W, padx=5, pady=5)
appointment_date_entry = ttk.Entry(appointment_frame, width=40)
appointment_date_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(appointment_frame, text="Lý do:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
appointment_reason_entry = ttk.Entry(appointment_frame, width=40)
appointment_reason_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Button(appointment_frame, text="Thêm Cuộc hẹn", command=add_appointment, bootstyle=SUCCESS).grid(row=4, column=0, columnspan=2, pady=10)

# Tab Báo cáo
report_frame = ttk.Frame(notebook, padding=10)
notebook.add(report_frame, text="Báo cáo")

report_button_frame = ttk.Frame(report_frame)
report_button_frame.pack(side=TOP, fill=tk.X, padx=5, pady=5)

ttk.Button(report_button_frame, text="Báo cáo đầy đủ", command=generate_full_report, bootstyle=INFO).pack(side=LEFT, padx=5)
ttk.Button(report_button_frame, text="Cuộc hẹn hôm nay", command=generate_today_report, bootstyle=INFO).pack(side=LEFT, padx=5)

report_text = scrolledtext.ScrolledText(report_frame, width=150, height=25, font=("Consolas", 10))
report_text.pack(padx=5, pady=5)

# Khởi tạo các dropdown ban đầu
patient_dict = {}
doctor_dict = {}
refresh_appointment_dropdowns()

root.mainloop()
