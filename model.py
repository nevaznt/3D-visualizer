from point import Point3D
from point import Vertice
from point import Face

class Model:
    def __init__(self, file):
        self.points = []
        self.vertices = []
        self.faces = []
        self.file = file
        self.loadData()
        
    def loadData(self):
        file = open(self.file, 'r')
        datastring = file.readlines()
        
        self.points = []
        self.vertices = []
        self.faces = []
        
        now_reading = 'vertex'
        for line in datastring:
            line = line.replace('\n', '')
            if line.__contains__('//'): line = line.split('//')[0]
            if line == '': continue
            if line.__contains__('vertex'): 
                now_reading = 'vertex'
                continue
            elif line.__contains__('vertice'):
                now_reading = 'vertice'
                continue
            elif line.__contains__('face'):
                now_reading = 'face'
                continue
            lineslited = line.split(' ')
            if now_reading == 'vertex' and len(lineslited) == 3: self.points.append(Point3D(float(lineslited[0]), float(lineslited[1]), float(lineslited[2])))
            elif now_reading == 'vertice' and len(lineslited) == 2: self.vertices.append(Vertice(int(lineslited[0]), int(lineslited[1])))
            elif now_reading == 'face' and len(lineslited) == 4: self.faces.append(Face(int(lineslited[0]), int(lineslited[1]), int(lineslited[2]), int(lineslited[3]), '#4f4f4f'))
            elif now_reading == 'face' and len(lineslited) == 5: self.faces.append(Face(int(lineslited[0]), int(lineslited[1]), int(lineslited[2]), int(lineslited[3]), lineslited[4]))
        
        file.close()
        return