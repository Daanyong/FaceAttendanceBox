import cv2
import os

# Ensure result directory exists
os.makedirs('./data/result', exist_ok=True)

# 이미지 검출기
def imageDetector(image_path, cascade, padding=20):
    # Load image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    results = cascade.detectMultiScale(
        gray,               # Input image
        scaleFactor=1.1,    # Scale factor for image pyramid
        minNeighbors=5,     # Minimum distance between detected objects
        minSize=(20, 20)    # Minimum size of detected objects
    )
    
    # Save detected faces with padding
    for idx, (x, y, w, h) in enumerate(results):
        # Calculate padded bounding box
        x_pad = max(x - 2 * padding, 0)
        y_pad = max(y - 4 * padding, 0)
        w_pad = min(w + 3 * padding, img.shape[1] - x_pad)
        h_pad = min(h + 5 * padding, img.shape[0] - y_pad)
        
        # Crop the face image with padding
        face_image = img[y_pad:y_pad + h_pad, x_pad:x_pad + w_pad]
        
        # Save face image to the result directory
        cv2.imwrite(f'./data/result/face_{idx}.jpg', face_image)

# Path to Haar cascade file
cascade_filename = 'haarcascade_frontalface_alt.xml'
# Load model
cascade = cv2.CascadeClassifier(cascade_filename)

# Path to save the captured image
image_path = './data/1.jpg'

# Capture image from webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    # Save the captured frame
    cv2.imwrite(image_path, frame)

# Release the webcam
cap.release()

# Detect faces in the captured image
imageDetector(image_path, cascade, padding=20)
