
# Libreria para hacer manejo de memoria en python y poder crear 
# variables con su propio tamaño de bytes
import struct 
import random

from collections import namedtuple
from obj import Obj 
from mathLib import mm, subtractVectors, crossProduct, normV
from math import cos, sin, pi

              
# En este caso se utilizaran un word y un dword
def bValue(param, byte):
    #word -> Ocupa 2 bytes
    #dword -> Ocupa 4 bytes
    return struct.pack('=h', byte) if param == 'word' else struct.pack('=l', byte)   
    
def color(r, g, b):
    # componentes de un pixel, r(rojo), g(verde) y b(azul)
    # Se determina un rango de [0, 1] al multiplicar los componentes por 255
    # Ademas se convierte a formato de bytes
    return bytes([int(b * 255), int(g * 255), int(r * 255)])  

def baryCoords(A, B, C, P):
    
    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        #PBC / ABC
        u = areaPBC / areaABC

        #PAC / ABC
        v = areaPAC / areaABC 

        # 1 - u - v
        w = 1 - u - v

    except:
        return -1, -1, -1
    else:
        return u, v, w


V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point2', ['x', 'y', 'z'])
V4 = namedtuple('Point2', ['x', 'y', 'z', 'w'])


class Renderer(object):
    def __init__(self, width, height):
        
        self.width = width 
        self.height = height
        
        #es el color que quiero de fondo
        self.clearColor = color(0, 0, 0)
        self.currColor = color(1,1,1)

        self.active_shader = None
        self.active_texture = None

        self.dirLight = V3(0, 0, 1)
        
        self.glViewport(0, 0, self.width, self.height)
        
        self.glClear()
        
    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height
        
    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)
        
    def glColor(self, r, g, b):
        self.currColor = color(r, g, b)
        
    def glClear(self):
        # dentro de la fun clear se crear el array de pixeles
        
        # aca se guardara el array de pixeles
        self.pixels = [[ self.clearColor for y in range(self.height) ] 
                        for x in range(self.width)]

        self.zbuffer = [[ float('inf') for y in range(self.height) ] 
                        for x in range(self.width)]
        
    def glClearViewport(self, clr = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x, y, clr)
    
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor
    
    def glCreateRotationMatrix(self, pitch = 0, yaw = 0, roll = 0):
        
        pitch *= pi/180
        yaw   *= pi/180 
        roll  *= pi/180

        pMatrix = [[1, 0, 0, 0],
                   [0, cos(pitch), -sin(pitch), 0],
                   [0, sin(pitch), cos(pitch), 0],
                   [0, 0, 0, 1]]

        yMatrix = [[cos(yaw), 0, sin(yaw), 0],
                   [0, 1, 0, 0],
                   [-sin(yaw), 0, cos(yaw), 0],
                   [0, 0, 0, 1]]

        rMatrix = [[cos(roll), -sin(roll), 0, 0],
                   [sin(roll), cos(roll), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]]

        return mm(mm(pMatrix, yMatrix), rMatrix)
        
            
    def glPoint_vp(self, ndcX,  ndcY, clr = None):
        x = (ndcX + 1) * (self.vpWidth / 2) + self.vpX
        y = (ndcY + 1) * (self.vpHeight / 2) + self.vpY
        
        x = int(x)
        y = int(y)
        
        self.glPoint(x,y, clr)
        

    def glCreateObjectMatrix(self, translate = V3(0, 0, 0), rotate = V3(0, 0, 0), scale = V3(1, 1, 1)):

        tMatrix = [[1, 0, 0, translate.x],
                   [0, 1, 0, translate.y],
                   [0, 0, 1, translate.z],
                   [0, 0, 0, 1]]

        rMatrix = self.glCreateRotationMatrix(rotate.x, rotate.y, rotate.z)

        sMatrix = [[scale.x, 0, 0, 0],
                   [0, scale.y, 0, 0],
                   [0, 0, scale.z, 0],
                   [0, 0, 0, 1]]

        return mm(mm(tMatrix, rMatrix), sMatrix)
        

    def glTransform(self, vertex, matrix):

        v = V4(vertex[0], vertex[1], vertex[2], 1)
        v = [[v.x], [v.y], [v.z], [v.w]]

        vt = mm(matrix, v)
        vf = V3(vt[0][0] / vt[3][0], 
                vt[1][0] /vt[3][0], 
                vt[2][0] /vt[3][0])

        return vf
        

    def glLoadModel(self, filename, translate = V3(0, 0, 0), rotate = V3(0, 0, 0), scale = V3(1, 1, 1)):
        model = Obj(filename)
        modelMatrix = self.glCreateObjectMatrix(translate, rotate, scale)

        for face in model.faces:
            vertCount = len(face)

            v0 = model.vertices[face[0][0] - 1 ]
            v1 = model.vertices[face[1][0] - 1 ]
            v2 = model.vertices[face[2][0] - 1 ]

            v0 = self.glTransform(v0, modelMatrix)
            v1 = self.glTransform(v1, modelMatrix)
            v2 = self.glTransform(v2, modelMatrix)

            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]

            self.glTriangle_bc(v0, v1, v2, texCoords = (vt0, vt1, vt2))

            if vertCount == 4:
                v3 = model.vertices[face[3][0] - 1]
                v3 = self.glTransform(v3, modelMatrix)
                vt3 = model.texcoords[face[3][1] - 1]
                self.glTriangle_bc(v0, v2, v3, texCoords = (vt0, vt2, vt3))


    def glTriangle_std(self, A, B, C, clr = None):
        
        if A.y < B.y: # Si A esta abajo de B
             A, B = B, A

        if A.y < C.y: # Si A esta abajo de C
             A, C = C, A  

        if B.y < C.y: # Si B esta abajo de C
             B, C = C, B

        self.glLine(A, B, clr)
        self.glLine(B, C, clr)
        self.glLine(C, A, clr)

        def flatBottom(vA, vB, vC):

            try:
                mBA = (vB.x - vA.x) / (vB.y - vA.y)
                mCA = (vC.x - vA.x) / (vC.y - vA.y)

            except:
                pass
             
            else:
                x0 = vB.x 
                x1 = vC.x

                for y in range(int(vB.y), int(vA.y)):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 += mBA
                    x1 += mCA

        def flatTop(vA, vB, vC):
            try:
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
                mCB = (vC.x - vB.x) / (vC.y - vB.y)
            except:
                pass
            else:
                x0 = vA.x
                x1 = vB.x

                for y in range(int(vA.y), int(vC.y), -1):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 -= mCA
                    x1 -= mCB

        if B.y == C.y:
            # Parte plana abajo
            flatBottom(A, B, C) 

        elif A.y == B.y:
            # Parte plana arriba
            flatTop(A, B, C)

        else:
            # Dibujo ambos tipos de triangulos
            # Teorema de intercepto

            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottom(A, B, D)
            flatTop(B, D, C)


        
    def glLine(self, v0, v1, clr = None):
        # Bresenham line algorithm
        # y = m * x + b
        
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)
        
        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0, clr)
            return
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        steep = dy > dx
        
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        # si se dibuja de derecha a izquierda que se dibuje al reves
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0
        
        
        for x in range(x0, x1 + 1):
            if steep:
                newY = x
                newX = y
                self.glPoint(y, x, clr)
                
            else:
                self.glPoint(x, y, clr)
                            
            offset += m
            
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                    
                limit += 1
    
    def glTriangle_bc(self, A, B, C, texCoords = (), clr = None):
                
        # bounding box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        subBA = subtractVectors(B, A)
        subCA = subtractVectors(C, A)

        #||AB X AC|| 
        # Producto Cruz normalizado
        triangleNormal = normV(crossProduct(subBA, subCA))
        

        for x in range(minX, maxX +1):
            for y in range(minY, maxY +1):
                u, v, w = baryCoords(A, B, C, V2(x,y))

                if 0<=u and 0<=v and 0<=w:

                    # P = Au + Bv + Cw
                    z = A.z * u + B.z * v + C.z * w

                    if z < self.zbuffer[x][y]:
                        self.zbuffer[x][y] = z   

                        if self.active_shader:
                            r, g, b = self.active_shader(self, 
                                                         baryCoords=(u,v,w), 
                                                         vColor = clr or self.currColor,
                                                         texCoords = texCoords,
                                                         triangleNormal = triangleNormal)
                            self.glPoint(x, y, color(r, g, b))

                        else:
                            self.glPoint(x, y, clr)


    # Funcion para crear la imagen, funcion para tener el bitmap - framebuffer 
    def glFinish(self, filename):
        # wb - tipo de escritura en bytes
        with open(filename, "wb") as file:
            
            #Formato de archivo bitmap
            
            #Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            
            # Tamano del archivo
            # 14 bytes de header + 40 bytes de offset = 54 bytes y el resto es
            # informacion del color
            file.write(bValue('dword', 54 + (self.width * self.width * 3)))
            
            file.write(bValue('dword', 0))
            # 14 bytes de header + 40 bytes de offset
            file.write(bValue('dword', 54))
            
            #InfoHeader
            
            #Tamano de infoHeader = 40 bytes 
            file.write(bValue('dword', 40))
            
            #Ancho y alto
            file.write(bValue('dword', self.width))
            file.write(bValue('dword', self.height))
            
            file.write(bValue('word', 1))
            #Bits per pixel - Cuanta memoria se ocupa por cada pixel(r, g y b)
            file.write(bValue('word', 24))
            file.write(bValue('dword', 0))
            #Tamano de la imagen 
            file.write(bValue('dword', self.width * self.height * 3))
            file.write(bValue('dword', 0))
            file.write(bValue('dword', 0))
            file.write(bValue('dword', 0))
            file.write(bValue('dword', 0))
            
            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])