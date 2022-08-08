# Libreria personal matematica

def mm(m1, m2):
        l_M1 = len(m1)
        l_M1_in, l_M2_in = len(m1[0]), len(m2[0])
        matrixR = []

        for rM1 in range(l_M1):
            new = []
            for cM2 in range(l_M2_in):
                new.append(sum(m1[rM1][rM2] * m2[rM2][cM2] for rM2 in range(l_M1_in)))
            matrixR = matrixR + [new]

        return matrixR

def subtractVectors(v1, v2):
    v1x, v1y, v1z = v1.x, v1.y, v1.z
    v2x, v2y, v2z = v2.x, v2.y, v2.z

    return [(v2x - v1x), (v2y - v1y), (v2z - v1z)]

def crossProduct(v1, v2):
    v1x, v1y, v1z = v1[0], v1[1], v1[2]
    v2x, v2y, v2z = v2[0], v2[1], v2[2]

    x = (v1y * v2z) - (v2y * v1z)
    y = (v2x * v1z) - (v1x * v2z)
    z = (v1x * v2y) - (v2x * v1y)

    return [x, y, z]

def normV(v):
    x, y, z = v[0], v[1], v[2]
    xSquared = (x)**2
    ySquared = (y)**2
    zSquared = (z)**2
    norm = (xSquared + ySquared + zSquared)**0.5

    return  [(x/norm), (y/norm), (z/norm)] 

def dotProduct(v1, v2):
    v1x, v1y, v1z = v1[0], v1[1], v1[2]
    v2x, v2y, v2z = v2[0], v2[1], v2[2]

    return (v1x * v2x) + (v1y * v2y) + (v1z * v2z)

