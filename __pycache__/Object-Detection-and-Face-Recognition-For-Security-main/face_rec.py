import cv2
import numpy as np
import face_recognition
import os

known_face_encodings = []
known_face_names = []

known_face_dir = 'known_faces'
for filename in os.listdir(known_face_dir):
  file_path = os.path.join(known_face_dir, filename)

  if os.path.isfile(file_path):
    img = face_recognition.load_image_file(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(img)

    if len(face_locations) > 0:
      face_encoding = face_recognition.face_encodings(img)[0]
      known_face_encodings.append(face_encoding)

      name = os.path.splitext(filename)[0]
      known_face_names.append(name)

cap = cv2.VideoCapture(0)

confidence_threshold = 0.95

while True:
  ret, frame = cap.read()

  face_locations = face_recognition.face_locations(frame)
  face_encodings = face_recognition.face_encodings(frame, face_locations)

  for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"
    confidence = 0.0

    if True in matches:
      first_match_index = matches.index(np.max(matches))
      name = known_face_names[first_match_index]
      confidence = np.max(matches)

    if confidence >= confidence_threshold:
      cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
      cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
      font = cv2.FONT_HERSHEY_DUPLEX
      cv2.putText(frame, f"{name} ({confidence:.2f})", (left + 6, bottom - 10), font, 1.0, (255, 255, 255), 1)
    else:
      cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
      cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
      font = cv2.FONT_HERSHEY_DUPLEX
      cv2.putText(frame, "Unknown", (left + 6, bottom - 10), font, 1.0, (255, 255, 255), 1)

  cv2.imshow('Webcam Face Recognition', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
