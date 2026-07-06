import cv2

def capture_from_camera(save_path="captured_food.jpg"):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise Exception("Could not access the webcam.")

    print("Camera opened. Point it at your food.\nPress 'c' to capture, or 'q' to quit.")
    captured_path = None

    while True:
        ret, frame = cam.read()
        if not ret:
            raise Exception("Failed to read from webcam.")

        cv2.imshow("Food Scanner - Press c to capture, q to quit", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            cv2.imwrite(save_path, frame)
            print(f"Photo captured and saved as {save_path}")
            captured_path = save_path
            break
        elif key == ord('q'):
            print("Capture cancelled.")
            break

    cam.release()
    cv2.destroyAllWindows()
    return captured_path