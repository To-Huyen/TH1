import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import tkinter as tk
from tkinter import messagebox, ttk

# Đọc dữ liệu từ file CSV
data = pd.read_csv(r'D:\Ki 7\Ma nguon mo\TH1\bai6\Student_Performance.csv')

# Chuyển đổi giá trị phân loại thành giá trị số
label_encoder = LabelEncoder()
data['Extracurricular Activities'] = label_encoder.fit_transform(data['Extracurricular Activities'])

# Tách biến đặc trưng (X) và biến mục tiêu (y)
X = data[['Hours Studied', 'Previous Scores', 'Extracurricular Activities', 'Sleep Hours', 'Sample Question Papers Practiced']]
y = data['Performance Index']

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Khởi tạo các mô hình
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(),
    "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
    "K-Nearest Neighbors": KNeighborsRegressor(n_neighbors=5),
    "Support Vector Regression": SVR()
}

# Tạo giao diện người dùng với tkinter
root = tk.Tk()
root.title("Dự đoán Hiệu quả Học tập Sinh viên")

# Các nhãn và ô nhập dữ liệu
tk.Label(root, text="Số giờ học").grid(row=0, column=0)
tk.Label(root, text="Điểm số trước đó").grid(row=1, column=0)
tk.Label(root, text="Hoạt động ngoại khóa (0 = Không, 1 = Có)").grid(row=2, column=0)
tk.Label(root, text="Số giờ ngủ").grid(row=3, column=0)
tk.Label(root, text="Số bài kiểm tra đã làm").grid(row=4, column=0)

entry_hours_studied = tk.Entry(root)
entry_previous_scores = tk.Entry(root)
entry_extracurricular_activities = tk.Entry(root)
entry_sleep_hours = tk.Entry(root)
entry_sample_question_papers = tk.Entry(root)

entry_hours_studied.grid(row=0, column=1)
entry_previous_scores.grid(row=1, column=1)
entry_extracurricular_activities.grid(row=2, column=1)
entry_sleep_hours.grid(row=3, column=1)
entry_sample_question_papers.grid(row=4, column=1)

# Dropdown chọn mô hình
model_choice = tk.StringVar(root)
model_choice.set("Linear Regression")
tk.Label(root, text="Chọn mô hình:").grid(row=5, column=0)
model_menu = ttk.Combobox(root, textvariable=model_choice, values=list(models.keys()))
model_menu.grid(row=5, column=1)

# Hàm dự đoán
def predict_performance():
    try:
        # Lấy dữ liệu từ các ô nhập
        inputs = [
            float(entry_hours_studied.get()),
            float(entry_previous_scores.get()),
            int(entry_extracurricular_activities.get()),
            float(entry_sleep_hours.get()),
            int(entry_sample_question_papers.get())
        ]
        # Kiểm tra nếu có số âm
        if any(value < 0 for value in inputs):
            messagebox.showerror("Lỗi", "Vui lòng không nhập số âm!")
            return
        # Chuẩn hóa dữ liệu đầu vào
        new_data = scaler.transform([inputs])

        # Chọn mô hình và dự đoán
        selected_model = models[model_choice.get()]
        selected_model.fit(X_train, y_train)
        prediction = selected_model.predict(new_data)

        # Hiển thị kết quả
        percentage_prediction = max(0, prediction[0])  # Đảm bảo không âm
        messagebox.showinfo("Kết quả dự đoán", f"Hiệu quả học tập dự đoán: {percentage_prediction:.2f}%")

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng dữ liệu!")

# Nút dự đoán
predict_button = tk.Button(root, text="Dự đoán", command=predict_performance)
predict_button.grid(row=6, column=0, columnspan=2)

# Chạy giao diện
root.mainloop()
