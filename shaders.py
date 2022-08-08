
from mathLib import dotProduct

def fragmentShader(render, **kwargs):
    
    u, v, w = kwargs["baryCoords"]
    r, g, b = kwargs["vColor"]

    return u, v, w 


def flat(render, **kwargs):
    
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    triangleNormal = kwargs["triangleNormal"] 
    
    b /= 255
    g /= 255
    r /= 255

    negDirLight = [-render.dirLight.x, -render.dirLight.y, -render.dirLight.z]
    intensity = dotProduct(triangleNormal, negDirLight)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0


def glow(render, **kwargs):
    
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    triangleNormal = kwargs["triangleNormal"] 
    
    b /= 255
    g /= 255
    r /= 255

    negDirLight = [-render.dirLight.x, -render.dirLight.y, -render.dirLight.z]
    intensity = dotProduct(triangleNormal, negDirLight)

    yellow = (1,1,0)

    b *= intensity * 0.7
    g *= intensity * 0.7
    r *= intensity * 0.7

    b += intensity * yellow[2]
    g += intensity * yellow[1]
    r += intensity * yellow[0]

    if b > 1: b = 1
    if g > 1: g = 1
    if r > 1: r = 1

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0



def textureShader(render, **kwargs):
    
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"] 
    
    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:

        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    return r, g, b


def flatNtex(render, **kwargs):
    
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"] 
    
    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:

        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

        if texColor[2] > 0 or texColor[1] > 0 or texColor[2] > 0:
            return r, g, b
        else:
            return 0, 0, 0

    negDirLight = [-render.dirLight.x, -render.dirLight.y, -render.dirLight.z]
    intensity = dotProduct(triangleNormal, negDirLight)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0, 0, 0