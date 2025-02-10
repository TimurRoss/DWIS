import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import time
from mathutils import Quaternion
from var import Vars

def draw_box(x:int=10,y:int=10,z:int=10):
        glColor3f(255, 0, 0)
        x1_2=x/2
        y1_2=y/2
        z1_2=z/2
        vertices = (
            (x1_2, -y1_2, -z1_2),
            (x1_2, y1_2, -z1_2),
            (-x1_2, y1_2, -z1_2),
            (-x1_2, -y1_2, -z1_2),
            (x1_2, -y1_2, z1_2),
            (x1_2, y1_2, z1_2),
            (-x1_2, y1_2, z1_2),
            (-x1_2, -y1_2, z1_2)
        )
        edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7)
        )
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
def draw_triangles():
    # Draw wings and tail fin in green
    # fill(0, 255, 0, 200);
    
    # Wing top layer
    glColor3f(0, 255, 0)
    glBegin(GL_LINE_LOOP)
    glVertex3fv((-100, 2, 30))
    glVertex3fv((0,  2, -80))
    glVertex3fv((100,  2, 30))
    glEnd()

    
    # Wing bottom layer
    glBegin(GL_LINE_LOOP)
    glVertex3fv((-100, -2, 30))
    glVertex3fv((0, -2, -80))
    glVertex3fv((100, -2, 30))
    glEnd()

    
    # Tail left layer
    glBegin(GL_LINE_LOOP)
    glVertex3fv((-2, 0, 98))
    glVertex3fv((-2, -30, 98))
    glVertex3fv((-2, 0, 70))
    glEnd()

    
    # Tail right layer
    glBegin(GL_LINE_LOOP)
    glVertex3fv(( 2, 0, 98))
    glVertex3fv(( 2, -30, 98))
    glVertex3fv(( 2, 0, 70))
    glEnd()
def draw_quads():

    glColor3f(0, 255, 0)
    glBegin(GL_LINES);
    glVertex3f(-100, 2, 30); glVertex3f(-100, -2, 30); glVertex3f(  0, -2, -80); glVertex3f(  0, 2, -80);
    glVertex3f( 100, 2, 30); glVertex3f( 100, -2, 30); glVertex3f(  0, -2, -80); glVertex3f(  0, 2, -80);
    glVertex3f(-100, 2, 30); glVertex3f(-100, -2, 30); glVertex3f(100, -2,  30); glVertex3f(100, 2,  30);

    glVertex3f(-2,   0, 98); glVertex3f(2,   0, 98); glVertex3f(2, -30, 98); glVertex3f(-2, -30, 98);
    glVertex3f(-2,   0, 98); glVertex3f(2,   0, 98); glVertex3f(2,   0, 70); glVertex3f(-2,   0, 70);
    glVertex3f(-2, -30, 98); glVertex3f(2, -30, 98); glVertex3f(2,   0, 70); glVertex3f(-2,   0, 70);

    glColor3f(0, 0, 255)
    glVertex3fv((10, 10, -100)); glVertex3fv((10, 10, -105));
    glVertex3fv((-10,  10, -100)); glVertex3fv((-10,  10, -105));
    glVertex3fv((-10,  -10, -100)); glVertex3fv((-10,  -10, -105));
    glVertex3fv((10,  -10, -100)); glVertex3fv((10,  -10, -105));
    glEnd();

def draw_front():
    # front layer
    glColor3f(0, 0, 255)
    glBegin(GL_LINE_LOOP)
    glVertex3fv((10, 10, -100))
    glVertex3fv((-10,  10, -100))
    glVertex3fv((-10,  -10, -100))
    glVertex3fv((10,  -10, -100))
    glEnd()

    
    # back layer
    glBegin(GL_LINE_LOOP)
    glVertex3fv((10, 10, -105))
    glVertex3fv((-10,  10, -105))
    glVertex3fv((-10,  -10, -105))
    glVertex3fv((10,  -10, -105))
    glEnd()
def rotate_model(vec:tuple=(1,0,0,0)):
    q=Quaternion(vec)
    axis,angle=q.to_axis_angle()
    glRotatef(angle,axis.x,axis.y,axis.z)
def draw():
    draw_box(10,10,200)
    draw_triangles()
    draw_quads()
    draw_front()
    rotate_model((1,0,1,1),)

class ImuApp:
    def __init__(self, display = (500, 500)):
        # global Var
        self.display=display
        self.functions=[]


        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('IMU симулятор')

        Vars['imuapp_is_enabled']=True
        # Var.imuapp.is_enabled=True

        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 350.0)
        glTranslatef(0.0, 0.0, -200)

    def mainloop(self):
        # global Var
        while True:
            print(Vars['imuapp_is_enabled'])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    Vars['imuapp_is_enabled']=False
                    # Var.imuapp.is_enabled = False
                    quit()
                    
            # glRotatef(1, 0, 1, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            for func,args in self.functions:
                func(*args)

            pygame.display.flip()
            pygame.time.wait(10)
    def add(self,func,args=()):
        self.functions.append((func,args))

class FrameOgl(OpenGLFrame):
    def initgl(self):
        """Initalize gl states when the frame is created"""
        glViewport(0, 0, self.width, self.height)
        glClearColor(0.0, 1.0, 0.0, 0.0)    
        self.start = time.time()
        self.nframes = 0

    def redraw(self):
        """Render a single frame"""
        glClear(GL_COLOR_BUFFER_BIT)
        draw()
        tm = time.time() - self.start
        self.nframes += 1
        print("fps",self.nframes / tm, end="\r" )

def start(Vars):
    app=ImuApp(Vars)
    app.add(draw)
    app.mainloop()

if __name__ == "__main__":
    start()