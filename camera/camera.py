import cv2 #webcam and processing of image data.

def capture_from_camera(save_path="captured_food.jpg"):
    
    
                              
    cam = cv2.VideoCapture(0)#creates a connection to the hardware 
    
    if not cam.isOpened():
        raise Exception("Could not access the webcam.")

    print("Camera opened. Point it at your food.\nPress 'c' to capture, or 'q' to quit.")
    
    captured_path = None    #this value is expected yo be returnd latr that's why none if user hasn't captured the image

    while True:
        ret, frame = cam.read() #ret gets True/False,frame gets the actual raw image pixel data.
        
        if not ret:
            raise Exception("Failed to read from webcam.")

        cv2.imshow("Food Scanner - Press c to capture, q to quit", frame)#opens a pop-up window on your screen to show the current video frame
        
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            cv2.imwrite(save_path, frame)  # saves the current frame (image data) to the hard drive at the save_path location
            print(f"Photo captured and saved as {save_path}")
            
            captured_path = save_path
            break
            
        elif key == ord('q'):
            print("Capture cancelled.")
            break

    cam.release() 
    
    cv2.destroyAllWindows()
    
    # sends the final image path back to the main script so it can be passed to the LogMeal API.
    return captured_path

