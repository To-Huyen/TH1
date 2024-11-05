import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, integrate, limit, oo, lambdify

# Hàm tính đạo hàm cho hàm một ẩn
def derivative_one_var(a, b, c):
    x = symbols('x')
    function = a * x**2 + b * x + c
    derivative_expr = diff(function, x)
    return str(derivative_expr)

# Hàm tính đạo hàm cho hàm hai ẩn
def derivative_two_var(a, b, c, d, e, f):
    x, y = symbols('x y')
    function = a * x**2 + b * y**2 + c * x * y + d * x + e * y + f
    derivative_x = diff(function, x)
    derivative_y = diff(function, y)
    return str(derivative_x), str(derivative_y)

# Hàm tính giới hạn
def calculate_limit(a, b, c, limit_value):
    x = symbols('x')
    function = a * x**2 + b * x + c
    limit_value = limit_value if limit_value != 'oo' else oo  # xử lý giới hạn vô cực
    limit_result = limit(function, x, limit_value)
    return str(limit_result)

# Hàm tính tích phân
def calculate_integral(a, b, c):
    x = symbols('x')
    function = a * x**2 + b * x + c
    integral_expr = integrate(function, x)
    return str(integral_expr)

# Hàm tính vi phân
def calculate_differential(a, b, c, x0, dx):
    x = symbols('x')
    function = a * x**2 + b * x + c
    derivative_value = derivative_one_var(a, b, c)  # Tính đạo hàm
    derivative_at_x0 = lambdify(x, derivative_value)(x0)  # Giá trị đạo hàm tại x0
    df = derivative_at_x0 * dx  # Vi phân
    return df

# Hàm vẽ đồ thị
def plot_function(a, b, c, function_type):
    x = symbols('x')
    if function_type == "1 ẩn":
        function = a * x**2 + b * x + c
        f = lambdify(x, function, 'numpy')
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)
        
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, label=f'f(x) = {a}x² + {b}x + {c}')
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')
        plt.title('Đồ thị hàm một ẩn')
        plt.xlabel('x')
        plt.ylabel('f(x)')
    
    elif function_type == "2 ẩn":
        y = symbols('y')
        function = a * x**2 + b * y**2 + c * x * y
        f = lambdify((x, y), function, 'numpy')
        x_vals = np.linspace(-10, 10, 400)
        y_vals = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = f(X, Y)

        plt.figure(figsize=(8, 6))
        plt.contourf(X, Y, Z, levels=50, cmap='viridis')
        plt.colorbar()
        plt.title('Đồ thị hàm hai ẩn')
        plt.xlabel('x')
        plt.ylabel('y')

    plt.grid()
    plt.show()

# Tạo giao diện người dùng
def create_main_window():
    window = tk.Tk()
    window.title("Học Giải Tích")

    tk.Label(window, text="Chọn loại hàm số:").pack()
    
    function_type = tk.StringVar(value="1 ẩn")
    function_options = ["1 ẩn", "2 ẩn"]
    tk.OptionMenu(window, function_type, *function_options).pack()

    tk.Label(window, text="Nhập hệ số a:").pack()
    a_entry = tk.Entry(window)
    a_entry.pack()

    tk.Label(window, text="Nhập hệ số b:").pack()
    b_entry = tk.Entry(window)
    b_entry.pack()

    tk.Label(window, text="Nhập hệ số c:").pack()
    c_entry = tk.Entry(window)
    c_entry.pack()

    tk.Label(window, text="Nhập hệ số d (nếu hàm 2 ẩn):").pack()
    d_entry = tk.Entry(window)
    d_entry.pack()

    tk.Label(window, text="Nhập hệ số e (nếu hàm 2 ẩn):").pack()
    e_entry = tk.Entry(window)
    e_entry.pack()

    tk.Label(window, text="Nhập hệ số f (nếu hàm 2 ẩn):").pack()
    f_entry = tk.Entry(window)
    f_entry.pack()

    tk.Label(window, text="Nhập giá trị giới hạn (vd: 0 hoặc 'oo' cho vô cực):").pack()
    limit_entry = tk.Entry(window)
    limit_entry.pack()

    tk.Label(window, text="Nhập x0 cho vi phân:").pack()
    x0_entry = tk.Entry(window)
    x0_entry.pack()

    tk.Label(window, text="Nhập dx cho vi phân:").pack()
    dx_entry = tk.Entry(window)
    dx_entry.pack()

    def show_derivative():
        selected_type = function_type.get()
        if selected_type == "1 ẩn":
            a = float(a_entry.get())
            b = float(b_entry.get())
            c = float(c_entry.get())
            result = derivative_one_var(a, b, c)
            messagebox.showinfo("Kết quả đạo hàm", f"Đạo hàm của {a}x² + {b}x + {c} là: {result}")
        elif selected_type == "2 ẩn":
            a = float(a_entry.get())
            b = float(b_entry.get())
            c = float(c_entry.get())
            d = float(d_entry.get())
            e = float(e_entry.get())
            f = float(f_entry.get())
            result_x, result_y = derivative_two_var(a, b, c, d, e, f)
            messagebox.showinfo("Kết quả đạo hàm", f"Đạo hàm theo x: {result_x}\nĐạo hàm theo y: {result_y}")

    def show_limit():
        a = float(a_entry.get())
        b = float(b_entry.get())
        c = float(c_entry.get())
        limit_value = limit_entry.get()
        result = calculate_limit(a, b, c, limit_value)
        messagebox.showinfo("Kết quả giới hạn", f"Giới hạn của {a}x² + {b}x + {c} khi x tiến đến {limit_value} là: {result}")

    def show_integral():
        a = float(a_entry.get())
        b = float(b_entry.get())
        c = float(c_entry.get())
        result = calculate_integral(a, b, c)
        messagebox.showinfo("Kết quả tích phân", f"Tích phân của {a}x² + {b}x + {c} là: {result}")

    def show_differential():
        a = float(a_entry.get())
        b = float(b_entry.get())
        c = float(c_entry.get())
        x0 = float(x0_entry.get())
        dx = float(dx_entry.get())
        result = calculate_differential(a, b, c, x0, dx)
        messagebox.showinfo("Kết quả vi phân", f"Vi phân tại x0={x0} với dx={dx} là: {result}")

    def plot_graph():
        a = float(a_entry.get())
        b = float(b_entry.get())
        c = float(c_entry.get())
        selected_type = function_type.get()
        if selected_type == "2 ẩn":
            d = float(d_entry.get())
            e = float(e_entry.get())
            f = float(f_entry.get())
            plot_function(a, b, c, selected_type)
        else:
            plot_function(a, b, c, selected_type)

    tk.Button(window, text="Tính đạo hàm", command=show_derivative).pack()
    tk.Button(window, text="Tính giới hạn", command=show_limit).pack()
    tk.Button(window, text="Tính tích phân", command=show_integral).pack()
    tk.Button(window, text="Tính vi phân", command=show_differential).pack()
    tk.Button(window, text="Vẽ đồ thị", command=plot_graph).pack()
    
    return window

# Hàm chính
def main():
    root = create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main()
