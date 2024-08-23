import cv2
import supervision as sv
from ultralytics import YOLOv10
import distance

model = YOLOv10(f'weight/train_50_v10_d3_no_stairs/weights/best.pt')
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

cap = cv2.VideoCapture('video/way_back_to_ASML.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Can't open the webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    boxes = len(results.boxes.xywh.tolist())

    if boxes != 0:
        dist = distance.distance(results=results)
        print(f'Distance: {dist}')

    detections = sv.Detections.from_ultralytics(results)
    annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)

    for i, box in enumerate(results.boxes.xywh.tolist()):
        x, y, w, h = box
        label_text = f"Distance: {dist[i]:.2f}m" if boxes != 0 else "NO distance"
        cv2.putText(annotated_image, label_text, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)

    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
    annotated_image = cv2.resize(annotated_image, (192*9, 108*9), interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam', annotated_image)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        print("Escape hit, closing...")
        break

cap.release()
cv2.destroyAllWindows()
