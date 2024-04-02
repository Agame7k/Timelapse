import cv2
import time

def capture_frames(interval=10, camera_port=0, output='timelapse.avi'):
    cap = cv2.VideoCapture(camera_port)
    frame_count = 0

    # Get the frame's width, height, and frames per second
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = 24.0

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Write the frame into the file 'output'
        out.write(frame)

        # Wait for the specified interval
        time.sleep(interval)

    # Release everything when the job is finished
    cap.release()
    out.release()

if __name__ == "__main__":
    capture_frames()