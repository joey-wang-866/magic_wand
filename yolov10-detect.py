import cv2
import supervision as sv
from ultralytics import YOLO
from  ultralytics import YOLOv10
import distance
import time

# 初始化模型
model = YOLOv10('weight/train30_v10m_d3_imgsz1000/weights/best.pt')

# 初始化標註器
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

# 開啟影片檔案
cap = cv2.VideoCapture('video/way_to_buy_drink.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Can't open the video file")
    exit()

# 取得影片屬性
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_duration = 1.0 / fps

# 初始化影片寫入器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video/way_to_buy_drink.mp4', fourcc, fps, (frame_width, frame_height))

while True:
    start_time = time.time()  # 計時開始
    ret, frame = cap.read()
    if not ret:
        break

    # 使用模型進行偵測
    results = model(frame)[0]
    boxes = len(results.boxes.xywh.tolist())

    dist = []
    if boxes != 0:
        dist = distance.distance(results=results)
        print(f'Distance: {dist}')

    # 轉換偵測結果為 Supervision 的格式
    detections = sv.Detections.from_ultralytics(results)
    annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)

    # 在影像上顯示距離
    for i, box in enumerate(results.boxes.xywh.tolist()):
        x, y, w, h = box
        label_text = f"Distance: {dist[i]:.2f}m" if boxes != 0 else "NO distance"
        cv2.putText(annotated_image, label_text, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)

    # 標註影像
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

    # 寫入結果至影片文件
    out.write(annotated_image)

    # 計算每幀的處理時間並調整等待時間
    end_time = time.time()
    elapsed_time = end_time - start_time
    delay_time = max(int((frame_duration - elapsed_time) * 1000), 1)  # 保證至少等待1毫秒

    # 顯示結果
    cv2.imshow('Webcam', annotated_image)

    # 偵測按鍵以退出
    if cv2.waitKey(delay_time) & 0xFF == 27:  # 按下 ESC 退出
        print("Escape hit, closing...")
        break

# 釋放資源
cap.release()
out.release()
cv2.destroyAllWindows()
