import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import firwin, lfilter, butter, filtfilt
import tkinter as tk
from tkinter import ttk

# Hàm tạo tín hiệu
def generate_signal(frequency, amplitude, phase, duration, sampling_rate=1000, signal_type='sine'):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    
    if signal_type == 'sine':
        signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    elif signal_type == 'square':
        signal = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    elif signal_type == 'sawtooth':
        signal = amplitude * (2 * (t * frequency % 1) - 1)
    else:
        raise ValueError("Loại tín hiệu không hỗ trợ")
    
    return t, signal

# Hàm tính Fourier Transform
def plot_fft(signal, sampling_rate):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / sampling_rate)

    plt.plot(xf, np.abs(yf))
    plt.title("Biến đổi Fourier")
    plt.xlabel("Tần số (Hz)")
    plt.ylabel("Biên độ")
    plt.show()

# Bộ lọc FIR
def apply_fir_filter(signal, cutoff, fs, filter_type='low'):
    nyq_rate = fs / 2.0
    taps = firwin(numtaps=101, cutoff=cutoff / nyq_rate, pass_zero=(filter_type == 'low'))
    filtered_signal = lfilter(taps, 1.0, signal)
    return filtered_signal

# Bộ lọc IIR
def apply_iir_filter(signal, cutoff, fs, order=5, filter_type='low'):
    nyq_rate = fs / 2.0
    b, a = butter(order, cutoff / nyq_rate, btype=filter_type)
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal

# GUI
def create_gui():
    root = tk.Tk()
    root.title("Công cụ hỗ trợ học Xử lý Tín hiệu Số")

    # Nhập tham số
    tk.Label(root, text="Tần số (Hz)").pack()
    freq_entry = tk.Entry(root)
    freq_entry.pack()
    
    tk.Label(root, text="Biên độ").pack()
    amp_entry = tk.Entry(root)
    amp_entry.pack()
    
    tk.Label(root, text="Pha (Radians)").pack()
    phase_entry = tk.Entry(root)
    phase_entry.pack()

    tk.Label(root, text="Thời gian (s)").pack()
    duration_entry = tk.Entry(root)
    duration_entry.pack()

    # Loại tín hiệu
    tk.Label(root, text="Chọn loại tín hiệu").pack()
    signal_type = tk.StringVar(value='sine')
    signal_menu = ttk.Combobox(root, textvariable=signal_type, values=["sine", "square", "sawtooth"])
    signal_menu.pack()

    # Nút tạo tín hiệu
    def plot_signal():
        freq = float(freq_entry.get())
        amp = float(amp_entry.get())
        phase = float(phase_entry.get())
        duration = float(duration_entry.get())
        
        t, signal = generate_signal(frequency=freq, amplitude=amp, phase=phase, duration=duration, signal_type=signal_type.get())
        plt.plot(t, signal)
        plt.title(f"Tín hiệu {signal_type.get()}: {freq} Hz, Biên độ {amp}")
        plt.xlabel("Thời gian (s)")
        plt.ylabel("Biên độ")
        plt.show()
        
    tk.Button(root, text="Tạo tín hiệu", command=plot_signal).pack()

    # Nút biến đổi Fourier
    def plot_fourier():
        freq = float(freq_entry.get())
        amp = float(amp_entry.get())
        phase = float(phase_entry.get())
        duration = float(duration_entry.get())
        
        _, signal = generate_signal(frequency=freq, amplitude=amp, phase=phase, duration=duration, signal_type=signal_type.get())
        plot_fft(signal, sampling_rate=1000)

    tk.Button(root, text="Biến đổi Fourier", command=plot_fourier).pack()

    # Chọn loại bộ lọc
    tk.Label(root, text="Chọn loại bộ lọc").pack()
    filter_type = tk.StringVar(value='FIR')
    filter_menu = ttk.Combobox(root, textvariable=filter_type, values=["FIR", "IIR"])
    filter_menu.pack()

    # Áp dụng bộ lọc
    def apply_filter():
        freq = float(freq_entry.get())
        amp = float(amp_entry.get())
        phase = float(phase_entry.get())
        duration = float(duration_entry.get())
        
        t, signal = generate_signal(frequency=freq, amplitude=amp, phase=phase, duration=duration, signal_type=signal_type.get())
        
        if filter_type.get() == "FIR":
            filtered_signal = apply_fir_filter(signal, cutoff=5, fs=1000)
            plt.plot(t, filtered_signal, label='Bộ lọc FIR')
        elif filter_type.get() == "IIR":
            filtered_signal = apply_iir_filter(signal, cutoff=5, fs=1000)
            plt.plot(t, filtered_signal, label='Bộ lọc IIR')
        
        plt.title("Tín hiệu sau khi lọc")
        plt.xlabel("Thời gian (s)")
        plt.ylabel("Biên độ")
        plt.legend()
        plt.show()

    tk.Button(root, text="Áp dụng bộ lọc", command=apply_filter).pack()

    root.mainloop()

# Khởi chạy GUI
create_gui()
