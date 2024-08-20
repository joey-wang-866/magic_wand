import cv2
import supervision as sv
from ultralytics import YOLO

foc = 266
real_hight_car = 15.7

model = YOLO(f'best45.pt')
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
    boxes = len(results.boxes.xyxy.tolist())
    if boxes != 0:
        for coords in results.boxes.xywh.tolist():
            x = coords[0]
            y = coords[1]
            w = coords[2]
            h = coords[3]
            distance = (foc * real_hight_car)/h
            print(f'{distance:.2f}')
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