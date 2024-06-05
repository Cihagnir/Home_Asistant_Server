from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

model = YOLO("yolo-Weights/yolov8n.pt",verbose=True)
classNames = ["person", "dog", "cat"]

confidence_threshold = 0.85

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    print("------------ RESULTS ------------")

    for r in results:
        boxes = r.boxes
        classes = r.names
        for box in boxes:
            if box.conf[0] > confidence_threshold:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                class_id = int(box.cls[0])
                class_name = classes[class_id]
                print(f"Class name which has confident : {class_name}")

                if class_name in classNames:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    org = (x1, y1 - 10)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv2.putText(img, f"{class_name} detected!", org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()