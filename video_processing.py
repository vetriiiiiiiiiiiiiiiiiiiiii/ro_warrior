import cv2
import numpy as np

class VideoProcessing:
    def __init__(self, model):
        self.model = model
        self.capture = cv2.VideoCapture(1)  # Use the first camera
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def process_video(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            # Preprocess the frame for the model
            processed_frame = self.preprocess_frame(frame)

            # Make predictions
            predictions = self.model.predict(processed_frame)

            # Analyze predictions and detect survivors
            self.detect_survivors(frame, predictions)

            # Detect faces
            self.detect_faces(frame)

            # Display the frame
            cv2.imshow('Video Feed', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.capture.release()
        cv2.destroyAllWindows()

    def preprocess_frame(self, frame):
        # Resize and normalize the frame for the model
        frame = cv2.resize(frame, (224, 224))  # Example size, adjust as needed
        frame = frame / 255.0  # Normalize
        return np.expand_dims(frame, axis=0)  # Add batch dimension

    def detect_survivors(self, frame, predictions):
        # Example logic to draw bounding boxes or labels based on predictions
        for prediction in predictions:
            if prediction['class'] == 'human' and prediction['confidence'] > 0.5:
                # Draw bounding box
                x, y, w, h = prediction['box']  # Assuming prediction contains box coordinates
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 2, 0), 2)
                cv2.putText(frame, '', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,2, 0), 2)

    def detect_faces(self, frame):
        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

        # Draw green boxes around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box
            cv2.putText(frame, 'human located', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Label
