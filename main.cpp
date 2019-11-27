#include <iostream>
#include <math.h>


using namespace std;

const int DIM_MAX = 1000;

struct Point {
    double x, y;
    bool operator != (const Point &P) {
        return x != P.x && y != P.y;
    }
};

int cntPoints;
Point points[DIM_MAX];
int pointConvexity[DIM_MAX];
int pointPrincipality[DIM_MAX];

void read() {
    cin >> cntPoints;
    for (int i = 1; i <= cntPoints; ++i)
        cin >> points[i].x >> points[i].y;
    points[0] = points[cntPoints];
    points[cntPoints + 1] = points[1];
}

int sign(const Point &A, const Point &B, const Point &C) {
    double value = (B.x - A.x) * (C.y - A.y) - (C.x - A.x) * (B.y - A.y);
    if (value == 0)
        return 0;
    return value > 0 ? 1 : -1;
}

int getPolygonOrientation() {
    int polygonSign = 0;
    for (int i = 1; i <= cntPoints && polygonSign == 0; ++i)
        polygonSign = sign(points[i - 1], points[i + 1], points[i]);
    return polygonSign;
}

void getPointsConvexity() {
    for (int i = 1; i <= cntPoints; ++i)
        pointConvexity[i] = sign(points[i - 1], points[i + 1], points[i]);
}

double distance(const Point& A, const Point& B) {
    return sqrt(pow((A.x - B.x), 2) + pow((A.y - B.y), 2));
}

int pointInTriangle(int idx1, int idx2,int idx3){

    if (idx1 == 0)
        idx1 = cntPoints;
    if (idx3 == cntPoints + 1)
        idx3 = 1;

    Point p1 = points[idx1];
    Point p2 = points[idx2];
    Point p3 = points[idx3];

    for (int i = 1; i <= cntPoints; ++i)
        if (i != idx1 && i != idx2 && i != idx3){

            int o1 = sign(p1, p2, points[i]);
            int o2 = sign(p2, p3, points[i]);
            int o3 = sign(p3, p1, points[i]);


            //if the point is on the LEFT side of all the edges or if the point is ON any edge
            if ((o1 < 0 && o2 < 0 && o3 < 0))
                return -1;

            //if the point is on the RIGHT side of all the edges
            if ((o1 > 0 && o2 > 0 && o3 > 0))
                return -1;

            //if the point is on one edge
            if (!o1 && distance(p1, points[i]) + distance(points[i], p2) == distance(p1, p2))
                return -1;

            if (!o2 && distance(p2, points[i]) + distance(points[i], p3) == distance(p2, p3))
                return -1;

            if (!o3 && distance(p3, points[i]) + distance(points[i], p1) == distance(p3, p1))
                return -1;

        }

    return 1;

}

void pointsType() {
    for (int i = 1; i <= cntPoints; ++i)
        pointPrincipality[i] = pointInTriangle(i - 1, i, i + 1);
}

void print() {
    int polygonSign = getPolygonOrientation();
    if (polygonSign) {
        for (int i = 1; i <= cntPoints; ++i) {
            int pointSign = pointConvexity[i];
            if (pointSign) {
                cout << "Varful " << i << " este " << (pointSign == polygonSign ? "convex " : "concav ") <<
                     (pointPrincipality[i] == 1 ? "principal!\n" : "neprincipal!\n");
            }
            else {
                cout << "Puncte coliniare!\n";
            }
        }
    }
    else {
        cout << "Toate punctele sunt coliniare!\n";
        exit(EXIT_SUCCESS);
    }
}

int main() {
    read();
    getPointsConvexity();
    pointsType();
    print();
    return 0;
}