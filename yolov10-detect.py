import cv2
import supervision as sv
from ultralytics import YOLO
from ultralytics import YOLOv10
import distance
import time
import os

model = YOLOv10('weights/train102/weights/best.pt')

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

cap = cv2.VideoCapture('video/V_20240821_183401_ES5.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Can't open the video file")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_duration = 1.0 / fps

output_folder = 'output_video/7'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

frame_count = 0

while True:
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    boxes = len(results.boxes.xywh.tolist())

    dist = []
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

    frame_filename = os.path.join(output_folder, f'frame_{frame_count:05d}.png')
    cv2.imwrite(frame_filename, annotated_image)
    frame_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    delay_time = max(int((frame_duration - elapsed_time) * 1000), 1)

    cv2.imshow('Webcam', annotated_image)

    if cv2.waitKey(delay_time) & 0xFF == 27:
        print("Escape hit, closing...")
        break

cap.release()
cv2.destroyAllWindows()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video/7/reconstructed_video.mp4', fourcc, fps, (frame_width, frame_height))

for i in range(frame_count):
    frame_filename = os.path.join(output_folder, f'frame_{i:05d}.png')
    frame = cv2.imread(frame_filename)
    out.write(frame)

out.release()
print("Video reconstruction complete.")
