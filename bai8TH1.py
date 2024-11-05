import cv2
import numpy as np
import tkinter as tk
from tkinter import Button, Label, filedialog
from PIL import Image, ImageTk

# Khởi tạo ảnh gốc và ảnh đã lọc
img = None
filtered_img = None

# Các bộ lọc
kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
kernel_3x3 = np.ones((3, 3), np.float32) / 9.0
kernel_5x5 = np.ones((5, 5), np.float32) / 25.0
kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

# Hàm cập nhật hiển thị ảnh sau khi áp dụng bộ lọc
def apply_filter(filter_type):
    global filtered_img
    if img is None:
        print("Chưa có ảnh để lọc.")
        return
    
    if filter_type == "3x3":
        filtered_img = cv2.filter2D(img, -1, kernel_3x3)
    elif filter_type == "5x5":
        filtered_img = cv2.filter2D(img, -1, kernel_5x5)
    elif filter_type == "sharpen":
        filtered_img = cv2.filter2D(img, -1, kernel_sharpen)
    elif filter_type == "grayscale":
        filtered_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR)
    elif filter_type == "remove_background":
        filtered_img = remove_background(img)
    else:
        filtered_img = cv2.filter2D(img, -1, kernel_identity)
    
    show_images()

# Hàm hiển thị ảnh gốc và ảnh sau lọc
def show_images():
    if img is None or filtered_img is None:
        return

    img_original = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_filtered = Image.fromarray(cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB))

    img_original_tk = ImageTk.PhotoImage(img_original)
    img_filtered_tk = ImageTk.PhotoImage(img_filtered)

    label_original.config(image=img_original_tk)
    label_original.image = img_original_tk

    label_filtered.config(image=img_filtered_tk)
    label_filtered.image = img_filtered_tk

# Hàm lưu ảnh sau khi lọc
def save_image():
    if filtered_img is not None:
        cv2.imwrite('filtered_image.png', filtered_img)
        print("Ảnh sau khi lọc đã được lưu.")
    else:
        print("Chưa có ảnh sau khi lọc để lưu.")

# Hàm tải ảnh từ file
def load_image():
    global img, filtered_img
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        filtered_img = img.copy()
        show_images()

# Hàm chụp ảnh từ webcam
def capture_image():
    global img, filtered_img
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        img = frame
        filtered_img = img.copy()
        show_images()
    cap.release()

# Hàm xóa phông
def remove_background(image):
    # Tạo mặt nạ ban đầu
    mask = np.zeros(image.shape[:2], np.uint8)
    
    # Khởi tạo mô hình nền và tiền cảnh
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Định vùng cho đối tượng (ở giữa ảnh)
    rect = (50, 50, image.shape[1] - 50, image.shape[0] - 50)
    
    # Áp dụng thuật toán GrabCut
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # Đánh dấu các pixel là nền hoặc tiền cảnh
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    result = image * mask2[:, :, np.newaxis]

    # Làm mờ phần nền
    background = cv2.GaussianBlur(image, (21, 21), 0)
    final_img = background * (1 - mask2[:, :, np.newaxis]) + result
    
    return final_img.astype(np.uint8)

# Tạo giao diện
root = tk.Tk()
root.title("Lọc Ảnh")

# Khung hiển thị ảnh gốc và ảnh sau lọc
label_original = Label(root)
label_original.grid(row=0, column=0, padx=10, pady=10)
label_filtered = Label(root)
label_filtered.grid(row=0, column=2, padx=10, pady=10)

# Các nút lựa chọn bộ lọc
btn_identity = Button(root, text="Bộ lọc gốc", command=lambda: apply_filter("identity"))
btn_identity.grid(row=1, column=1)

btn_3x3 = Button(root, text="Làm mờ 3x3", command=lambda: apply_filter("3x3"))
btn_3x3.grid(row=2, column=1)

btn_5x5 = Button(root, text="Làm mịn 5x5", command=lambda: apply_filter("5x5"))
btn_5x5.grid(row=3, column=1)

btn_sharpen = Button(root, text="Làm nét", command=lambda: apply_filter("sharpen"))
btn_sharpen.grid(row=4, column=1)

btn_grayscale = Button(root, text="Ảnh đen trắng", command=lambda: apply_filter("grayscale"))
btn_grayscale.grid(row=5, column=1)

btn_remove_background = Button(root, text="Xóa phông", command=lambda: apply_filter("remove_background"))
btn_remove_background.grid(row=6, column=1)

# Nút tải ảnh từ file và chụp ảnh từ webcam
btn_load = Button(root, text="Tải ảnh từ file", command=load_image)
btn_load.grid(row=7, column=1, pady=10)

btn_capture = Button(root, text="Chụp ảnh từ webcam", command=capture_image)
btn_capture.grid(row=8, column=1, pady=10)

# Nút lưu ảnh sau khi lọc
btn_save = Button(root, text="Lưu ảnh sau khi lọc", command=save_image)
btn_save.grid(row=9, column=1, pady=10)

# Hiển thị ảnh ban đầu nếu có
show_images()

root.mainloop()
