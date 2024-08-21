import cv2
import supervision as sv
from ultralytics import YOLOv10
import distance

model = YOLOv10(f'trained_weight/best.pt')
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
cap=cv2.VideoCapture('video/V_20240821_125044_ES5.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
if not cap.isOpened():
    print("can't open the webcam")
while True:
    ret,frame=cap.read()
    if not ret:
        break
    results = model(frame)[0]
    boxes = len(results.boxes.xywh.tolist())
    if boxes != 0:
        dist = distance.distance(results=results)
        print(f'Distance:{dist}')
    detections = sv.Detections.from_ultralytics(results)
    # print(detections)
    annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
    """for i, box in enumerate(results.boxes.xywh.tolist()):
        x, y, w, h = box
        label_text = f"Distance:{dict[i]:.2f}" if dict else "NO distance"
        cv2.putText(annotated_image, label_text, (int(x) - int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)"""
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
    annotated_image = cv2.resize(annotated_image, (192*5, 108*5), interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam',annotated_image)
    k=cv2.waitKey(1)
    if k%256==27:
        print("Escape hit,closing...")
        break

cap.release()
cv2.destroyAllWindows()