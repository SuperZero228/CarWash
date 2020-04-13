from django.conf import settings
import cv2 as cv
import numpy as np
import imutils
from math import floor, tan, sqrt, atan2, pi
from sklearn.cluster import KMeans
from pandas import DataFrame
import math
import os

# Путь к папке media
MEDIA = "C:\CREESTL\Programming\PythonCoding\semestr_4\CarWash\media"

# C:\CREESTL\Programming\PythonCoding\semestr_4\CarWash\CarWash\apps\users
PATH_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class Point():
    """
    Класс служит для обозначения факта, что точка уже соединена с какой-то другой или же свободна
    """

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.is_start = False  # точка - начало прямой
        self.is_end = False  # точка - конец прямой\
        self.connected = []  # здесь будут хранится координаты центроидов, которые соединены с данным


class Center():
    """
    Класс парковочного места
    """

    # id - номер центра парковки, coords - координаты центра парковки
    def __init__(self, id, coords):
        self.id = id
        self.coords = coords


def friendly_interface(img):
    """
    Пока что очень сырой интерфейс для работы с пользователем
    Взпаимодействие с пользователем через консоль
    """
    if img is None:
        print("You wrote a wrong path to the image! Try once again")
        exit()

    # пользователь выбирает, хочет ли он видеть все шаги обработки кадра
    print("Do you want to see all the steps of processing?")
    print("1) Yes\n2) No")
    choice = int(input())
    if choice == 1:
        show_steps = True
    else:
        show_steps = False
    return show_steps


def show(img=0, name_window=0, show=False):
    """
    Просто показывает изображение если надо показывать или закрывает все окна если не надо
    """
    if show:
        cv.imshow(name_window, img)
        cv.waitKey()
    else:
        cv.destroyAllWindows()


def search_degrees(all_points, min_d=0, max_d=0):
    """
    Нужна для поиска угла наклона парковки и линий котрые соответствуют этому углу
    ВАЖНО данная функция может возвращять разное число переменных (работает в двух режимах)
    1)если тебе нужно получить предпологаемый угол наклона от минимально возможного до максимально
    возможного то помести в нее координаты точек
    2)если нужно получить линии в этом диапазоне углов то помести в нее координаты точек и границы диапазона углов
    """
    if (min_d == 0) and (max_d == 0):
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
            if (min_d == 0) and (max_d == 0):
                key = math.trunc(degrees / 5)
                key_inv = math.trunc(degrees_inv / 5)
                if key_inv == 72:
                    key_inv = 71
                print(degrees, degrees_inv, key, key_inv, '\n')
                d[key] += 1
                d[key_inv] += 1
            elif (min_d < degrees) and (degrees < max_d):
                line = [int(all_points[i][0]), int(all_points[i][1]), int(point[0]), int(point[1])]
                line_list.append(line)
            i += 1
        print('\n')
    if (min_d == 0) and (max_d == 0):
        print(d)
        key_min = (max(d, key=d.get) * 5 - 20)
        key_max = key_min + 40
        print('key_min = ', key_min, 'key_max = ', key_max)
        return key_min, key_max
    else:
        print(line_list)
        return line_list


def nothing(*arg):
    """
    Нужна дла корректной работы следующей функции
    """
    pass


def manually_set_filter(img):
    """
    Пользователь вручную настраивает цветовой фильтр дла распознавания белых линий парковки
    """

    cv.namedWindow("result")  # главное окно
    cv.namedWindow("settings")  # окно настроек

    # создаем 6 бегунков для настроек параметров HLS
    cv.createTrackbar("h1", "settings", 0, 255, nothing)
    cv.createTrackbar("s1", "settings", 0, 255, nothing)
    cv.createTrackbar("v1", "settings", 0, 255, nothing)
    cv.createTrackbar("h2", "settings", 255, 255, nothing)
    cv.createTrackbar("s2", "settings", 255, 255, nothing)
    cv.createTrackbar("v2", "settings", 255, 255, nothing)

    while True:

        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # считываем значения бегунков
        h1 = cv.getTrackbarPos("h1", "settings")
        s1 = cv.getTrackbarPos("s1", "settings")
        v1 = cv.getTrackbarPos("v1", "settings")
        h2 = cv.getTrackbarPos("h2", "settings")
        s2 = cv.getTrackbarPos("s2", "settings")
        v2 = cv.getTrackbarPos("v2", "settings")

        # формируем начальный и конечный цвет фильтра
        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        # накладываем фильтр на кадр в модели HSV
        thresh = cv.inRange(hsv, h_min, h_max)

        cv.imshow("result", thresh)

        # для окончания настройки фильтра необходимо нажать на q
        ch = cv.waitKey(5)
        if ch == ord("q"):
            cv.destroyAllWindows()

            return h_min, h_max  # после того как пользователь нажимает на q то возвращаются границы


def apply_filter(img, black_or_white, green):
    """
    Эта функция создает "маски" которые фильтруют все пиксели, оставляя только те, цвет которых
    указан
    """
    # кадр переводится в формат HSV
    image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    if black_or_white == True:
        # маска для белого цвета в формате HLS
        lower, upper = manually_set_filter(img)
        # ниже - универсальный фильтр для белого цвета
        # lower = np.uint8([0, 0, 211])
        # upper = np.uint8([255, 65, 255])
        white_mask = cv.inRange(image, lower, upper)
        print("Applying white filter")
        mask = white_mask
        return mask
    if green == True:
        # маска для зеленого цвета
        # применяется, чтобы отфильтровать все, кроме линий Хофа
        lower = np.uint8([0, 196, 197])
        upper = np.uint8([255, 255, 255])
        green_mask = cv.inRange(image, lower, upper)
        print("Applying green filter")
        mask = green_mask
        return mask


def lines_to_array(lines):
    """
    Функция переводит линии в формат массива
    """
    new = []
    for i, line in enumerate(lines):
        new.append(np.array(line[0]).tolist())
    return new


def npoint2array(points):
    """
    Функция переводит точки из формата numpy в формат массива
    """
    output = []
    for i, point in enumerate(points):
        output.append(np.array(point[0]).tolist())
    return output


def delete_short_lines(lines):
    """
    Функция удаляет все слишком короткие линии
    """
    max_length = 0
    new = []
    for line in lines:
        line = np.array(line).tolist()
        x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
        length = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if length > max_length:
            max_length = length
    desired_length = max_length / 2  # требуемая длина - половина максимальной
    for line in lines:
        x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
        length = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if length > desired_length:  # если длина линии больше требуемой (половины максимальной), то она возвращается
            new.append(line)

    lines = new
    lines = np.array(lines)
    return lines


def only_different_cnts(contours):
    """
    Функция удаляет из массива контуров одинаковые контуры
    """
    cnt_box = {}  # словарь (номер контура-бокс)
    for i, c in enumerate(contours):
        rect = cv.minAreaRect(c)  # это типа tuple
        box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = np.int0(box)  # округление координат
        box = list(box)  # переводим из формала tuple внешний массив
        for i in range(len(box) - 1):
            box[i] = list(box[i])  # переводим из формата tuple внутренние подмассивы

        cnt_box[i] = box  # заносим в словарь

    for i, box in cnt_box.items():
        for j in range(i, len(cnt_box.keys()) - 1):  # от i и до конца массива ключей
            another_box = cnt_box[j]
            if box == another_box:
                print("Found similar contours...Deleting them")
                to_delete = contours[j]
                contours.remove(
                    to_delete)  # если нашли одинаковые контуры, то сразу из массива удаляем все, кроме первого

    return contours  # возвращаем массив без повторений


def find_distance(p1, p2):
    """
    Функция находит расстояние между двумя точками(центроидами)
    """
    distance = sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    return distance


def find_distance_class(p1, p2):
    """
    Функция находит расстояние между двумя точками, представленными через класс
    """
    distance = sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)
    return distance


def only_different_centroids(centroids):
    """
    Функция удаляет центроиды, находящиеся близко друг к другу
    """
    new = []
    for c in centroids:
        new.append(np.array(c).tolist())
    for c in new:
        for a in new:
            if c != a:
                if find_distance(c, a) < 20:  # это расстяние можно варьировать
                    new.remove(a)

    return new


def only_different_park_centers(centers):
    """
    Функция удаляет ложно обнаруженные центры парковок, находящиеся близко друг к другу
    """
    for c in centers:
        for a in centers:
            if c != a:
                if find_distance(c, a) < 20:  # это расстяние можно варьировать
                    centers.remove(a)

    return centers


def to_class_list(centroids):
    """
    Преобразует массив центроидов в массив экземпляров классов
    """
    class_list = []
    for centroid in centroids:
        class_list.append(Point(centroid[0], centroid[
            1]))  # создаем массив экземпляров класса чтобы потом понимать какие точки соединены, а какие - нет
    centroids = class_list

    return centroids


def approx_to_x_and_y(approx):
    """
    Функция переводит approx в координаты x и y
    """
    x = []
    y = []
    for el in approx:
        el = np.array(el).tolist()
        el = el[0]
        x.append(el[0])
        y.append(el[1])
    return x, y


def search_centers(contours, img, min_area, show_steps):
    """
    Эта функция ищет центры контуров и фильтрует все контуры от шума
    """
    ##################################################################################################################################
    # Добавить проверку не входит ли центроида одного экземпляра класса парковочного места в контур другого добавить класс парковочное место
    ##################################################################################################################################

    centers = []  # массив координтак центров парковок (не центроидов!)
    good_contours = []  # массив подходящих нам контуров
    for i, c in enumerate(contours):
        rect = cv.minAreaRect(c)  # находится прямоугольник, вписанный в контур
        area = int(rect[1][0] * rect[1][1])  # вычисление площади
        box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = np.int0(box)  # округление координат
        box = np.array(box).tolist()
        perimeter = cv.arcLength(c, True)
        epsilon = 0.02 * perimeter
        approx = cv.approxPolyDP(c, epsilon, False)

        if area > min_area:
            # отсеиваются контуры, у которых слишком много изгибов
            if (len(approx)) in range(5, 7):
                cv.drawContours(img, [c], -1, (0, 0, 255), 3)  # рисуются контуры на чистом кадре
                good_contours.append(c)  # координаты контуры добавляются в массив, из которого потом будут извлечены
                x1, y1 = box[0][0], box[0][1]
                x2, y2 = box[2][0], box[2][1]
                center = [(x1 + x2) / 2, (y1 + y2) / 2]
                centers.append(center)  # добавляет координаты центра парковки в массив, чтобы потом их нарисовать
                show(img, "rect", show_steps)
    return centers


def lines_processing(for_lines, with_lines, show_steps, W):
    """
    Эта функция фильтрует а потом рисует линии хофа на предварительно обработанном изображении
    """
    # минимальная длина линии и минимальный разрыв между линиями
    min_length = W / 100
    max_gap = W / 80
    # находятся все линии на кадре
    lines = cv.HoughLinesP(for_lines, rho=1, theta=np.pi / 180, threshold=50, minLineLength=min_length,
                           maxLineGap=max_gap)
    # переводим линии в формат массива
    lines = lines_to_array(lines)
    # иногда, если находятся линии во весь экран, то слишком много подходящих из-за этого удаляется
    lines = delete_short_lines(lines)
    # все линии рисуются на кадре
    for line in lines:
        x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
        cv.line(with_lines, (x1, y1), (x2, y2), (0, 255, 0), 3)
    show(with_lines, "Hough_lines", show_steps)
    return with_lines


def image_processing(img, show_steps):
    """
    Занимается предварительной обработкой изображения и узнает его форму
    """
    # размер кадра изменяется для удобства
    original_img = imutils.resize(img, width=800)
    (H, W) = original_img.shape[:2]
    # ограничение в 0.002 сильно влияет на корректность работы - его можно варьировать
    show(original_img, "original_img", show_steps)

    # убираются шумы с фото
    no_noize = cv.bilateralFilter(original_img, 11, 17, 17)

    # накладывается белый фильтр, чтобы потом применить линии Хофа
    white_img = apply_filter(no_noize, True, False)
    show(white_img, "white_filter", show_steps)
    return original_img, white_img, H, W


def search_contours(edges, for_contours, show_steps):
    """
    Ищет контуры убирает контуры больше похожие на шум
    """
    contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    print("Found contours: ", len(contours))
    # удаляются все одинаковые контуры, чтобы не рисовать их много раз
    contours = only_different_cnts(contours)
    print("Final number of contours: ", len(contours))
    # рисуются все полученные контуры
    cv.drawContours(for_contours, contours, -1, (0, 255, 0), 2)
    show(for_contours, "all_contours", show_steps)
    return contours


def search_key_points(contours, for_approx, show_steps):
    """
    Ищет кластеры по большому количеству точек, центры этих кластеров (ключевые точки) и фильтрует к.т.
    """
    # Словарь координат точек approx
    data = {
        "x": [],
        "y": []
    }

    approx_lenghts = []
    for i, c in enumerate(contours):
        perimeter = cv.arcLength(c, True)
        # эпсилон - максимальное расстояние от настоящего угла на картинке и его "предсказания"
        # True отвечает за замыкание первой и последней точек
        epsilon = 0.02 * perimeter

        # мест четное -> approx = мест * 5
        # мест нечетное -> approx = мест * 4 + 1

        approx = cv.approxPolyDP(c, epsilon, False)  # находим незамкнутые контуры

        # надо ограничить длину - не надо добавлять контуры из 200 точек
        if len(approx) // 4 < 2:
            approx_lenghts.append(len(approx))

        # находим все x и y координаты точек
        x, y = approx_to_x_and_y(approx)
        for each_x in x:
            data["x"].append(each_x)
        for each_y in y:
            data["y"].append(each_y)

        # рисуются точки
        cv.drawContours(for_approx, approx, -1, (0, 255, 0), 3)

    show(for_approx, "approx", show_steps)
    data_frame = DataFrame(data, columns=["x", "y"])
    # это - ожидаемое число кластеров центроидов
    num_of_clusters = sum(approx_lenghts) // 2

    # применятеся алгоритм kmeans чтобы распределить все центроиды на кластеры
    key_means = KMeans(n_clusters=num_of_clusters).fit(data_frame)
    centroids = key_means.cluster_centers_
    centroids = only_different_centroids(centroids)

    return centroids


def process(original_img, show_steps):
    """
    главная функция программы, которая вызывает все, описанные выше
    на вход подается кадр с камеры
    на выходе получаем тот же кадр с размеченными на нем парковочными местами с номерами, расставленными на них
    """


    original_img, white_img, H, W = image_processing(original_img, show_steps)

    min_area = (W * H) * 0.002  # это минимальная площадь контура, которая будет обрабатываться
    with_lines = lines_processing(white_img, original_img.copy(), show_steps, W)

    # на кадр с нарисованными зелеными линиями применяется фильтр зеленого цвета
    with_lines = apply_filter(with_lines, False, True)
    show(with_lines, "green_filter", show_steps)

    # находятся все грани
    edges = cv.Canny(with_lines, 100, 200)
    show(edges, "edges", show_steps)

    # создаем копии для рисования на них
    for_centroids = original_img.copy()
    for_centroids_2 = for_centroids.copy()
    for_final_contours = original_img.copy()
    for_pure_rects = original_img.copy()

    # находятся все конутры
    contours = search_contours(edges, original_img.copy(), show_steps)

    # находятся центроиды по контурам
    centroids = search_key_points(contours,  original_img.copy(), show_steps)

    # _______________________________________________________________________________________________________________________
    print(centroids)
    min_d, max_d = search_degrees(centroids)
    print(min_d, max_d)
    line_list = search_degrees(centroids, min_d, max_d)
    for line in line_list:
        cv.line(with_lines, (line[0], line[1]), (line[2], line[3]), (255, 255, 255), 5)
    show(with_lines, "preparatory_result", show_steps)

    centroids = to_class_list(centroids)  # делаем массив классов вместо просто массива

    # все центриды рисуются в виде синих кругов
    if show_steps:
        for c in centroids:
            cv.circle(for_centroids_2, (int(c.x), int(c.y)), 5, (255, 0, 0), 3)
    show(for_centroids_2, "all_centroids", show_steps)

    # еще раз находятся все контуры
    contours, _ = cv.findContours(with_lines, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # все контуры рисуются
    cv.drawContours(for_final_contours, contours, -1, (0, 255, 0), 3)
    show(for_final_contours, "final_contours", show_steps)

    # ищем центры всех контуров и фильтруем их
    centers = search_centers(contours, for_pure_rects, min_area, show_steps)

    # создаем массив классов центров парковок
    centers_classes = []
    # удаляем центры, которые накладываются друг на друга
    centers = only_different_park_centers(centers)
    # уже после того, как нарисовали прямоугольники - рисуем номера, чтобы они были поверх них
    id = 0
    for i, center in enumerate(centers):
        # в массив добавляем новый центр
        centers_classes.append(Center(id, center))
        cv.circle(for_pure_rects, (int(center[0]), int(center[1])), 5, (255, 255, 0), 3)
        # ставим id над центром
        cv.putText(for_pure_rects, str(id + 1), (int(center[0]) + 10, int(center[1]) - 10), cv.FONT_HERSHEY_SIMPLEX,
                   0.5, (255, 0, 0), 2)
        id += 1
    show(for_pure_rects, "FINAL", show_steps)

    # Удалаяет все фреймы
    show(show=False)

    # финальная версия картинки сохраняется в папку, а потом выводится на HTML страницу
    #cv.imwrite(settings.MEDIA_ROOT + "FINAL.png", for_pure_rects)
    cv.imwrite(MEDIA + '/output/parking.jpg', for_pure_rects)

    # после всех преобразований возвращает:
    # финальную картинку
    # массив классов центра парковок (id, координаты центра)
    # массив контуров, подходящих нам (парковок)
    return for_pure_rects
