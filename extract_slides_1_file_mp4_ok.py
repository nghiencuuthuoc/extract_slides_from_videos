import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import PhotoImage

def extract_frames(video_path, output_folder, interval_sec=10):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frame per second
    frame_interval = int(fps * interval_sec)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
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
    return saved_count

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        video_path_var.set(file_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_var.set(folder_path)

def run_extraction():
    video_path = video_path_var.get()
    output_folder = output_folder_var.get()
    interval_sec = int(interval_sec_var.get())

    if not video_path or not output_folder:
        messagebox.showerror("Error", "Vui lòng chọn đầy đủ video và thư mục xuất")
        return

    try:
        saved_count = extract_frames(video_path, output_folder, interval_sec)
        messagebox.showinfo("Success", f"Trích xuất {saved_count} ảnh thành công!")
    except Exception as e:
        messagebox.showerror("Error", f"Đã có lỗi xảy ra: {str(e)}")

# --- Cấu hình GUI ---
root = tk.Tk()
root.title("Trích Xuất Ảnh Từ Video MP4")

# Thêm hình nền
bg_image = PhotoImage(file="./nct_logo.png")  # Đường dẫn đến hình nền
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Biến cho GUI
video_path_var = tk.StringVar()
output_folder_var = tk.StringVar()
interval_sec_var = tk.StringVar(value="10")  # Mặc định là 10 giây

# Giao diện
tk.Label(root, text="Chọn file video (MP4):", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
tk.Entry(root, textvariable=video_path_var, width=40).pack(pady=5)
tk.Button(root, text="Chọn video", command=browse_file).pack(pady=5)

tk.Label(root, text="Chọn thư mục xuất ảnh:", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
tk.Entry(root, textvariable=output_folder_var, width=40).pack(pady=5)
tk.Button(root, text="Chọn thư mục", command=browse_output_folder).pack(pady=5)

tk.Label(root, text="Thời gian giữa các ảnh (giây):", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
tk.Entry(root, textvariable=interval_sec_var, width=40).pack(pady=5)

tk.Button(root, text="Chạy Trích Xuất", command=run_extraction).pack(pady=20)

# Hiển thị cửa sổ
root.mainloop()
