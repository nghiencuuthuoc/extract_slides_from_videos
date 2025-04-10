import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import glob
import cv2

def extract_frames(video_path, input_root, output_root, interval_sec=10):
    # Tính đường dẫn tương đối để giữ nguyên cấu trúc thư mục
    relative_path = os.path.relpath(video_path, input_root)
    relative_folder = os.path.splitext(relative_path)[0]  # Bỏ phần .mp4

    # Tạo folder đầu ra tương ứng (tạo nếu không tồn tại)
    output_folder = os.path.join(output_root, relative_folder)
    os.makedirs(output_folder, exist_ok=True)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = int(fps * interval_sec)

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            img_name = f"{video_name}_frame_{saved_count:06d}.jpg"
            output_path = os.path.join(output_folder, img_name)
            cv2.imwrite(output_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"✅ {saved_count} ảnh từ: {relative_path}")

def process_folder(input_root, output_root, interval_sec=10):
    for video_file in glob.glob(os.path.join(input_root, "**", "*.mp4"), recursive=True):
        extract_frames(video_file, input_root, output_root, interval_sec)

def browse_input_folder():
    folder_selected = filedialog.askdirectory(title="Chọn thư mục gốc chứa video")
    input_folder_var.set(folder_selected)

def browse_output_folder():
    folder_selected = filedialog.askdirectory(title="Chọn thư mục lưu ảnh")
    output_folder_var.set(folder_selected)

def start_extraction():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    try:
        interval = int(interval_var.get())
        if input_folder == "" or output_folder == "" or interval <= 0:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
        else:
            # Tạo thư mục đầu ra nếu chưa có
            os.makedirs(output_folder, exist_ok=True)
            process_folder(input_folder, output_folder, interval)
            messagebox.showinfo("Thành công", "Đã hoàn thành việc trích xuất ảnh!")
    except ValueError:
        messagebox.showerror("Lỗi", "Thời gian trích xuất phải là số hợp lệ.")

# Tạo cửa sổ GUI
root = tk.Tk()
root.title("Trích xuất Slide Giảng dạy từ Video")

# Tạo các widget
input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
interval_var = tk.StringVar()

tk.Label(root, text="Chọn thư mục gốc chứa video:").pack(padx=10, pady=5)
tk.Entry(root, textvariable=input_folder_var, width=50).pack(padx=10, pady=5)
tk.Button(root, text="Chọn thư mục", command=browse_input_folder).pack(padx=10, pady=5)

tk.Label(root, text="Chọn thư mục lưu ảnh trích xuất:").pack(padx=10, pady=5)
tk.Entry(root, textvariable=output_folder_var, width=50).pack(padx=10, pady=5)
tk.Button(root, text="Chọn thư mục", command=browse_output_folder).pack(padx=10, pady=5)

tk.Label(root, text="Thời gian trích xuất (giây):").pack(padx=10, pady=5)
tk.Entry(root, textvariable=interval_var, width=20).pack(padx=10, pady=5)

tk.Button(root, text="Bắt đầu", command=start_extraction).pack(padx=10, pady=20)

# Chạy ứng dụng
root.mainloop()
