import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Đọc dữ liệu từ file water_potability.csv
df = pd.read_csv(r'D:\Ki 7\Ma nguon mo\TH1\bai7\water_potability.csv')

# Chuẩn hóa tên cột để tránh lỗi
df.columns = df.columns.str.strip().str.lower()

# Tiền xử lý dữ liệu: Thay thế các giá trị NaN bằng giá trị trung bình
df.fillna(df.mean(), inplace=True)

# Kiểm tra tỷ lệ "nước uống được" và "không uống được"
print("Tỷ lệ mẫu trong dữ liệu:")
print(df['potability'].value_counts(normalize=True))

# Chia dữ liệu thành X (đặc trưng) và y (mục tiêu)
X = df.drop('potability', axis=1)
y = df['potability']

# Chuẩn bị dữ liệu: Chia tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình học máy
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Tạo cửa sổ ứng dụng Tkinter
root = tk.Tk()
root.title("Ứng Dụng Xác Định Chất Lượng Nước")
root.geometry("500x700")

# Nhãn hướng dẫn
label = tk.Label(root, text="Nhập các thông số để dự đoán chất lượng nước:", font=("Arial", 14))
label.pack(pady=20)

# Các trường nhập liệu và giá trị khoảng
fields = [
    ("pH", (0, 14)), 
    ("Hardness", (0, 500)), 
    ("Solids", (0, 50000)), 
    ("Chloramines", (0, 10)), 
    ("Sulfate", (0, 500)), 
    ("Conductivity", (0, 1000)), 
    ("Organic Carbon", (0, 50)), 
    ("Trihalomethanes", (0, 120)), 
    ("Turbidity", (0, 10))
]

entries = {}

# Tạo các trường nhập liệu với giá trị tham khảo
for field, (min_val, max_val) in fields:
    frame = tk.Frame(root)
    frame.pack(pady=5)
    label = tk.Label(frame, text=f"{field} (Giá trị từ {min_val} đến {max_val}):")
    label.pack(side=tk.LEFT, padx=5)
    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT, padx=5)
    entries[field] = entry

# Hàm để xử lý dự đoán
def predict_quality():
    try:
        input_data = {}
        for field, (min_val, max_val) in fields:
            value = entries[field].get()
            try:
                value = float(value)
            except ValueError:
                raise ValueError(f"Giá trị của {field} phải là số.")
            if value < min_val or value > max_val:
                raise ValueError(f"Giá trị của {field} phải trong khoảng từ {min_val} đến {max_val}.")
            input_data[field.lower()] = value

        # Tạo DataFrame từ dữ liệu đầu vào
        input_df = pd.DataFrame([input_data])
        input_scaled = scaler.transform(input_df)

        # Dự đoán chất lượng nước
        prediction = model.predict(input_scaled)

        # In dữ liệu đầu vào và kết quả dự đoán để kiểm tra
        print("Dữ liệu đầu vào:", input_data)
        print("Kết quả dự đoán:", prediction)

        result = "Nước có thể uống được." if prediction[0] == 1 else "Nước không an toàn để uống."
        messagebox.showinfo("Kết quả dự đoán", result)
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

# Nút dự đoán
predict_button = tk.Button(root, text="Dự Đoán", command=predict_quality, font=("Arial", 12))
predict_button.pack(pady=20)

# Chạy ứng dụng
root.mainloop()
