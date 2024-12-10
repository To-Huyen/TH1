#img = cv2.imread('input_shapes.png', cv2.IMREAD_GRAYSCALE)Đọc ảnh input_shapes.png vào biến img với chế độ màu xám (grayscale)
#rows, cols = img.shape  Lấy kích thước (số hàng và số cột) của ảnh. img.shape trả về một tuple có dạng (rows, cols)
#sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = 5) Áp dụng bộ lọc Sobel để tính đạo hàm theo chiều ngang (sự thay đổi giá trị ảnh theo chiều ngang).
#sobel_vertical = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize = 5)Áp dụng bộ lọc Sobel để tính đạo hàm theo chiều dọc (sự thay đổi giá trị ảnh theo chiều dọc).
#cv2.imshow('Original', img) Hiển thị ảnh gốc trong một cửa sổ tên là "Original". Hàm cv2.imshow mở cửa sổ để hiển thị ảnh.
#cv2.imshow('Sobel horizontal', sobel horizontal) Hiển thị kết quả của bộ lọc Sobel theo chiều ngang trong một cửa sổ tên là "Sobel horizontal"
#cv2.imshow('Sobel vertical', sobel vertical) Hiển thị kết quả của bộ lọc Sobel theo chiều dọc trong một cửa sổ tên là "Sobel vertical"

#Chức năng chính của đoạn lệnh:
#Đọc ảnh dưới dạng ảnh xám (grayscale).
#Sử dụng bộ lọc Sobel để phát hiện biên theo hai hướng:
#Chiều ngang (horizontal edges).
#Chiều dọc (vertical edges).
#Hiển thị ảnh gốc và các ảnh sau khi áp dụng bộ lọc Sobel.

#Ý tưởng cải tiến đoạn lệnh :
#Thêm lọc Solbel tổng hợp
#chức năng tải ảnh từ file
#chức năng lưu ảnh ra màn hình
#chức năng lọc Áp dụng Gaussian
#chức năng lọc Áp dụng Canny

import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog
from tkinter import messagebox
import os
import matplotlib.pyplot as plt

# Hàm tăng độ sáng cho ảnh
def increase_brightness(img, value=50):
    hsv = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v[v > 255] = 255
    v[v < 0] = 0
    hsv = cv2.merge((h, s, v))
    bright_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    bright_img = cv2.cvtColor(bright_img, cv2.COLOR_BGR2GRAY)
    return bright_img

# Hàm tải ảnh từ file
def load_image():
    global img, img_path
    img_path = filedialog.askopenfilename(
        title="Chọn file ảnh",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if img_path:
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            label_status.config(text="Không thể đọc file ảnh!")
        else:
            label_status.config(text="Ảnh đã được tải thành công!")
            show_image(img, "Ảnh gốc")

# Hàm áp dụng bộ lọc Gaussian
def apply_gaussian():
    global processed_img
    if img is None:
        label_status.config(text="Hãy tải ảnh trước!")
        return
    processed_img = cv2.GaussianBlur(img, (5, 5), 0)
    show_image(processed_img, "Kết quả: Làm mờ Gaussian")

# Hàm áp dụng Sobel
def apply_sobel():
    global processed_img_x, processed_img_y, processed_img_combined
    if img is None:
        label_status.config(text="Hãy tải ảnh trước!")
        return

    # Tính toán Sobel theo từng chiều
    sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)  # Gradient theo chiều ngang
    sobel_vertical = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)    # Gradient theo chiều dọc
    
    # Chuyển sang định dạng uint8 để hiển thị
    processed_img_x = cv2.convertScaleAbs(sobel_horizontal)
    processed_img_y = cv2.convertScaleAbs(sobel_vertical)

    # Kết hợp hai gradient để hiển thị tổng hợp
    sobel_combined = cv2.magnitude(sobel_horizontal, sobel_vertical)
    processed_img_combined = np.uint8(sobel_combined)
    
    # Hiển thị các kết quả
    show_image(processed_img_x, "Kết quả: Sobel (Chiều ngang)")
    show_image(processed_img_y, "Kết quả: Sobel (Chiều dọc)")
    show_image(processed_img_combined, "Kết quả: Sobel (Tổng hợp)")

# Hàm áp dụng bộ lọc Canny
def apply_canny():
    global processed_img
    if img is None:
        label_status.config(text="Hãy tải ảnh trước!")
        return
    
    # Áp dụng bộ lọc Canny để phát hiện biên
    processed_img = cv2.Canny(img, 100, 200)
    show_image(processed_img, "Kết quả: Phát hiện biên (Canny)")

# Hàm tăng độ sáng
def brighten_image():
    global processed_img
    if img is None:
        label_status.config(text="Hãy tải ảnh trước!")
        return
    processed_img = increase_brightness(img, value=50)
    show_image(processed_img, "Kết quả: Tăng độ sáng")

# Hàm lưu ảnh
def save_image():
    if processed_img is None:  # Kiểm tra xem ảnh đã được xử lý hay chưa
        messagebox.showerror("Lỗi", "Chưa có ảnh nào để lưu!")
        return
    save_path = os.path.join(os.path.expanduser("~"), "Desktop", "processed_image.png")
    cv2.imwrite(save_path, processed_img)
    label_status.config(text=f"Ảnh đã được lưu tại: {save_path}")
    messagebox.showinfo("Thành công", f"Ảnh đã lưu thành công tại:\n{save_path}")

# Hàm hiển thị ảnh bằng matplotlib
def show_image(image, title):
    plt.figure()
    plt.imshow(image, cmap='gray')
    plt.title(title, fontsize=14)
    plt.axis('off')  # Tắt các trục
    plt.show()

# Tạo giao diện chính
root = Tk()
root.title("Công cụ xử lý ảnh")
root.geometry("400x300")

img = None  # Biến toàn cục lưu ảnh
img_path = ""  # Đường dẫn ảnh
processed_img = None  # Biến lưu ảnh sau khi xử lý

# Chọn ảnh mặc định và áp dụng Sobel khi chương trình chạy
default_img_path = r"C:\Users\minhv\Desktop\TX2MNM\input_shapes.png"  # Đường dẫn đến ảnh mặc định
img = cv2.imread(default_img_path, cv2.IMREAD_GRAYSCALE)
if img is not None:
    label_status = Label(root, text="Ảnh mặc định đã được tải thành công!", fg="blue")
    label_status.pack(pady=20)
    apply_sobel()
else:
    label_status = Label(root, text="Không thể tải ảnh mặc định!", fg="red")
    label_status.pack(pady=20)

# Giao diện
Button(root, text="Tải ảnh", command=load_image, width=20).pack(pady=10)
Button(root, text="Áp dụng Gaussian", command=apply_gaussian, width=20).pack(pady=10)
Button(root, text="Tăng độ sáng", command=brighten_image, width=20).pack(pady=10)
Button(root, text="Áp dụng Sobel", command=apply_sobel, width=20).pack(pady=10)
Button(root, text="Áp dụng Canny", command=apply_canny, width=20).pack(pady=10)  # Nút áp dụng Canny
Button(root, text="Lưu ảnh", command=save_image, width=20).pack(pady=10)

label_status = Label(root, text="Chưa có ảnh nào được tải.", fg="blue")
label_status.pack(pady=20)

# Khởi chạy giao diện
root.mainloop()





