import numpy as np
import tkinter as tk
from tkinter import messagebox

def is_valid_input(input_str):
    """Kiểm tra xem input có phải là số thực hay không"""
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def giai_he():
    try:
        # Lấy dữ liệu từ giao diện và kiểm tra xem có hợp lệ không
        inputs = [entry_a11.get(), entry_a12.get(), entry_a21.get(), entry_a22.get(), entry_b1.get(), entry_b2.get()]
        if not all(is_valid_input(i) for i in inputs):
            raise ValueError("Vui lòng chỉ nhập số!")
        
        # Chuyển dữ liệu sang float và tạo ma trận A và B
        A = np.array([[float(entry_a11.get()), float(entry_a12.get())], [float(entry_a21.get()), float(entry_a22.get())]])
        B = np.array([float(entry_b1.get()), float(entry_b2.get())])
        
        # Kiểm tra định thức ma trận (nếu định thức = 0 thì vô nghiệm hoặc vô số nghiệm)
        det_A = np.linalg.det(A)
        if det_A == 0:
            raise ValueError("Hệ phương trình có vô số nghiệm hoặc vô nghiệm (định thức = 0).")
        
        # Giải hệ phương trình Ax = B
        nghiem = np.linalg.solve(A, B)
        
        # Hiển thị kết quả
        messagebox.showinfo("Kết quả", f"Nghiệm của hệ: x1 = {nghiem[0]:.4f}, x2 = {nghiem[1]:.4f}")
    
    except np.linalg.LinAlgError:
        messagebox.showerror("Lỗi", "Hệ phương trình vô nghiệm hoặc vô số nghiệm.")
    except ValueError as ve:
        messagebox.showerror("Lỗi", str(ve))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

# Tạo cửa sổ GUI
window = tk.Tk()
window.title("Giải Hệ Phương Trình Tuyến Tính")

# Tạo các label và entry cho ma trận A
tk.Label(window, text="a11").grid(row=0, column=0)
entry_a11 = tk.Entry(window)
entry_a11.grid(row=0, column=1)

tk.Label(window, text="a12").grid(row=0, column=2)
entry_a12 = tk.Entry(window)
entry_a12.grid(row=0, column=3)

tk.Label(window, text="a21").grid(row=1, column=0)
entry_a21 = tk.Entry(window)
entry_a21.grid(row=1, column=1)

tk.Label(window, text="a22").grid(row=1, column=2)
entry_a22 = tk.Entry(window)
entry_a22.grid(row=1, column=3)

# Tạo các label và entry cho vector B
tk.Label(window, text="b1").grid(row=2, column=0)
entry_b1 = tk.Entry(window)
entry_b1.grid(row=2, column=1)

tk.Label(window, text="b2").grid(row=2, column=2)
entry_b2 = tk.Entry(window)
entry_b2.grid(row=2, column=3)

# Nút để giải hệ phương trình
solve_button = tk.Button(window, text="Giải", command=giai_he)
solve_button.grid(row=3, column=1, columnspan=2)

# Chạy ứng dụng GUI
window.mainloop()
