# names: {0: 'bike', 1: 'car', 2: 'cat', 3: 'dog',
#            4: 'motorcycle', 5: 'stairs', 6: 'green-light', 
#               7: 'red-light', 8: 'yellow-light'}

foc = 2660
real_height_car = 1.57
real_height_person = 1.70
real_height_motorcycle = 1.30

def distance(boxes):
    distance = []
    cls = boxes.cls.tolist()
    cls = [clss for clss in cls]
    cls = list(map(int, cls))

    for i, coords in enumerate(boxes.xywh.tolist()):
        h = coords[3]
        if cls[i] == 0:
            print("bike")
        if cls[i] == 1:
            print("car")
            distance.append((foc * real_height_car)/h)
        if cls[i] == 2:
            print("cat")
        if cls[i] == 3:
            print("dog")
        if cls[i] == 4:
            print("motorcycle")
            distance.append((foc * real_height_motorcycle)/h)
        if cls[i] == 5:
            print("stairs")
            distance.append((foc * real_height_person)/h)
        if cls[i] == 6:
            print("green-light")
        if cls[i] == 7:
            print("red-light")
        if cls[i] == 8:
            print("yellow-light")



    return distance