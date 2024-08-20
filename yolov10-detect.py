import cv2
import supervision as sv
from ultralytics import YOLO
import distance

model = YOLO(f'best29.pt')
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()  
cap=cv2.VideoCapture('test2.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
if not cap.isOpened():
    print("can't open the webcam")
while True:
    ret,frame=cap.read()
    # frame = cv2.resize(frame, (128, 72), interpolation=cv2.INTER_AREA)
    if not ret:
        break
    results = model(frame)[0]
    boxes = len(results.boxes.xywh.tolist())
    if boxes != 0:
        dist = distance.distance(boxes=results.boxes)
        print(dist)
    detections = sv.Detections.from_ultralytics(results)
    annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
    annotated_image = cv2.resize(annotated_image, (128*5, 72*5), interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam',annotated_image)
    k=cv2.waitKey(1)
    if k%256==27:
        print("Escape hit,closing...")
        break

cap.release()
cv2.destroyAllWindows()