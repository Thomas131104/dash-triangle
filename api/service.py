import math
import models.triangle as triangle


def analyze_triangle(tri):

    if not tri.is_exist():

        raise ValueError("Tam giác không tồn tại")

    return {

        "edge_1": tri.a,
        "edge_2": tri.b,
        "edge_3": tri.c,

        "perimeter": tri.perimeter(),
        "area": tri.area(),

        "incircle_radius": tri.incircle_radius(),
        "circumcircle_radius": tri.circumcircle_radius(),

    }



def triangle_from_coords(x1,y1,x2,y2,x3,y3):

    A=triangle.Point(x1,y1)
    B=triangle.Point(x2,y2)
    C=triangle.Point(x3,y3)

    AB=A.distance_to_other(B)
    AC=A.distance_to_other(C)
    BC=B.distance_to_other(C)

    return triangle.Triangle(AB,AC,BC)



def triangle_ccc(a,b,c):
    return triangle.Triangle(a,b,c)



def triangle_cgc(a,b,angleC):
    c=math.sqrt(
        a*a+b*b-2*a*b*math.cos(angleC)
    )
    return triangle.Triangle(a,b,c)



def triangle_gcg(A,c,B):
    C=math.pi-A-B
    if C<=0:
        raise ValueError("Góc sai")
    a=c*math.sin(A)/math.sin(C)
    b=c*math.sin(B)/math.sin(C)

    return triangle.Triangle(a,b,c)