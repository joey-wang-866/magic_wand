import cv2

win_width = 1920
win_height = 1080

win_width = 768
win_height = 432
mid_width = int(win_width / 2)
mid_height = int(win_height / 2)

foc = 1990.0       # 根据教程调试相机焦距
real_wid = 9.05   # A4纸横着的时候的宽度，视频拍摄A4纸要横拍，镜头横，A4纸也横
font = cv2.FONT_HERSHEY_SIMPLEX
w_ok = 1

capture = cv2.VideoCapture(0)
capture.set(3, win_width)
capture.set(4, win_height)

while (True):
    ret, frame = capture.read()
    # frame = cv2.flip(frame, 1)
    if ret == False:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, binary = cv2.threshold(gray, 140, 200, 60)    # 扫描不到纸张轮廓时，要更改阈值，直到方框紧密框住纸张
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary = cv2.dilate(binary, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)    # 查看所检测到的轮框
    for c in contours:
        if cv2.contourArea(c) < 1000:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
            continue

        x, y, w, h = cv2.boundingRect(c)  # 该函数计算矩形的边界框

        if x > mid_width or y > mid_height:
            continue
        if (x + w) < mid_width or (y + h) < mid_height:
            continue
        if h > w:
            continue
        if x == 0 or y == 0:
            continue
        if x == win_width or y == win_height:
            continue

        w_ok = w
        cv2.rectangle(frame, (x + 1, y + 1), (x + w_ok - 1, y + h - 1), (0, 255, 0), 2)

    dis_inch = (real_wid * foc) / (w_ok - 2)
    dis_cm = dis_inch * 2.54
    # os.system("cls")
    # print("Distance : ", dis_cm, "cm")
    frame = cv2.putText(frame, "%.2fcm" % (dis_cm), (5, 25), font, 0.8, (0, 255, 0), 2)
    frame = cv2.putText(frame, "+", (mid_width, mid_height), font, 1.0, (0, 255, 0), 2)

    cv2.namedWindow('res', 0)
    cv2.namedWindow('gray', 0)
    cv2.resizeWindow('res', win_width, win_height)
    cv2.resizeWindow('gray', win_width, win_height)
    cv2.imshow('res', frame)
    cv2.imshow('gray', binary)

    c = cv2.waitKey(40)
    if c == 27:
        break

cv2.destroyAllWindows()
