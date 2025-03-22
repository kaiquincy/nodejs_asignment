import os
import tkinter
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from sklearn.linear_model import LinearRegression

# Cấu hình style cho ttk.Treeview (để bảng dữ liệu hiển thị giao diện dark)
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                fieldbackground="#343638",
                bordercolor="#343638",
                borderwidth=0,
                rowheight=25)
style.map("Treeview", background=[("selected", "#22559b")])
style.configure("Treeview.Heading",
                background="#565b5e",
                foreground="white",
                relief="flat")
style.map("Treeview.Heading", background=[("active", "#3484F0")])

# Đặt giao diện tối cho matplotlib
plt.style.use('dark_background')

CSV_FILE = 'sales_data.csv'

class SalesManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Doanh Thu Bán Hàng")
        self.geometry("1000x700")

        # Load dữ liệu từ file CSV
        self.df = self.load_data()
        if self.df is None:
            self.destroy()
            return

        # Tạo khung sidebar bên trái (chiều rộng cố định 200px)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        # Tạo khung nội dung chính bên phải
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Tạo các nút menu trong sidebar
        self.create_sidebar_buttons()

        # Mặc định hiển thị màn hình tổng quan (summary)
        self.show_summary()

    def load_data(self):
        if not os.path.exists(CSV_FILE):
            messagebox.showerror("Lỗi", f"File {CSV_FILE} không tồn tại. Vui lòng chạy generate_sample_data.py trước.")
            return None
        df = pd.read_csv(CSV_FILE)
        if 'revenue' not in df.columns:
            df['revenue'] = df['quantity'] * df['unit_price']
        df['date'] = pd.to_datetime(df['date'])
        return df

    def save_data(self):
        self.df.to_csv(CSV_FILE, index=False)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_sidebar_buttons(self):
        # Tiêu đề ứng dụng
        title_label = ctk.CTkLabel(self.sidebar_frame, text="Quản Lý\nDoanh Thu", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(20, 10), padx=10)

        # Các nút chức năng
        btn_summary = ctk.CTkButton(self.sidebar_frame, text="Tóm tắt", command=self.show_summary)
        btn_summary.pack(pady=5, padx=10, fill="x")

        btn_view = ctk.CTkButton(self.sidebar_frame, text="Xem Dữ Liệu", command=self.view_data)
        btn_view.pack(pady=5, padx=10, fill="x")

        btn_add = ctk.CTkButton(self.sidebar_frame, text="Thêm Dữ Liệu", command=self.add_data_view)
        btn_add.pack(pady=5, padx=10, fill="x")

        btn_edit_delete = ctk.CTkButton(self.sidebar_frame, text="Chỉnh Sửa/Xóa", command=self.edit_delete_view)
        btn_edit_delete.pack(pady=5, padx=10, fill="x")

        # Separator
        separator = ctk.CTkLabel(self.sidebar_frame, text="----------------")
        separator.pack(pady=10)

        # Nhãn Biểu Đồ
        chart_label = ctk.CTkLabel(self.sidebar_frame, text="Biểu Đồ")
        chart_label.pack(pady=5)

        btn_chart_revenue_date = ctk.CTkButton(self.sidebar_frame, text="Doanh Thu Ngày", command=self.chart_revenue_by_date)
        btn_chart_revenue_date.pack(pady=5, padx=10, fill="x")

        btn_chart_quantity_product = ctk.CTkButton(self.sidebar_frame, text="Sản Phẩm Bán Được", command=self.chart_quantity_by_product)
        btn_chart_quantity_product.pack(pady=5, padx=10, fill="x")

        btn_chart_revenue_distribution = ctk.CTkButton(self.sidebar_frame, text="Doanh Thu Phân Bổ", command=self.chart_revenue_distribution)
        btn_chart_revenue_distribution.pack(pady=5, padx=10, fill="x")

        # Thêm nút Dự Đoán Doanh Thu
        btn_predict = ctk.CTkButton(self.sidebar_frame, text="Dự Đoán Doanh Thu", command=self.predict_revenue_view)
        btn_predict.pack(pady=5, padx=10, fill="x")

        # Separator
        separator2 = ctk.CTkLabel(self.sidebar_frame, text="----------------")
        separator2.pack(pady=10)

        btn_export = ctk.CTkButton(self.sidebar_frame, text="Xuất Báo Cáo", command=self.export_report)
        btn_export.pack(pady=5, padx=10, fill="x")

        btn_exit = ctk.CTkButton(self.sidebar_frame, text="Thoát", command=self.quit)
        btn_exit.pack(pady=5, padx=10, fill="x")

    def show_summary(self):
        self.clear_content_frame()
        total_revenue = self.df['revenue'].sum()
        total_quantity = self.df['quantity'].sum()
        summary_text = f"Tổng doanh thu: {total_revenue}\nTổng số lượng bán được: {total_quantity}"
        summary_label = ctk.CTkLabel(self.content_frame, text=summary_text, font=ctk.CTkFont(size=16))
        summary_label.pack(pady=20, padx=20, anchor="w")

    def view_data(self):
        self.clear_content_frame()

        # Khung lọc dữ liệu
        filter_frame = ctk.CTkFrame(self.content_frame)
        filter_frame.pack(pady=10, padx=10, fill="x")

        lbl_from = ctk.CTkLabel(filter_frame, text="Từ ngày (YYYY-MM-DD):")
        lbl_from.pack(side="left", padx=5)
        entry_from = ctk.CTkEntry(filter_frame, width=120, placeholder_text="YYYY-MM-DD")
        entry_from.pack(side="left", padx=5)

        lbl_to = ctk.CTkLabel(filter_frame, text="Đến ngày (YYYY-MM-DD):")
        lbl_to.pack(side="left", padx=5)
        entry_to = ctk.CTkEntry(filter_frame, width=120, placeholder_text="YYYY-MM-DD")
        entry_to.pack(side="left", padx=5)

        lbl_product = ctk.CTkLabel(filter_frame, text="Sản phẩm:")
        lbl_product.pack(side="left", padx=5)
        entry_product = ctk.CTkEntry(filter_frame, width=150, placeholder_text="Tên sản phẩm")
        entry_product.pack(side="left", padx=5)

        def apply_filter():
            filtered_df = self.df.copy()
            from_date = entry_from.get().strip()
            to_date = entry_to.get().strip()
            product = entry_product.get().strip().lower()
            if from_date:
                try:
                    from_dt = datetime.strptime(from_date, "%Y-%m-%d")
                    filtered_df = filtered_df[filtered_df['date'] >= from_dt]
                except ValueError:
                    messagebox.showerror("Lỗi", "Định dạng Từ ngày không hợp lệ.")
                    return
            if to_date:
                try:
                    to_dt = datetime.strptime(to_date, "%Y-%m-%d")
                    filtered_df = filtered_df[filtered_df['date'] <= to_dt]
                except ValueError:
                    messagebox.showerror("Lỗi", "Định dạng Đến ngày không hợp lệ.")
                    return
            if product:
                filtered_df = filtered_df[filtered_df['product'].str.lower().str.contains(product)]
            populate_tree(filtered_df)

        btn_filter = ctk.CTkButton(filter_frame, text="Lọc", command=apply_filter)
        btn_filter.pack(side="left", padx=5)
        btn_reset = ctk.CTkButton(filter_frame, text="Reset", command=lambda: populate_tree(self.df))
        btn_reset.pack(side="left", padx=5)

        # Hiển thị dữ liệu trong Treeview
        tree_frame = ctk.CTkFrame(self.content_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("date", "product", "quantity", "unit_price", "revenue")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)

        def populate_tree(dataframe):
            for row in tree.get_children():
                tree.delete(row)
            for _, row in dataframe.iterrows():
                tree.insert("", "end", values=(
                    row['date'].strftime("%Y-%m-%d"), row['product'], row['quantity'], row['unit_price'], row['revenue']
                ))
        populate_tree(self.df)

    def add_data_view(self):
        self.clear_content_frame()
        title = ctk.CTkLabel(self.content_frame, text="Thêm Dữ Liệu Bán Hàng", font=ctk.CTkFont(size=16))
        title.pack(pady=10)
        form_frame = ctk.CTkFrame(self.content_frame)
        form_frame.pack(pady=10)

        lbl_date = ctk.CTkLabel(form_frame, text="Ngày (YYYY-MM-DD):")
        lbl_date.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_date = ctk.CTkEntry(form_frame)
        entry_date.grid(row=0, column=1, padx=5, pady=5)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        lbl_product = ctk.CTkLabel(form_frame, text="Sản phẩm:")
        lbl_product.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_product = ctk.CTkEntry(form_frame)
        entry_product.grid(row=1, column=1, padx=5, pady=5)

        lbl_quantity = ctk.CTkLabel(form_frame, text="Số lượng:")
        lbl_quantity.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_quantity = ctk.CTkEntry(form_frame)
        entry_quantity.grid(row=2, column=1, padx=5, pady=5)

        lbl_unit_price = ctk.CTkLabel(form_frame, text="Đơn giá:")
        lbl_unit_price.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        entry_unit_price = ctk.CTkEntry(form_frame)
        entry_unit_price.grid(row=3, column=1, padx=5, pady=5)

        def submit():
            date_str = entry_date.get().strip()
            product = entry_product.get().strip()
            quantity = entry_quantity.get().strip()
            unit_price = entry_unit_price.get().strip()
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Lỗi", "Ngày không hợp lệ. Định dạng: YYYY-MM-DD")
                return
            try:
                quantity = int(quantity)
                unit_price = float(unit_price)
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng và đơn giá phải là số.")
                return
            revenue = quantity * unit_price
            new_row = {
                "date": date_obj,
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "revenue": revenue
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            self.save_data()
            messagebox.showinfo("Thành công", "Dữ liệu đã được thêm.")
            self.show_summary()

        btn_submit = ctk.CTkButton(self.content_frame, text="Thêm", command=submit)
        btn_submit.pack(pady=10)

    def edit_delete_view(self):
        self.clear_content_frame()
        title = ctk.CTkLabel(self.content_frame, text="Chỉnh Sửa / Xóa Dữ Liệu", font=ctk.CTkFont(size=16))
        title.pack(pady=10)
        tree_frame = ctk.CTkFrame(self.content_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("index", "date", "product", "quantity", "unit_price", "revenue")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)

        def populate_tree():
            for row in tree.get_children():
                tree.delete(row)
            for idx, row in self.df.iterrows():
                tree.insert("", "end", values=(
                    idx, row['date'].strftime("%Y-%m-%d"), row['product'], row['quantity'], row['unit_price'], row['revenue']
                ))
        populate_tree()

        def edit_record():
            selected = tree.focus()
            if not selected:
                messagebox.showerror("Lỗi", "Vui lòng chọn bản ghi để chỉnh sửa.")
                return
            values = tree.item(selected, "values")
            idx = int(values[0])
            self.edit_record_window(idx)

        def delete_record():
            selected = tree.focus()
            if not selected:
                messagebox.showerror("Lỗi", "Vui lòng chọn bản ghi để xóa.")
                return
            values = tree.item(selected, "values")
            idx = int(values[0])
            if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bản ghi này?"):
                self.df = self.df.drop(idx).reset_index(drop=True)
                self.save_data()
                populate_tree()
                messagebox.showinfo("Thành công", "Bản ghi đã được xóa.")

        btn_frame = ctk.CTkFrame(self.content_frame)
        btn_frame.pack(pady=10)
        btn_edit = ctk.CTkButton(btn_frame, text="Chỉnh sửa", command=edit_record)
        btn_edit.pack(side="left", padx=10)
        btn_delete = ctk.CTkButton(btn_frame, text="Xóa", command=delete_record)
        btn_delete.pack(side="left", padx=10)

    def edit_record_window(self, idx):
        record = self.df.iloc[idx]
        edit_win = ctk.CTkToplevel(self)
        edit_win.title("Chỉnh sửa bản ghi")
        edit_win.geometry("300x250")

        lbl_date = ctk.CTkLabel(edit_win, text="Ngày (YYYY-MM-DD):")
        lbl_date.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_date = ctk.CTkEntry(edit_win)
        entry_date.grid(row=0, column=1, padx=5, pady=5)
        entry_date.insert(0, record['date'].strftime("%Y-%m-%d"))

        lbl_product = ctk.CTkLabel(edit_win, text="Sản phẩm:")
        lbl_product.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_product = ctk.CTkEntry(edit_win)
        entry_product.grid(row=1, column=1, padx=5, pady=5)
        entry_product.insert(0, record['product'])

        lbl_quantity = ctk.CTkLabel(edit_win, text="Số lượng:")
        lbl_quantity.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_quantity = ctk.CTkEntry(edit_win)
        entry_quantity.grid(row=2, column=1, padx=5, pady=5)
        entry_quantity.insert(0, record['quantity'])

        lbl_unit_price = ctk.CTkLabel(edit_win, text="Đơn giá:")
        lbl_unit_price.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        entry_unit_price = ctk.CTkEntry(edit_win)
        entry_unit_price.grid(row=3, column=1, padx=5, pady=5)
        entry_unit_price.insert(0, record['unit_price'])

        def update_record():
            date_str = entry_date.get().strip()
            product = entry_product.get().strip()
            quantity = entry_quantity.get().strip()
            unit_price = entry_unit_price.get().strip()
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Lỗi", "Ngày không hợp lệ. Định dạng: YYYY-MM-DD")
                return
            try:
                quantity = int(quantity)
                unit_price = float(unit_price)
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng và đơn giá phải là số.")
                return
            revenue = quantity * unit_price
            self.df.at[idx, 'date'] = date_obj
            self.df.at[idx, 'product'] = product
            self.df.at[idx, 'quantity'] = quantity
            self.df.at[idx, 'unit_price'] = unit_price
            self.df.at[idx, 'revenue'] = revenue
            self.save_data()
            messagebox.showinfo("Thành công", "Bản ghi đã được cập nhật.")
            edit_win.destroy()
            self.edit_delete_view()

        btn_update = ctk.CTkButton(edit_win, text="Cập nhật", command=update_record)
        btn_update.grid(row=4, column=0, columnspan=2, pady=10)

    def chart_revenue_by_date(self):
        self.clear_content_frame()
        df_grouped = self.df.groupby('date')['revenue'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(df_grouped['date'], df_grouped['revenue'], marker='o')
        ax.set_title("Doanh Thu Theo Ngày")
        ax.set_xlabel("Ngày")
        ax.set_ylabel("Doanh thu")
        ax.grid(True)
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def chart_quantity_by_product(self):
        self.clear_content_frame()
        df_grouped = self.df.groupby('product')['quantity'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(df_grouped['product'], df_grouped['quantity'])
        ax.set_title("Số Lượng Bán Theo Sản Phẩm")
        ax.set_xlabel("Sản phẩm")
        ax.set_ylabel("Số lượng")
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def chart_revenue_distribution(self):
        self.clear_content_frame()
        df_grouped = self.df.groupby('product')['revenue'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(df_grouped['revenue'], labels=df_grouped['product'], autopct='%1.1f%%', startangle=140)
        ax.set_title("Phân Bổ Doanh Thu Theo Sản Phẩm")
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def predict_revenue_view(self):
        self.clear_content_frame()

        # Chuẩn bị dữ liệu cho mô hình
        min_date = self.df['date'].min()
        max_date = self.df['date'].max()
        date_range = pd.date_range(start=min_date, end=max_date, freq='D')
        df_grouped = self.df.groupby('date')['revenue'].sum().reindex(date_range, fill_value=0).to_frame().reset_index()
        df_grouped.columns = ['date', 'revenue']
        df_grouped['days'] = (df_grouped['date'] - min_date).dt.days

        # Huấn luyện mô hình hồi quy tuyến tính
        X = df_grouped[['days']]
        y = df_grouped['revenue']
        model = LinearRegression()
        model.fit(X, y)

        # Tạo giao diện
        title = ctk.CTkLabel(self.content_frame, text="Dự Đoán Doanh Thu Tương Lai", font=ctk.CTkFont(size=16))
        title.pack(pady=10)

        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.pack(pady=10)

        lbl_date = ctk.CTkLabel(input_frame, text="Nhập ngày (YYYY-MM-DD):")
        lbl_date.grid(row=0, column=0, padx=5, pady=5)
        entry_date = ctk.CTkEntry(input_frame, width=150)
        entry_date.grid(row=0, column=1, padx=5, pady=5)

        result_label = ctk.CTkLabel(self.content_frame, text="", font=ctk.CTkFont(size=14))
        result_label.pack(pady=10)

        plot_frame = ctk.CTkFrame(self.content_frame)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def predict():
            date_str = entry_date.get().strip()
            try:
                future_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Lỗi", "Ngày không hợp lệ. Định dạng: YYYY-MM-DD")
                return

            future_days = (future_date - min_date).days
            prediction = model.predict([[future_days]])[0]
            result_label.configure(text=f"Dự đoán doanh thu cho {date_str}: {prediction:.2f}")

            # Xóa nội dung cũ trong plot_frame
            for widget in plot_frame.winfo_children():
                widget.destroy()

            # Vẽ biểu đồ
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.scatter(df_grouped['date'], df_grouped['revenue'], label='Dữ liệu lịch sử', color='cyan')
            all_dates = pd.date_range(start=min_date, end=future_date, freq='D')
            all_days = (all_dates - min_date).days
            X_all = pd.DataFrame({'days': all_days})
            y_pred = model.predict(X_all)
            ax.plot(all_dates, y_pred, color='red', label='Đường hồi quy')
            ax.scatter(future_date, prediction, color='green', label='Dự đoán', zorder=5)
            ax.set_title("Dự Đoán Doanh Thu")
            ax.set_xlabel("Ngày")
            ax.set_ylabel("Doanh thu")
            ax.legend()
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            # Nhúng biểu đồ vào giao diện
            canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        btn_predict = ctk.CTkButton(input_frame, text="Dự Đoán", command=predict)
        btn_predict.grid(row=0, column=2, padx=5, pady=5)

    def export_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                self.df.to_excel(file_path, index=False)
                messagebox.showinfo("Thành công", f"Báo cáo đã được xuất ra {file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất báo cáo: {e}")

if __name__ == "__main__":
    app = SalesManagerApp()
    app.mainloop()