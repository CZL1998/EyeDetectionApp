import cv2
from flask import Flask, render_template, Response, jsonify

# Flask app
app = Flask(__name__)

# OpenCV: face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Create a camera
camera = cv2.VideoCapture(0)

# Coordinate variables: left eye and right eye
left_eye_coords = (-1, -1)
right_eye_coords = (-1, -1)

# Detect eyes
def process_frame():
    global left_eye_coords, right_eye_coords
    while True:
        # カメラからフレームを読み込む
        # Capture a frame from the camera
        ret, frame = camera.read()
        if not ret:
            break

        # Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            # Draw a rectangle: face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            roi_gray = gray[y:y + h // 2, x:x + w]
            roi_color = frame[y:y + h // 2, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10, minSize=(30, 30))

            # If at least two eyes are detected
            if len(eyes) >= 2:
                eyes = sorted(eyes, key=lambda e: e[0])
                left_eye = eyes[0]
                right_eye = eyes[1]

                # Calculate the coordinates of the left and right eyes
                left_eye_coords = (x + left_eye[0] + left_eye[2] // 2, y + left_eye[1] + left_eye[3] // 2)
                right_eye_coords = (x + right_eye[0] + right_eye[2] // 2, y + right_eye[1] + right_eye[3] // 2)

                # Draw rectangles: eyes
                cv2.rectangle(roi_color, (left_eye[0], left_eye[1]), (left_eye[0] + left_eye[2], left_eye[1] + left_eye[3]), (0, 255, 0), 2)
                cv2.rectangle(roi_color, (right_eye[0], right_eye[1]), (right_eye[0] + right_eye[2], right_eye[1] + right_eye[3]), (0, 255, 0), 2)

        # Send to frontend: JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to display the homepage
@app.route('/')
def index():
    return render_template('index.html')

# video_feed
@app.route('/video_feed')
def video_feed():
    return Response(process_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_eye_coords')
def get_eye_coords():
    left_eye = tuple(map(int, left_eye_coords))
    right_eye = tuple(map(int, right_eye_coords))
    return jsonify(left_eye=left_eye, right_eye=right_eye)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

