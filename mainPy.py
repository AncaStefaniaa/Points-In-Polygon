import math
from typing import List
from graphics import *


def read():
    with open("data.in") as file_in:
        cnt_points = int(file_in.readline())
        points = [(0, 0)]
        for line in file_in:
            x, y = map(int, line.split())
            points.append((x, y))
        # pentru a simplifica algoritmul, facem ca lista de points sa fie „circulara” pentru primul si ultimul element
        points[0] = points[cnt_points]
        points.append(points[1])
    return points, cnt_points


"""
    Testul de orientare -> se calculeaza determinantul 
    1   1   1
    a1  b1  c1
    a2  b2  c2
    Returneaza < 0, daca point_c este in DREAPTA segmentului determinat de point_a si point_b
    Returneaza > 0, daca point_c este in STANGA segmentului determinat de point_a si point_b
    Returneaza = 0, daca point_c este COLINIAR cu point_a si point_b
"""
def sign(point_a, point_b, point_c) -> int:
    # se calculeaza determinantul, folosind o formula mai scurta
    value = (point_b[0] - point_a[0]) * (point_c[1] - point_a[1]) - (point_c[0] - point_a[0]) * (point_b[1] - point_a[1])
    if value == 0:
        return 0
    return 1 if value > 0 else -1


"""
    Determinare orientare poligon (sens trigonometric sau antitrigonometric)
    Returneaza < 0 => SENS TRIGONOMETRIC
    Returneaza > 0 => SENS ANTITRIGONOMETRIC
    Returneaza = 0 => TOATE PUNCTELE COLINIARE
    Returneaza la fel ca functia sign
"""
def get_polygon_orientation(points, cnt_points) -> int:
    polygon_sign = 0
    i = 1
    # cautam primele 3 puncte necoliniare si le facem semnul cu functia sign
    while i <= cnt_points and polygon_sign == 0:
        polygon_sign = sign(points[i - 1], points[i + 1], points[i])
        i += 1
    return polygon_sign


"""
    Determinarea convexitatii pentru fiecare punct (cu ajutorul functiei sign)
"""
def get_points_convexity(points, cnt_points) -> List[int]:
    points_convexity = [0]
    for i in range(1, cnt_points + 1):
        points_convexity.append(sign(points[i - 1], points[i + 1], points[i]))
    return points_convexity


"""
    Determinare daca un punct este principal sau nu
    Returneaza -1, daca exista punct in interior
    Returneaza 1, daca nu exista punct in interior
"""
def no_points_in_triangle(points, cnt_points, idx1, idx2, idx3) -> int:
    # se modifica indicii pentru a usura munca cu primul si ultimul element, fara a trata cazuri speciale
    if idx1 == 0:
        idx1 = cnt_points
    if idx3 == cnt_points + 1:
        idx3 = 1


    for i in range(1, cnt_points + 1):
        if i != idx1 and i != idx2 and i != idx3:
            o1 = sign(points[idx1], points[idx2], points[i])
            o2 = sign(points[idx2], points[idx3], points[i])
            o3 = sign(points[idx3], points[idx1], points[i])

            right = (o1 < 0) or (o2 < 0) or (o3 < 0) # cel putin la dreapta unei drepte
            left = (o1 > 0) or (o2 > 0) or (o3 > 0) # cel putin la stanga unei drepte
            if (left and right) == 0:
                # pentru ca punctul sa fie in interior, trebuie sa fie de aceeasi parte a dreptelor
                return -1

    return 1

"""
    Determina pentru fiecare punct daca este principal sau neprincipal
    Un punct este PRINCIPAL, daca [Pi−1 Pi+1] este diagonala (echivalent: nu exista un alt varf in interiorul sau pe 
    laturile triunghiului determinat de Pi−1, Pi si Pi+1) si NEPRINCIPAL, altfel
"""
def points_type(points, cnt_points) -> List[int]:
    points_principality = [0]
    for i in range(1, cnt_points + 1):
        points_principality.append(no_points_in_triangle(points, cnt_points, i - 1, i, i + 1))
    return points_principality


"""
    Afisare de control in consola
"""
def print_points(points, cnt_points, points_convexity, points_principality):
    polygon_sign = get_polygon_orientation(points, cnt_points)
    if polygon_sign != 0:
        for i in range(1, cnt_points + 1):
            point_sign = points_convexity[i]
            if point_sign:
                print("Varful ", end=" ")
                print(i, end=" ")
                if point_sign == polygon_sign:
                    print("convex", end=" ")
                else:
                    print("concav", end=" ")
                if points_principality[i] == 1:
                    print("principal")
                else:
                    print("neprincipal")
            else:
                print("Toate punctele sunt coliniare")
    else:
        print("Toate punctele sunt coliniare")


"""
    Reprezentare grafica
"""
def graphic(points, cnt_points, points_convexity, points_principality):
    scale = 40  # scalare puncte pentru a le face vizibile
    window_height = 800
    window_width = 1200

    # convertire lista de tuples la lista de Points + scalare
    points_cpy = [Point(0, 0)]
    for i in range(1, cnt_points + 1):
        points_cpy.append(Point(window_width / 2 + points[i][0] * scale, window_height / 2 + points[i][1] * scale))

    polygon = Polygon(points_cpy[1 : cnt_points + 1]) # punctele din care este format poligonul

    win = GraphWin("Points in polygon", window_width, window_height) # afisare fereastra
    win.setCoords(0, 0, window_width, window_height)  # setare origine

    input_box = [[] for i in range(0, cnt_points + 1)]   # lista de etichete 
    polygon_sign = get_polygon_orientation(points, cnt_points) 

    # setare eticheta pentru fiecare varf
    for i in range(1, cnt_points + 1):
        if points_convexity[i] == 0 or polygon_sign == 0:
            input_box[i] = Entry(Point(points_cpy[i].x, points_cpy[i].y), len("Coliniare"))
            input_box[i].setText("Coliniare")
        elif points_principality[i] == -1 and points_convexity[i] != polygon_sign:
            input_box[i] = Entry(Point(points_cpy[i].x, points_cpy[i].y), len("Concav Nepr"))
            input_box[i].setText("Concav Nepr")
        elif points_principality[i] == 1 and points_convexity[i] != polygon_sign:
            input_box[i] = Entry(Point(points_cpy[i].x, points_cpy[i].y), len("Concav Pr"))
            input_box[i].setText("Concav Pr")
        elif points_principality[i] == -1 and points_convexity[i] == polygon_sign:
            input_box[i] = Entry(Point(points_cpy[i].x, points_cpy[i].y), len("Convex Nepr"))
            input_box[i].setText("Convex Nepr")
        elif points_principality[i] == 1 and points_convexity[i] == polygon_sign:
            input_box[i] = Entry(Point(points_cpy[i].x, points_cpy[i].y), len("Convex Pr"))
            input_box[i].setText("Convex Pr")

        input_box[i].setSize(8)

    polygon.setFill(color_rgb(255, 182, 203)) # colorare poligon in ROZ
    polygon.setOutline(color_rgb(199, 21, 133)) # culoare margine
    polygon.draw(win)   # desenare margini poligon

    # scriere etichete
    for i in range(1, cnt_points + 1):
         input_box[i].draw(win)

    # desenare axe
    Line(Point(window_width / 2, window_height), Point(window_width / 2, 0)).draw(win)  # Oy
    Line(Point(0, window_height / 2), Point(window_width, window_height / 2)).draw(win) # Ox

    oXStart = Entry(Point(20, window_height / 2), 4) # Ox punct de start
    oXStart.setText(str(int(-window_width / 2 / scale)))
    oXStart.draw(win)

    oXEnd = Entry(Point(window_width - 20, window_height / 2) , 4)  # Ox punct de final
    oXEnd.setText(str(int(window_width / 2 / scale)))
    oXEnd.draw(win)

    oYStart = Entry(Point(window_width / 2, 15) , 4)    # Oy punct de start
    oYStart.setText(str(int(-window_height / 2 / scale)))
    oYStart.draw(win)

    oYEnd = Entry(Point(window_width / 2, window_height - 15) , 4)  #Oy punct de final
    oYEnd.setText(str(int(window_height / 2 / scale)))
    oYEnd.draw(win)

    win.getMouse()  # asteptare click
    win.close()

def main():
    points, cnt_points = read()
    points_convexity = get_points_convexity(points, cnt_points)
    points_principality = points_type(points, cnt_points)
    print_points(points, cnt_points, points_convexity, points_principality)
    graphic(points, cnt_points, points_convexity, points_principality)

if __name__ == "__main__":
    main()

