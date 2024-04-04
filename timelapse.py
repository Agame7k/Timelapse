import cv2
import glob
import os
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread

# Get list of image files
image_files = glob.glob('photos/*.jpg')  # adjust the pattern as needed
image_files.sort(key=os.path.getmtime)

# Get the most recent video file
video_files = glob.glob('*.avi')
if video_files:
    video_file = max(video_files, key=os.path.getmtime)
else:
    video_file = None

root = tk.Tk()
root.attributes('-fullscreen', True)

# Create a canvas to display the image and video
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

def update_image():
    if image_files:
        # Display the next image
        image_file = image_files.pop(0)
        image = Image.open(image_file)

        # Resize the image to fit the window
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor='nw', image=photo)
        canvas.image = photo

        # Schedule the next update
        root.after(5000, update_image)  # adjust the delay as needed
    else:
        # Play the video
        if video_file is not None:
            cap = cv2.VideoCapture(video_file)
            if not cap.isOpened():
                print(f"Could not open video file {video_file}")
                return

            # Create an image on the canvas to update for each frame
            photo_image = None

            frame_count = 0
            while True:
                ret, frame = cap.read()
                if ret:
                    # Skip every other frame
                    frame_count += 1
                    if frame_count % 2 != 0:
                        continue

                    # Resize the frame to fit the window
                    frame = cv2.resize(frame, (root.winfo_screenwidth(), root.winfo_screenheight()))

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

                    if photo_image is None:
                        photo_image = canvas.create_image(0, 0, anchor='nw', image=photo)
                    else:
                        canvas.itemconfig(photo_image, image=photo)

                    canvas.image = photo
                    root.update()
                else:
                    break
            cap.release()

        # Start over with the first image
        image_files.extend(glob.glob('photos/*.jpg'))
        image_files.sort(key=os.path.getmtime)
        update_image()

update_image()

root.mainloop()