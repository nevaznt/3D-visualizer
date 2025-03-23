import pygame as py
from sys import exit
from model import Model
from point import Point3D
from point import Point2D
from point import FaceAndDepth
import math

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FOV = 10
CAMERAX = SCREEN_WIDTH/2
CAMERAY = SCREEN_HEIGHT/2

MODELPATH = 'creeper.txt'

objRotationX = 0.0
objRotationY = 0.0
objSize = 100
model = Model(MODELPATH)

showPoints = False
showOutline = True
showFaces = True

def projection(point: Point3D) -> Point2D:
    global objSize
    return Point2D(CAMERAX + (FOV * point.x) / (FOV+point.z) * objSize, CAMERAY + (FOV * point.y) / (FOV+point.z) * objSize)

def rotateX(point: Point3D,rotation) -> Point3D:
    returnPoint = Point3D(0, 0, 0)
    returnPoint.x = point.x
    returnPoint.y = math.cos(rotation) * point.y - math.sin(rotation) * point.z
    returnPoint.z = math.sin(rotation) * point.y + math.cos(rotation) * point.z
    return returnPoint

def rotateY(point: Point3D, rotation) -> Point3D:
    returnPoint = Point3D(0, 0, 0)
    returnPoint.x = math.cos(rotation) * point.x - math.sin(rotation) * point.z
    returnPoint.y = point.y
    returnPoint.z = math.sin(rotation) * point.x + math.cos(rotation) * point.z
    return returnPoint

def drawVertexes():
    global objRotationX, objRotationY
    
    for point in model.points:
            rotatedPoint = rotateX(rotateY(point, objRotationX), objRotationY)
            point = projection(rotatedPoint)
            py.draw.circle(screen, 'red', [point.x, point.y], 3)

    return

def drawVertices():
    global objRotationX, objRotationY
    
    for vertice in model.vertices:
            startPoint = rotateX(rotateY(model.points[vertice.start], objRotationX), objRotationY)
            endPoint = rotateX(rotateY(model.points[vertice.end], objRotationX), objRotationY)
            start = projection(startPoint)
            end = projection(endPoint)
            py.draw.line(screen, 'black', [start.x, start.y], [end.x, end.y], 4)

    return

def drawFaces():
    global objRotationX, objRotationY
    
    faces = []
    for face in model.faces:
        a = rotateX(rotateY(model.points[face.a], objRotationX), objRotationY)
        b = rotateX(rotateY(model.points[face.b], objRotationX), objRotationY)
        c = rotateX(rotateY(model.points[face.c], objRotationX), objRotationY)
        d = rotateX(rotateY(model.points[face.d], objRotationX), objRotationY)        
        faces.append(FaceAndDepth(a, b, c, d, face.color, (a.z + b.z + c.z + d.z) / 4))

    g = 0
    while g < len(faces)-1:
        if(faces[g].avgZ > faces[g+1].avgZ):
            f = FaceAndDepth(faces[g+1].a, faces[g+1].b, faces[g+1].c, faces[g+1].d, faces[g+1].color, faces[g+1].avgZ)
            faces[g+1] = faces[g]
            faces[g] = f
            g = -1
        g+=1

    for i in range(len(faces)-1, -1, -1):   
        aPoint = projection(faces[i].a)
        bPoint = projection(faces[i].b)
        cPoint = projection(faces[i].c)
        dPoint = projection(faces[i].d)      
        py.draw.polygon(screen, faces[i].color, [[aPoint.x, aPoint.y], [bPoint.x, bPoint.y], [cPoint.x, cPoint.y], [dPoint.x, dPoint.y]])
        if(showOutline): py.draw.polygon(screen, 'black', [[aPoint.x, aPoint.y], [bPoint.x, bPoint.y], [cPoint.x, cPoint.y], [dPoint.x, dPoint.y]], 4)

    return


py.init()
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = py.time.Clock()

background = py.image.load("background.png")
background = py.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
    mouse_wheel = 0
    
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                exit()
            if event.key == py.K_1:
                showPoints = not showPoints
            if event.key == py.K_2:
                showOutline = not showOutline
            if event.key == py.K_3:
                showFaces = not showFaces
            if event.key == py.K_r:
                model.loadData()
        if event.type == py.MOUSEWHEEL:
            mouse_wheel = event.y
    
    mouse_pressed = py.mouse.get_pressed()
    mouse_rel = py.mouse.get_rel()
    
    zoomproc = int(objSize/10)
    
    py.display.set_caption('zoom: ' + str(zoomproc) + '%; camera: ' + str(int(CAMERAX)) + ', ' + str(int(CAMERAY)) + '; rotation: ' + '{:.2f}'.format(objRotationX) + ', ' + '{:.2f}'.format(objRotationY) + '; vertexes: ' + str(len(model.points)) + '; vertices: ' + str(len(model.vertices)) + '; faces: ' + str(len(model.faces)))

    screen.blit(background, (0, 0))
   
    if showOutline and not showFaces: drawVertices()
    elif showFaces: drawFaces()
    if showPoints: drawVertexes()
    
    if mouse_pressed[2]:
        objRotationX += (mouse_rel[0] / 100)
        objRotationY += (mouse_rel[1] / 100)
    if mouse_pressed[0]:
        CAMERAX += (mouse_rel[0])
        CAMERAY += (mouse_rel[1])
    
    if objSize > 0 and mouse_wheel < 0: objSize -= 10
    elif objSize < 1000 and mouse_wheel > 0: objSize += 10
    
    py.display.update() 
    clock.tick(60)