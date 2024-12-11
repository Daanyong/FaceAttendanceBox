import cv2
import timeit
import os

# Ensure result directory exists
os.makedirs('./data/result', exist_ok=True)

# 이미지 검출기
def imageDetector(image_path, cascade):
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
    
    # Save detected faces
    for idx, box in enumerate(results):
        x, y, w, h = box
        x, y = x-40, y-40
        w, h = w+50, h+50
        face_image = img[y:y+h, x:x+w]
        # Save face image to the result directory
        cv2.imwrite(f'./data/result/face_{idx}.jpg', face_image)

# Path to Haar cascade file
cascade_filename = 'haarcascade_frontalface_alt.xml'
# Load model
cascade = cv2.CascadeClassifier(cascade_filename)

# Path to input image
image_path = './data/1.jpg'

# Detect faces in the image
imageDetector(image_path, cascade)
