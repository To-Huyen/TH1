import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

def show_entries():
    for widget in frame_entries.winfo_children():
        widget.destroy()

    shape = shape_var.get()
    global entry1, entry2, entry3
    entry1 = tk.Entry(frame_entries)
    entry2 = tk.Entry(frame_entries)
    entry3 = tk.Entry(frame_entries)

    if shape == "Hình cầu":
        tk.Label(frame_entries, text="Bán kính:").pack()
        entry1.pack()
    elif shape == "Hình lập phương":
        tk.Label(frame_entries, text="Cạnh:").pack()
        entry1.pack()
    elif shape == "Hình hộp chữ nhật":
        tk.Label(frame_entries, text="Chiều dài:").pack()
        entry1.pack()
        tk.Label(frame_entries, text="Chiều rộng:").pack()
        entry2.pack()
        tk.Label(frame_entries, text="Chiều cao:").pack()
        entry3.pack()
    elif shape == "Hình chóp đều":
        tk.Label(frame_entries, text="Cạnh đáy:").pack()
        entry1.pack()
        tk.Label(frame_entries, text="Chiều cao:").pack()
        entry2.pack()

def show_flat_shape_entries():
    for widget in frame_flat_entries.winfo_children():
        widget.destroy()

    shape = flat_shape_var.get()
    global flat_entry1, flat_entry2, flat_entry3,flat_entry4,flat_entry5
    flat_entry1 = tk.Entry(frame_flat_entries)
    flat_entry2 = tk.Entry(frame_flat_entries)
    flat_entry3 = tk.Entry(frame_flat_entries)
    flat_entry4 = tk.Entry(frame_flat_entries)
    flat_entry5 = tk.Entry(frame_flat_entries)

    if shape == "Hình tròn":
        tk.Label(frame_flat_entries, text="Bán kính:").pack()
        flat_entry1.pack()
    elif shape == "Hình tam giác":
        tk.Label(frame_flat_entries, text="Cạnh a:").pack()
        flat_entry1.pack()
        tk.Label(frame_flat_entries, text="Cạnh b:").pack()
        flat_entry2.pack()
        tk.Label(frame_flat_entries, text="Cạnh c:").pack()
        flat_entry3.pack()
    elif shape == "Hình vuông":
        tk.Label(frame_flat_entries, text="Cạnh:").pack()
        flat_entry1.pack()
    elif shape == "Hình chữ nhật":
        tk.Label(frame_flat_entries, text="Chiều dài:").pack()
        flat_entry1.pack()
        tk.Label(frame_flat_entries, text="Chiều rộng:").pack()
        flat_entry2.pack()
    elif shape == "Hình thang":
        tk.Label(frame_flat_entries, text="Đáy lớn:").pack()
        flat_entry1.pack()
        tk.Label(frame_flat_entries, text="Đáy nhỏ:").pack()
        flat_entry2.pack()
        tk.Label(frame_flat_entries, text="Chiều cao:").pack()
        flat_entry3.pack()
        tk.Label(frame_flat_entries, text="Cạnh bên 1:").pack()
        flat_entry4.pack()
        tk.Label(frame_flat_entries, text="Cạnh bên 2:").pack()
        flat_entry5.pack()
    elif shape == "Hình bình hành":
        tk.Label(frame_flat_entries, text="Cạnh đáy:").pack()
        flat_entry1.pack()
        tk.Label(frame_flat_entries, text="Cạnh bên:").pack()
        flat_entry2.pack()
        tk.Label(frame_flat_entries, text="Chiều cao:").pack()
        flat_entry3.pack()

def validate_and_draw():
    shape = shape_var.get()
    try:
        values = [abs(float(entry1.get()))] if shape == "Hình cầu" or shape == "Hình lập phương" else \
                 [abs(float(entry1.get())), abs(float(entry2.get()))] if shape == "Hình chóp đều" else \
                 [abs(float(entry1.get())), abs(float(entry2.get())), abs(float(entry3.get()))]

        calculate_and_draw(shape, values)
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")

def calculate_flat_shape():
    shape = flat_shape_var.get()
    try:
        if shape == "Hình tròn":
            radius = (float(flat_entry1.get()))
            if radius > 0:
                area = np.pi * radius ** 2
                perimeter = 2 * np.pi * radius
                messagebox.showinfo("Hình tròn", f"Diện tích: {area:.2f}, Chu vi: {perimeter:.2f}")
            else:
                raise ValueError("Bán kính phải lớn hơn 0.")
            
        elif shape == "Hình tam giác":
            a, b, c = (float(flat_entry1.get())), (float(flat_entry2.get())), (float(flat_entry3.get()))
            if any(side <= 0 for side in [a, b, c]):
                raise ValueError("Các cạnh phải lớn hơn 0.")
            if a + b > c and a + c > b and b + c > a:
                perimeter = a + b + c
                s = perimeter / 2
                area = np.sqrt(s * (s - a) * (s - b) * (s - c))
                messagebox.showinfo("Hình tam giác", f"Diện tích: {area:.2f}, Chu vi: {perimeter:.2f}")
            else:
                raise ValueError("Ba cạnh không hợp lệ để tạo thành tam giác.")
            
        elif shape == "Hình vuông":
            side = (float(flat_entry1.get()))    
            if side <= 0:
                raise ValueError("Cạnh phải lớn hơn 0.")
            area = side ** 2
            perimeter = 4 * side
            messagebox.showinfo("Hình vuông", f"Diện tích: {area:.2f}, Chu vi: {perimeter:.2f}")

        elif shape == "Hình chữ nhật":
            length, width = (float(flat_entry1.get())), (float(flat_entry2.get()))
            if length <= 0 or width <= 0:
                raise ValueError("Chiều dài và chiều rộng phải lớn hơn 0.")
            if length <= width:
                raise ValueError("Chiều dài phải lớn hơn chiều rộng.")
            area = length * width
            perimeter = 2 * (length + width)
            messagebox.showinfo("Hình chữ nhật", f"Diện tích: {area:.2f}, Chu vi: {perimeter:.2f}")

        elif shape == "Hình thang":
                base1 = (float(flat_entry1.get()))  # Đáy lớn
                base2 = (float(flat_entry2.get()))  # Đáy nhỏ
                height = (float(flat_entry3.get()))  # Chiều cao
                side1 = (float(flat_entry4.get()))  # Cạnh bên 1
                side2 = (float(flat_entry5.get()))  # Cạnh bên 2

                if base1 <= 0 or base2 <= 0 or side1 <= 0 or side2 <= 0:
                    messagebox.showerror("Lỗi", "Các cạnh phải lớn hơn 0.")
                    return
                if base1 <= base2:
                    messagebox.showerror("Lỗi", "Đáy lớn phải lớn hơn đáy nhỏ.")
                    return
                perimeter = base1 + base2 + side1 + side2  # Chu vi
                area = (base1 + base2) * height / 2       # Diện tích
                messagebox.showinfo(
                    "Hình thang",
                    f"Diện tích: {area:.2f}, Chu vi: {perimeter:.2f}")
                
        elif shape == "Hình bình hành":
                base = (float(flat_entry1.get()))  # Cạnh đáy
                side = (float(flat_entry2.get()))  # Cạnh bên
                height = (float(flat_entry3.get()))  # Chiều cao
                if base <= 0 or side <= 0:
                    messagebox.showerror("Lỗi", "Cạnh đáy và cạnh bên phải lớn hơn 0.")
                    return
                if height <= 0:
                    messagebox.showerror("Lỗi", "Chiều cao phải lớn hơn 0.")
                    return
                perimeter = 2 * (base + side)  # Chu vi
                area = base * height           # Diện tích
                messagebox.showinfo(
                    "Hình bình hành",
                    f"Diện tích: {area:.2f}, Chu vi: {perimeter:.2f}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")

def calculate_and_draw(shape, values):
    if shape == "Hình cầu":
        radius = values[0]
        area = 4 * np.pi * radius ** 2
        volume = (4/3) * np.pi * radius ** 3
        messagebox.showinfo("Hình cầu", f"Diện tích: {area:.2f}, Thể tích: {volume:.2f}")
        draw_sphere(radius)
    elif shape == "Hình lập phương":
        side = values[0]
        area = 6 * side ** 2
        volume = side ** 3
        messagebox.showinfo("Hình lập phương", f"Diện tích: {area:.2f}, Thể tích: {volume:.2f}")
        draw_cube(side)
    elif shape == "Hình hộp chữ nhật":
        length, width, height = values
        area = 2 * (length * width + width * height + height * length)
        volume = length * width * height
        messagebox.showinfo("Hình hộp chữ nhật", f"Diện tích: {area:.2f}, Thể tích: {volume:.2f}")
        draw_rectangular_prism(length, width, height)
    elif shape == "Hình chóp đều":
        base_side, height = values
        area = base_side ** 2 + 2 * base_side * np.sqrt((base_side / 2) ** 2 + height ** 2)
        volume = (1/3) * base_side ** 2 * height
        messagebox.showinfo("Hình chóp đều", f"Diện tích: {area:.2f}, Thể tích: {volume:.2f}")
        draw_pyramid(base_side, height)

def draw_sphere(radius):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(np.pi, 0, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x, y, z, color="b", alpha=0.6)
    ax.set_title("Hình cầu")
    plt.show()

def draw_rectangular_prism(length, width, height):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Các đỉnh của hình hộp chữ nhật
    x = [0, length, length, 0, 0, length, length, 0]
    y = [0, 0, width, width, 0, 0, width, width]
    z = [0, 0, 0, 0, height, height, height, height]

    # Các mặt
    vertices = [
        [0, 1, 5, 4],  # Mặt trước
        [1, 2, 6, 5],  # Mặt phải
        [2, 3, 7, 6],  # Mặt sau
        [3, 0, 4, 7],  # Mặt trái
        [0, 1, 2, 3],  # Mặt đáy
        [4, 5, 6, 7]   # Mặt trên
    ]

    for v in vertices:
        face = [[x[i], y[i], z[i]] for i in v]
        ax.add_collection3d(Poly3DCollection([face], alpha=0.6, edgecolor='k', facecolor="blue"))

    ax.set_xlim([0, length + 1])
    ax.set_ylim([0, width + 1])
    ax.set_zlim([0, height + 1])
    ax.set_title("Hình hộp chữ nhật")
    plt.show()

def draw_pyramid(base_side, height):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Tính tọa độ các đỉnh của hình chóp đều
    half_side = base_side / 2
    vertices = [
        [0, 0, 0],  # Đỉnh A
        [base_side, 0, 0],  # Đỉnh B
        [base_side, base_side, 0],  # Đỉnh C
        [0, base_side, 0],  # Đỉnh D
        [half_side, half_side, height]  # Đỉnh S (đỉnh chóp)
    ]

    # Các mặt của hình chóp
    faces = [
        [vertices[0], vertices[1], vertices[4]],  # Mặt SAB
        [vertices[1], vertices[2], vertices[4]],  # Mặt SBC
        [vertices[2], vertices[3], vertices[4]],  # Mặt SCD
        [vertices[3], vertices[0], vertices[4]],  # Mặt SDA
        [vertices[0], vertices[1], vertices[2], vertices[3]]  # Đáy ABCD
    ]

    for face in faces:
        ax.add_collection3d(Poly3DCollection([face], alpha=0.6, edgecolor='k', facecolor="orange"))

    ax.set_xlim([-1, base_side + 1])
    ax.set_ylim([-1, base_side + 1])
    ax.set_zlim([-1, height + 1])
    ax.set_title("Hình chóp đều")
    plt.show()

def draw_cube(side):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r = np.array([0, side])
    X, Y = np.meshgrid(r, r)
    ax.plot_surface(X, Y, np.zeros_like(X), color="cyan", alpha=0.6)
    ax.plot_surface(X, Y, np.full_like(X, side), color="cyan", alpha=0.6)
    ax.plot_surface(X, np.zeros_like(X), Y, color="cyan", alpha=0.6)
    ax.plot_surface(X, np.full_like(X, side), Y, color="cyan", alpha=0.6)
    ax.plot_surface(np.zeros_like(X), X, Y, color="cyan", alpha=0.6)
    ax.plot_surface(np.full_like(X, side), X, Y, color="cyan", alpha=0.6)
    ax.set_title("Hình lập phương")
    plt.show()

root = tk.Tk()
root.title("Phần mềm tính toán hình học")

frame_left = tk.Frame(root)
frame_left.pack(side="left", padx=10, pady=10)
frame_right = tk.Frame(root)
frame_right.pack(side="right", padx=10, pady=10)

tk.Label(frame_left, text="Chọn hình không gian:").pack()
shape_var = tk.StringVar(value="Hình cầu")
tk.OptionMenu(frame_left, shape_var, "Hình cầu", "Hình lập phương", "Hình hộp chữ nhật", "Hình chóp đều", command=lambda _: show_entries()).pack()
frame_entries = tk.Frame(frame_left)
frame_entries.pack()
tk.Button(frame_left, text="Tính toán và vẽ", command=validate_and_draw).pack(pady=5)

tk.Label(frame_right, text="Chọn hình phẳng:").pack()
flat_shape_var = tk.StringVar(value="Hình tròn")
tk.OptionMenu(frame_right, flat_shape_var, "Hình tròn", "Hình tam giác", "Hình vuông", "Hình chữ nhật", "Hình thang", "Hình bình hành", command=lambda _: show_flat_shape_entries()).pack()
frame_flat_entries = tk.Frame(frame_right)
frame_flat_entries.pack()
tk.Button(frame_right, text="Tính toán", command=calculate_flat_shape).pack(pady=5)

show_entries()
show_flat_shape_entries()
root.mainloop()
