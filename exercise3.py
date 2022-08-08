
from library import Renderer, color, V2, V3
from shaders import fragmentShader, flat, glow, textureShader, flatNtex
from texture import Texture
import random

width = 100
height = 100

rend = Renderer(width, height)

rend.active_shader = flatNtex

rend.active_texture = Texture("./models/modelTexture.bmp")


rend.glLoadModel("./models/cola_can.obj", 
                 translate= V3(width/2, height/2, 0), 
                 rotate = V3(0, 0, 0),
                 scale= V3(4.5, 4.5, 4.5))

rend.glFinish("outputs/pirate_coin.bmp")

