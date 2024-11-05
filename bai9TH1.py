import cv2
import numpy as np
from tkinter import Tk, Button, filedialog, Label, Scale, HORIZONTAL, Frame
from PIL import Image, ImageTk

def edge_detection(image, low_threshold, high_threshold):
    # Sử dụng bộ lọc Canny với các ngưỡng điều chỉnh từ thanh trượt
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges

def open_image():
    # Chọn ảnh từ file
    filepath = filedialog.askopenfilename()
    if filepath:
        global original_image
        original_image = cv2.imread(filepath)
        display_original_image(original_image)
        process_image()  # Gọi để cập nhật ảnh tách biên ngay sau khi chọn ảnh

def capture_image():
    # Chụp ảnh từ webcam
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, image = cap.read()
        cap.release()
        if ret:
            global original_image
            # Thay đổi kích thước ảnh chụp từ webcam để vừa với giao diện
            original_image = cv2.resize(image, (400, 300))  # Điều chỉnh kích thước phù hợp
            display_original_image(original_image)
            process_image()

def process_image():
    # Cập nhật ảnh tách biên theo giá trị thanh trượt
    if original_image is not None:
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        low_threshold = threshold1_scale.get()
        high_threshold = threshold2_scale.get()
        edges = edge_detection(gray_image, low_threshold, high_threshold)
        display_edge_image(edges)  # Cập nhật ảnh sau khi tách biên
        global processed_image
        processed_image = edges  # Lưu ảnh đã xử lý để sử dụng sau

def display_original_image(image):
    # Hiển thị ảnh gốc
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(rgb_image)
    img_tk = ImageTk.PhotoImage(img_pil)
    global original_label
    original_label.configure(image=img_tk)
    original_label.image = img_tk

def display_edge_image(image):
    # Hiển thị ảnh sau khi tách biên
    edge_rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    img_pil = Image.fromarray(edge_rgb_image)
    img_tk = ImageTk.PhotoImage(img_pil)
    global edge_label
    edge_label.configure(image=img_tk)
    edge_label.image = img_tk

def save_image():
    # Lưu ảnh sau khi tách biên
    if processed_image is not None:
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if filepath:
            cv2.imwrite(filepath, processed_image)
            print(f"Ảnh đã lưu tại: {filepath}")

# Tạo cửa sổ Tkinter
root = Tk()
root.title("Chương trình tách biên ảnh với thanh trượt điều chỉnh")

# Tạo khung bên trái và bên phải
left_frame = Frame(root)
left_frame.pack(side="left", padx=10, pady=10)

right_frame = Frame(root)
right_frame.pack(side="right", padx=10, pady=10)

# Nút chọn ảnh và chụp ảnh
btn_open = Button(left_frame, text="Chọn ảnh từ file", command=open_image)
btn_open.pack()

btn_capture = Button(left_frame, text="Chụp ảnh từ webcam", command=capture_image)
btn_capture.pack()

# Thanh trượt điều chỉnh ngưỡng tách biên
threshold1_scale = Scale(left_frame, from_=0, to=255, orient=HORIZONTAL, label="Ngưỡng dưới", command=lambda x: process_image())
threshold1_scale.set(100)
threshold1_scale.pack()

threshold2_scale = Scale(left_frame, from_=0, to=255, orient=HORIZONTAL, label="Ngưỡng trên", command=lambda x: process_image())
threshold2_scale.set(200)
threshold2_scale.pack()

# Nút lưu ảnh sau khi tách biên
btn_save = Button(left_frame, text="Lưu ảnh sau khi tách biên", command=save_image)
btn_save.pack()

# Nhãn hiển thị ảnh gốc và ảnh sau khi tách biên
original_label = Label(right_frame, text="Ảnh gốc", compound="top")
original_label.grid(row=0, column=0, padx=10, pady=10)

edge_label = Label(right_frame, text="Ảnh sau khi tách biên", compound="top")
edge_label.grid(row=0, column=1, padx=10, pady=10)

# Khởi tạo biến để lưu ảnh gốc và ảnh đã xử lý
original_image = None
processed_image = None

root.mainloop()
