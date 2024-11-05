import cv2
import numpy as np
import tkinter as tk
from tkinter import Button, Label, Scale, filedialog
from PIL import Image, ImageTk

# Khởi tạo ảnh gốc và ảnh đã lọc
img = None
filtered_img = None

# Hàm cập nhật ảnh theo bộ lọc và hiển thị ảnh sau khi lọc
def apply_filter(blur_value, sharp_value, bw_value, background_value):
    global img, filtered_img
    if img is None:
        return

    # Tạo bản sao của ảnh gốc
    filtered_img = img.copy()

    # 1. Bộ lọc mờ
    if blur_value > 0:
        kernel_size = (blur_value, blur_value)  # Kích thước kernel tùy theo thanh trượt
        filtered_img = cv2.GaussianBlur(filtered_img, kernel_size, 0)

    # 2. Bộ lọc làm nét
    if sharp_value > 0:
        kernel_sharp = np.array([[0, -sharp_value, 0], [-sharp_value, sharp_value * 4 + 1, -sharp_value], [0, -sharp_value, 0]])
        filtered_img = cv2.filter2D(filtered_img, -1, kernel_sharp)

    # 3. Chuyển đổi sang đen trắng
    if bw_value > 0:
        gray = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
        filtered_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # 4. Bộ lọc xóa phông (làm mờ nền)
    if background_value > 0:
        mask = np.zeros(filtered_img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (50, 50, filtered_img.shape[1] - 50, filtered_img.shape[0] - 50)
        cv2.grabCut(filtered_img, mask, rect, bgdModel, fgdModel, background_value, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        filtered_img = filtered_img * mask2[:, :, np.newaxis]

    show_images()

# Hàm hiển thị ảnh gốc và ảnh sau khi lọc
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

# Hàm tải ảnh từ file
def load_image():
    global img, filtered_img
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        filtered_img = img.copy()
        show_images()

# Hàm lưu ảnh sau khi lọc
def save_image():
    if filtered_img is not None:
        cv2.imwrite('filtered_image.png', filtered_img)
        print("Ảnh sau khi lọc đã được lưu.")
    else:
        print("Chưa có ảnh sau khi lọc để lưu.")

# Hàm chụp ảnh từ webcam
def capture_image():
    global img, filtered_img
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không mở được webcam.")
        return
    
    ret, frame = cap.read()
    cap.release()
    if ret:
        # Thay đổi kích thước ảnh cho vừa khung hiển thị
        frame = cv2.resize(frame, (300, 200))  # Điều chỉnh kích thước theo nhu cầu
        img = frame
        filtered_img = img.copy()
        show_images()
    else:
        print("Không chụp được ảnh.")


# Tạo giao diện
root = tk.Tk()
root.title("Bộ lọc ảnh với các hiệu ứng")

# Khung hiển thị ảnh gốc và ảnh sau lọc
label_original = Label(root, text="Ảnh Gốc")
label_original.grid(row=0, column=0, padx=10, pady=10)
label_filtered = Label(root, text="Ảnh Sau Lọc")
label_filtered.grid(row=0, column=2, padx=10, pady=10)

# Tạo thanh trượt cho các hiệu ứng
label_blur = Label(root, text="Mờ ảnh")
label_blur.grid(row=1, column=3)
scale_blur = Scale(root, from_=0, to=20, orient="horizontal", command=lambda val: apply_filter(int(val), scale_sharp.get(), scale_bw.get(), scale_background.get()))
scale_blur.grid(row=2, column=3)

label_sharp = Label(root, text="Làm nét ảnh")
label_sharp.grid(row=3, column=3)
scale_sharp = Scale(root, from_=0, to=5, orient="horizontal", command=lambda val: apply_filter(scale_blur.get(), int(val), scale_bw.get(), scale_background.get()))
scale_sharp.grid(row=4, column=3)

label_bw = Label(root, text="Đen trắng")
label_bw.grid(row=5, column=3)
scale_bw = Scale(root, from_=0, to=1, orient="horizontal", command=lambda val: apply_filter(scale_blur.get(), scale_sharp.get(), int(val), scale_background.get()))
scale_bw.grid(row=6, column=3)

label_background = Label(root, text="Xóa phông")
label_background.grid(row=7, column=3)
scale_background = Scale(root, from_=0, to=5, orient="horizontal", command=lambda val: apply_filter(scale_blur.get(), scale_sharp.get(), scale_bw.get(), int(val)))
scale_background.grid(row=8, column=3)

# Nút tải ảnh từ file
btn_load = Button(root, text="Tải ảnh từ file", command=load_image)
btn_load.grid(row=9, column=1, pady=10)

# Nút lưu ảnh sau khi lọc
btn_save = Button(root, text="Lưu ảnh sau khi lọc", command=save_image)
btn_save.grid(row=10, column=1, pady=10)

# Nút chụp ảnh từ webcam
btn_capture = Button(root, text="Chụp ảnh từ webcam", command=capture_image)
btn_capture.grid(row=9, column=2, pady=10)

# Hiển thị ảnh ban đầu nếu có
show_images()

root.mainloop()
