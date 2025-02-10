from OpenGL.GL import *
from OpenGL.GLU import *
from mathutils import Quaternion
from core.imuapp import ImuApp,draw
# import random as rand

def start():
    app=ImuApp()
    app.add(draw)
    app.mainloop()


if __name__ == "__main__":
    start()