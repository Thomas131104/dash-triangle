import math
import numpy as np
from __hidden.__safe import _safe_acos, _safe_eq

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
    
    def distance_to_origin(self):
        return math.hypot(self.x, self.y)
    
    def distance_to_other(self, other : "Point"):
        return math.hypot(self.x - other.x, self.y - other.y)
    
    def middle(self, other: "Point"):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)
    
    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_exist(self):
        a, b, c = self.a, self.b, self.c
        return (
            a + b > c and
            a + c > b and
            b + c > a
        )
    
    def edge_type(self):

        if not self.is_exist():
            return None

        a, b, c = self.a, self.b, self.c

        if _safe_eq(a,b) and _safe_eq(b,c):
            return "Tam giác đều"
        elif _safe_eq(a,b) or _safe_eq(a,c) or _safe_eq(b,c):
            return "Tam giác cân"
        else:
            return "Tam giác thường"

    def angle_type(self):

        if not self.is_exist():
            return None

        biggest_angle = math.degrees(max(self.angles().values()))

        if biggest_angle > 90 and not _safe_eq(biggest_angle,90):
            return "Tam giác tù"
        elif _safe_eq(biggest_angle,90):
            return "Tam giác vuông"
        else:
            return "Tam giác nhọn"

    def perimeter(self):
        return self.a + self.b + self.c if self.is_exist() else None

    def area(self):
        if not self.is_exist():
            return None
        p = self.perimeter() / 2
        return math.sqrt(p * (p-self.a) * (p-self.b) * (p-self.c))

    def incircle_radius(self):
        if not self.is_exist():
            return None
        return 2 * self.area() / self.perimeter()

    def circumcircle_radius(self):
        if not self.is_exist():
            return None
        return self.a * self.b * self.c / (4 * self.area())

    def angles(self):
        a = self.a
        b = self.b
        c = self.c

        A = _safe_acos((b*b + c*c - a*a) / (2*b*c))
        B = _safe_acos((a*a + c*c - b*b) / (2*a*c))
        C = _safe_acos((a*a + b*b - c*c) / (2*a*b))

        return {
            "angle_a": A,
            "angle_b": B,
            "angle_c": C
        }



class TriangleWithCoords: 
    def __init__(self, x1, y1, x2, y2, x3, y3): 
        self.A = Point(x1, y1) 
        self.B = Point(x2, y2) 
        self.C = Point(x3, y3) 
        edges = Triangle( 
            a = self.B.distance_to_other(self.C), 
            b = self.A.distance_to_other(self.C), 
            c = self.A.distance_to_other(self.B) 
        ) 
        if not edges.is_exist(): 
            raise ValueError("3 điểm thẳng hàng không tạo thành tam giác!") 
        
        self.triangle_edges = edges 
        
        ## Các hàm dưới đây trả về theo kiểu dict với các keys: 
        ## intersect: trọng tâm / trực tâm / tâm đường tròn nội tiếp / ngoại tiếp của hàm đó 
        ## feet: là keys chứa 3 điểm là 3 đường kéo dài nối từ 1 điểm đi qua intersect và giao với đường đối diện 
        

    # ## Trọng tâm  
    def centroid(self): 
        return { 
            "intersect" : Point(
                (self.A.x + self.B.x + self.C.x) / 3, 
                (self.A.y + self.B.y + self.C.y) / 3
            ), 
            "feet" : { 
                "A_feet" : self.B.middle(self.C), 
                "B_feet" : self.A.middle(self.C), 
                "C_feet" : self.A.middle(self.B) 
                } 
            } 
    
    ## Trực tâm - 3 đường cao 
    def orthocenter(self): # Hàm này tìm chân đường cao từ first xuống cạnh second-third 
        def __foot_of_altitude(first: Point, second: Point, third: Point): 
            # Vector cạnh second-third 
            dx = third.x - second.x 
            dy = third.y - second.y 
            
            # Vector second-first 
            fx = first.x - second.x 
            fy = first.y - second.y 
            
            # Hệ số chiếu 
            t = (fx * dx + fy * dy) / (dx * dx + dy * dy) 
            
            # Tọa độ chân đường cao 
            foot_x = second.x + t * dx 
            foot_y = second.y + t * dy 
            return Point(foot_x, foot_y) 
        

        A, B, C = self.A, self.B, self.C 
        # 3 chân đường cao 
        H_A = __foot_of_altitude(A, B, C) 
        H_B = __foot_of_altitude(B, A, C) 
        H_C = __foot_of_altitude(C, A, B) 
        
        # Bây giờ tìm giao điểm của 2 đường cao (A-H_A và B-H_B) 
        # Viết dạng 2 điểm → phương trình đường thẳng 
            
        def line_from_points(P, Q): 
            a = Q.y - P.y 
            b = P.x - Q.x 
            c = a * P.x + b * P.y 
            return a, b, c 
        
        a1, b1, c1 = line_from_points(A, H_A) 
        a2, b2, c2 = line_from_points(B, H_B) 
        det = a1 * b2 - a2 * b1 
        
        if np.isclose(det, 0): 
            raise ValueError("Không xác định trực tâm") 
        
        x = (c1 * b2 - c2 * b1) / det 
        y = (a1 * c2 - a2 * c1) / det 
        return { 
            "intersect": Point(x, y), 
            "feet": { 
                "A_feet": H_A, 
                "B_feet": H_B, 
                "C_feet": H_C 
            } 
        } 
    
    ## đường tròn ngoại tiếp - 3 đường trung trực 
    def circumcircle(self): 
        A, B, C = self.A, self.B, self.C 
        x1, y1 = A.x, A.y 
        x2, y2 = B.x, B.y 
        x3, y3 = C.x, C.y 
        
        D = 2 * ( x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2) ) 
        if np.isclose(D, 0): 
            raise ValueError("Ba điểm thẳng hàng!") 
        
        Ox = ( (x1**2 + y1**2)*(y2 - y3) + (x2**2 + y2**2)*(y3 - y1) + (x3**2 + y3**2)*(y1 - y2) ) / D 
        Oy = ( (x1**2 + y1**2)*(x3 - x2) + (x2**2 + y2**2)*(x1 - x3) + (x3**2 + y3**2)*(x2 - x1) ) / D 
        center = Point(Ox, Oy) 
        radius = center.distance_to_other(A) 

            # Tạo 3 đường trung trực dạng kéo dài
        def perpendicular_bisector(P, Q):
            mid = Point((P.x + Q.x)/2, (P.y + Q.y)/2)

            dx = Q.x - P.x
            dy = Q.y - P.y

            # vector vuông góc
            perp_dx = -dy
            perp_dy = dx

            scale = 100  # kéo dài cho đẹp

            return {
                "x": [mid.x - perp_dx*scale, mid.x + perp_dx*scale],
                "y": [mid.y - perp_dy*scale, mid.y + perp_dy*scale]
            }

        lines = [
            perpendicular_bisector(A, B),
            perpendicular_bisector(B, C),
            perpendicular_bisector(C, A),
        ]


        return { 
            "intersect": center, 
            "radius": radius, 
            "foot" : { 
                "A_feet" : self.B.middle(self.C), 
                "B_feet" : self.A.middle(self.C), 
                "C_feet" : self.A.middle(self.B) 
            },
            "lines": lines
        } 
        
        
    ## đường trọn nội tiếp - 3 đường phân giác 
    def incircle(self): 
        A, B, C = self.A, self.B, self.C 
        
        def __angle_bisector(first: Point, second: Point, third: Point): 
            # độ dài hai cạnh kề đỉnh first 
            side1 = first.distance_to_other(second) 
            side2 = first.distance_to_other(third) 
            
            # điểm chia đoạn second-third theo tỉ lệ side1 : side2 # chú ý đảo trọng số đúng thứ tự 
            x = (side2 * second.x + side1 * third.x) / (side1 + side2) 
            y = (side2 * second.y + side1 * third.y) / (side1 + side2) 
            return Point(x, y) 
        
        # 3 chân phân giác 
        D = __angle_bisector(A, B, C) 
        E = __angle_bisector(B, A, C) 
        F = __angle_bisector(C, A, B) 
        
        # Tâm nội tiếp = giao 2 phân giác (A-D và B-E) 
        def line_from_points(P, Q): 
            a = Q.y - P.y 
            b = P.x - Q.x 
            c = a * P.x + b * P.y 
            return a, b, c 
        
        a1, b1, c1 = line_from_points(A, D) 
        a2, b2, c2 = line_from_points(B, E) 
        det = a1 * b2 - a2 * b1 
        
        if np.isclose(det, 0): 
            raise ValueError("Không xác định tâm nội tiếp") 
        
        Ix = (c1 * b2 - c2 * b1) / det 
        Iy = (a1 * c2 - a2 * c1) / det 
        center = Point(Ix, Iy) 
        
        # bán kính = khoảng cách từ tâm tới 1 cạnh (ví dụ BC) 
        # 
        # # dùng công thức khoảng cách điểm - đường thẳng # phương trình BC 
        a = C.y - B.y 
        b = B.x - C.x 
        c = a * B.x + b * B.y 
        r = abs(a*Ix + b*Iy - c) / np.sqrt(a*a + b*b) 
        return { 
            "intersect": center, 
            "radius": r, 
            "feet": { 
                "A_feet": D, 
                "B_feet": E, 
                "C_feet": F 
            } 
        }