class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vertice:
    def __init__(self, s, e):
        self.start = s
        self.end = e

class Face:
    def __init__(self, a, b, c, d, color):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.color = color
        
class FaceAndDepth(Face):
    def __init__(self, a: Point3D, b: Point3D, c: Point3D, d: Point3D, color, avgZ):
        Face.__init__(self, a, b, c, d, color)
        self.avgZ = avgZ