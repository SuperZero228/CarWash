import math
import cv2
import numpy as np



def search_degrees(all_points, min_d = 0, max_d = 0):
    if(min_d == 0) and (max_d == 0):
        d = {a: 0 for a in range(72)}
        print(d)
    else:
        line_list = []
    for point in all_points:
        print(all_points.index(point))
        print(point)
        print('___________________________')
        i = all_points.index(point) + 1
        while i < len(all_points):
            print(all_points[i], "and", point)
            # point and all_points
            vector_ax = all_points[i][0] - point[0]
            vector_ay = all_points[i][1] - point[1]
            print(vector_ax, vector_ay)
            degrees = math.degrees(math.acos((vector_ax) / (math.sqrt(vector_ax ** 2 + vector_ay ** 2))))
            if (vector_ax == 0) and (vector_ay == 0):
                i += 1
                continue
            if vector_ay < 0:
                degrees = 180 - degrees
            degrees_inv = degrees + 180
            if(min_d == 0) and (max_d == 0):
                key = math.trunc(degrees / 5)
                key_inv = math.trunc(degrees_inv / 5)
                if key_inv == 72:
                    key_inv = 71
                print(degrees, degrees_inv, key, key_inv, '\n')
                d[key] += 1
                d[key_inv] += 1
            elif (min_d < degrees) and (degrees < max_d):
                line = [all_points[i][0], all_points[i][1], point[0], point[1]]
                line_list.append(line)
            i += 1
        print('\n')
    if(min_d == 0) and (max_d == 0):
        print(d)
        key_min = (max(d, key=d.get) * 5 - 5)
        key_max = key_min + 10
        print('key_min = ', key_min, 'key_max = ', key_max)
        return key_min, key_max
    else:
        print(line_list)
        return line_list

blank_image = np.zeros((500, 500, 3), np.uint8)

points = []
while(True):
    point = [0, 0]
    x = input("x = ")
    y = input("y = ")
    if(x == ' ') and (y == ' '):
        break
    point[0] = int(x)
    point[1] = int(y)
    points.append(point)
    print(points)
for point in points:
    cv2.circle(blank_image, (point[0], point[1]), 10, (0, 0, 255))
min_d, max_d = search_degrees(points)
print(min_d, max_d)
line_list = search_degrees(points, min_d=min_d, max_d=max_d)

for line in line_list:
    cv2.line(blank_image, (line[0], line[1]), (line[2], line[3]), (255, 255, 255), 5)
cv2.imshow("Img", blank_image)
cv2.waitKey(0)
