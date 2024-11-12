import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import messagebox

# Đọc dữ liệu từ file CSV
file_path = r'D:\Ki 7\Ma nguon mo\TH1\bai11\Student_Performance.csv'
df = pd.read_csv(file_path)

# Từ điển dịch từ tiếng Anh sang tiếng Việt cho các tên thống kê
translation = {
    "Hours Studied": "Số giờ học",
    "Previous Scores": "Điểm số trước đó",
    "Extracurricular Activities": "Hoạt động ngoại khóa",
    "Sleep Hours": "Giờ ngủ",
    "Sample Question Papers Practiced": "Số đề đã làm",
    "Performance Index": "Chỉ số hiệu suất",
    "Max": "Giá trị lớn nhất",
    "Min": "Giá trị nhỏ nhất",
    "Mean": "Giá trị trung bình"
}

# Hàm phân tích và hiển thị dữ liệu
def analyze_data():
    selection = analysis_var.get()
    if selection == "Tính toán Max, Min, Mean":
        # Tính toán Max, Min, Mean
        max_values = df[['Hours Studied', 'Previous Scores', 'Extracurricular Activities', 
                         'Sleep Hours', 'Sample Question Papers Practiced', 'Performance Index']].max()
        min_values = df[['Hours Studied', 'Previous Scores', 'Extracurricular Activities', 
                         'Sleep Hours', 'Sample Question Papers Practiced', 'Performance Index']].min()
        mean_values = df[['Hours Studied', 'Previous Scores', 'Extracurricular Activities', 
                          'Sleep Hours', 'Sample Question Papers Practiced', 'Performance Index']].mean()
        
        # Tạo chuỗi kết quả với hai ngôn ngữ
        result = "Kết quả phân tích:\n\n"
        result += "Tiếng Anh (English)    |   Tiếng Việt\n"
        result += "-"*40 + "\n"
        
        for stat, values in zip(["Max", "Min", "Mean"], [max_values, min_values, mean_values]):
            result += f"{stat} ({translation[stat]}):\n"
            for col, value in values.items():
                result += f"{col:30} {translation[col]:<30}: {value}\n"
            result += "\n"
        
        # Hiển thị kết quả trong messagebox
        messagebox.showinfo("Kết quả phân tích", result)
        
    elif selection == "Phân phối Số giờ học":
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Hours Studied'], bins=15, kde=True)
        plt.title('Phân phối Số giờ học')
        plt.xlabel('Hours Studied')
        plt.ylabel('Tần suất')
        plt.show()
        
    elif selection == "Phân phối Điểm số trước đó":
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Previous Scores'], bins=15, kde=True)
        plt.title('Phân phối Điểm số trước đó')
        plt.xlabel('Previous Scores')
        plt.ylabel('Tần suất')
        plt.show()
        
    elif selection == "Mối quan hệ giữa Số giờ ngủ và Chỉ số hiệu suất":
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Sleep Hours', y='Performance Index', data=df)
        plt.title('Mối quan hệ giữa Số giờ ngủ và Chỉ số hiệu suất')
        plt.xlabel('Sleep Hours')
        plt.ylabel('Performance Index')
        plt.show()
        
    elif selection == "Mối quan hệ giữa Số giờ học và Chỉ số hiệu suất":
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Hours Studied', y='Performance Index', data=df)
        plt.title('Mối quan hệ giữa Số giờ học và Chỉ số hiệu suất')
        plt.xlabel('Hours Studied')
        plt.ylabel('Performance Index')
        plt.show()
        
    elif selection == "Phân phối Chỉ số hiệu suất":
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Performance Index'], bins=15, kde=True)
        plt.title('Phân phối Chỉ số hiệu suất')
        plt.xlabel('Performance Index')
        plt.ylabel('Tần suất')
        plt.show()

# Thiết lập GUI
root = tk.Tk()
root.title("Phân tích dữ liệu")

# Tạo label và menu lựa chọn
label = tk.Label(root, text="Chọn nội dung cần phân tích:")
label.pack(pady=10)

analysis_var = tk.StringVar(value="Tính toán Max, Min, Mean")
options = [
    "Tính toán Max, Min, Mean",
    "Phân phối Số giờ học",
    "Phân phối Điểm số trước đó",
    "Mối quan hệ giữa Số giờ ngủ và Chỉ số hiệu suất",
    "Mối quan hệ giữa Số giờ học và Chỉ số hiệu suất",
    "Phân phối Chỉ số hiệu suất"
]

# Menu chọn nội dung
option_menu = tk.OptionMenu(root, analysis_var, *options)
option_menu.pack(pady=10)

# Nút bấm để phân tích dữ liệu
analyze_button = tk.Button(root, text="Phân tích", command=analyze_data)
analyze_button.pack(pady=20)

root.mainloop()
