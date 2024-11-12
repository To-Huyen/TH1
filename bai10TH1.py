import cv2
import numpy as np

# Hàm xử lý ảnh với các tham số điều chỉnh từ thanh trượt
def enhance_low_light_image(image, gamma, bilateral_filter_intensity):
    # Chuyển đổi ảnh sang không gian màu YUV để dễ điều chỉnh độ sáng
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    # Tăng độ sáng bằng cách cân bằng histogram của kênh Y (độ sáng)
    yuv_image[:, :, 0] = cv2.equalizeHist(yuv_image[:, :, 0])

    # Chuyển đổi lại sang không gian màu BGR
    enhanced_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)

    # Áp dụng bộ lọc gamma correction để tăng cường ánh sáng
    look_up_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255
                              for i in np.arange(0, 256)]).astype("uint8")
    enhanced_image = cv2.LUT(enhanced_image, look_up_table)

    # Sử dụng bộ lọc bilateral để giảm nhiễu mà vẫn giữ được độ nét
    denoised_image = cv2.bilateralFilter(enhanced_image, d=9, sigmaColor=bilateral_filter_intensity, sigmaSpace=bilateral_filter_intensity)

    return denoised_image

# Hàm cập nhật khi thay đổi thanh trượt
def update(val=0):
    gamma = cv2.getTrackbarPos("Gamma", "Enhance Image") / 10
    if gamma < 0.1:  # Tránh gamma quá thấp gây tối ảnh
        gamma = 0.1

    bilateral_intensity = cv2.getTrackbarPos("Denoise", "Enhance Image")

    enhanced_image = enhance_low_light_image(original_image, gamma, bilateral_intensity)

    # Ghép ảnh gốc và ảnh đã tăng cường cạnh nhau
    combined_image = np.hstack((original_image, enhanced_image))
    cv2.imshow("Enhance Image", combined_image)

# Đọc ảnh đầu vào
image_path = r"D:\Ki 7\Ma nguon mo\TH1\bai10\images.jpg"
original_image = cv2.imread(image_path)
if original_image is None:
    print("Không thể đọc ảnh.")
else:
    # Tạo cửa sổ hiển thị
    cv2.namedWindow("Enhance Image")

    # Tạo thanh trượt
    cv2.createTrackbar("Gamma", "Enhance Image", 15, 50, update)  # Giá trị mặc định là 1.5
    cv2.createTrackbar("Denoise", "Enhance Image", 75, 150, update)  # Giá trị mặc định cho bilateral filter

    # Hiển thị ảnh lần đầu
    update()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
