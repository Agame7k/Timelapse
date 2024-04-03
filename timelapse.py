import cv2
import time
import datetime
import tkinter as tk
import os
import threading
from PIL import Image, ImageTk

def capture_frames(interval=10, camera_port=0):
    cap = cv2.VideoCapture(camera_port)
    frame_count = 0

    filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.avi'
    output = 'Videos/' + filename 

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = 24.0

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)
        time.sleep(interval)

    cap.release()
    out.release()

def list_files(listbox):
    listbox.delete(0, tk.END)
    for file in os.listdir('Videos'):
        listbox.insert(tk.END, file)

def create_gui():
    root = tk.Tk()
    root.title("Image Files")

    listbox = tk.Listbox(root)
    listbox.pack(pady=15)

    # Create a label to display the image
    image_label = tk.Label(root)
    image_label.pack()

    def show_image(event):
        # Get the selected file
        file = listbox.get(listbox.curselection())

        # Open the image and display it
        image = Image.open('Images/' + file)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected

    # Bind the listbox's selection event to the show_image function
    listbox.bind('<<ListboxSelect>>', show_image)

    refresh_button = tk.Button(root, text="Refresh", command=lambda: list_files(listbox))
    refresh_button.pack()

    list_files(listbox)

    def check_selection():
        selection = listbox.curselection()
        if selection and selection[0] == listbox.size() - 1:
            list_files(listbox)
        root.after(1000, check_selection)

    check_selection()

    root.mainloop()


if __name__ == "__main__":
    gui_thread = threading.Thread(target=create_gui)
    gui_thread.start()

    capture_frames()