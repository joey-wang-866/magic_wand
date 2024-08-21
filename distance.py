# names: {0: 'bicycle', 1: 'car', 2: 'cat', 3: 'cone', 4: 'crosswalk', 5: 'dog', 6: 'scooter', 7: 'motorcycle', 8: 'people', 9: 'stairs', 10: 'red-light', 11: 'yellow-light', 12: 'green-light'}

foc = 2660
real_height_car = 1.57
real_height_person = 1.70
real_height_motorcycle = 1.30

def distance(results):
    boxes = results.boxes
    names = results.names
    distance = []
    cls = boxes.cls.tolist()
    cls = [clss for clss in cls]
    cls = list(map(int, cls))

    for i, coords in enumerate(boxes.xywh.tolist()):
        h = coords[3]
        for j, name in enumerate(names):
            if cls[i] == name:
                print(f'Name:{names[j]}')




    return distance