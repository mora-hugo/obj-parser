#!/usr/bin/env python3

import sys
import time
import math

from numpy import array

import libs.camera as _cam

try:
    from OpenGL.GL      import *
    from OpenGL.GLU     import *
    from OpenGL.GLUT    import *
except:
    print ('''ERROR: PyOpenGL not installed properly.''')

################################################################################
# GLOBAL VARS

camera          = _cam.camera([300, 300, 300], [0, 0, 0])#main camera
mouse           = [0, 0]                            #mouse current position
ancien_mouse           = [0, 0]

################################################################################
# SETUPS

def stopApplication():
    sys.exit(0)


def setupScene(model_file_name):
    '''OpenGL and Scene objects settings
    '''
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0., 200., 0., 1.))    
    glLightfv(GL_LIGHT0, GL_AMBIENT,(.1, .1, .1, 1.))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,(.7, .7, .7, 1.))
    
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    
    glColorMaterial(GL_FRONT,GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(.4, .4, .4, 1)
    
    global model
    model = read_model(model_file_name)


    
def rotation(p,u,a):
    x = u[0]
    y = u[1]
    z = u[2]
    c = math.cos(a)
    s = math.sin(a)
    matrice = [
        [x**2*(1-c)+c, x*y*(1-c)-z*s, x*z*(1-c)+y*s],
        [x*y*(1-c)+z*s, y**2*(1-c)+c, y*z*(1-c)-x*s],
        [x*z*(1-c)-y*s, y*z*(1-c)+x*s,z**2*(1-c)+c]
    ]
    return matriceFoisPoints(matrice,p)

def read_model(file_path):
    vertexs = []
    faces = []
    normales = []
    with open('/users/info/etu-s4/morahu/M4105C2/tp2/tp2/'+file_path,'r') as openfileobject:
        for line in openfileobject:
            tempLine = line.split(" ")
            if tempLine[0] == "v":
                if tempLine[1] == "":
                    tempLine.pop(1)
                vertexs.append([float(tempLine[1]),float(tempLine[2]),float(tempLine[3])])
            elif tempLine[0] == "vt":
                pass
            elif tempLine[0] == "f":
                temp = []
                for things in (tempLine[1],tempLine[2],tempLine[3]):
                    tempThings = things.split("/")
                    temp.append(tempThings[0])
                    
                    
                faces.append([int(temp[0]),int(temp[1]),int(temp[2])])

            else: 
                print("pas trouve")
        
        for calc1 in faces:
            a = vertexs[calc1[0]-1]
            b = vertexs[calc1[1]-1]
            c = vertexs[calc1[2]-1]
            vectorA = vector(a,b)
            vectorB = vector(a,c)
            calc = cross(vectorA,vectorB)
            normales.append(normalize(calc))
            

    return vertexs, faces, normales


################################################################################
# COMPUTATIONS

def cross(vectorA, vectorB):
    return [
            vectorA[1]*vectorB[2]-vectorA[2]*vectorB[1],
            vectorA[2]*vectorB[0]-vectorA[0]*vectorB[2],
            vectorA[0]*vectorB[1]-vectorA[1]*vectorB[0]
            ]


def vector(a, b):
    return [
        b[0] - a[0],
        b[1] - a[1],
        b[2] - a[2]
    ]

def norm(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])


def normalize(v):
    n = norm(v)
    return [v[0]/n, v[1]/n, v[2]/n]
   

def matriceFoisPoints(m,p):
    return [
        m[0][0]*p[0]+m[0][1]*p[1]+m[0][2]*p[2],
        m[1][0]*p[0]+m[1][1]*p[1]+m[1][2]*p[2],
        m[2][0]*p[0]+m[2][1]*p[1]+m[2][2]*p[2]
    ]
################################################################################
# DISPLAY FUNCS

def display_scene():
    '''display of the whole scene, mainly the spheres (in white)
    '''
    
    #Display a frame
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor(1,0,0,1)
    glVertex(0, 0, 0)
    glVertex(1000, 0, 0)
    glColor(0,1,0,1)
    glVertex(0, 0, 0)
    glVertex(0, 1000, 0)
    glColor(0,0,1,1)
    glVertex(0, 0, 0)
    glVertex(0, 0, 1000)
    glEnd()
    glEnable(GL_LIGHTING)
    
    #display the model
    glBegin(GL_TRIANGLES)
    i = 0
    for face in model[1]:
        # for face in mod:
        #     glNormal(model[2][face-1][0],model[0][face-1][1],model[2][face-1][2])
        #     glVertex(model[0][face-1][0],model[0][face-1][1],model[0][face-1][2])
        glNormal(*model[2][i])
        glVertex(*model[0][face[0]-1])
        glVertex(*model[0][face[1]-1])
        glVertex(*model[0][face[2]-1])
        i += 1
    glEnd()

def display():
    '''Global Display function
    '''
    
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity ()             # clear the matrix 
    
    ###############
    #Point of View
    gluLookAt ( camera.position[0], camera.position[1], camera.position[2], 
                camera.viewpoint[0], camera.viewpoint[1], camera.viewpoint[2], 
                camera.up[0], camera.up[1], camera.up[2])
    
    ###############
    #Frame
    display_scene()
    
    glutSwapBuffers()


def reshape (w, h):
    '''Perspective matrix for the projection
        Called by windows rescaling events
    '''
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective(60.0,float(w)/float(h),.1,1000.0)
    glMatrixMode (GL_MODELVIEW)


################################################################################
## INTERACTION FUNCS

def keyboard(key, x, y):
    '''Called when a keyboard ascii key is pressed
    '''
    if key == b'\x1b':
        stopApplication()
    elif key == b'f':
        glutFullScreen()
    else:
        print ("key", key)


def mouse_clicks(button, state, x, y):
    '''Called when a mouse's button is pressed or released.
    - button is in [GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON],
    - state is in [GLUT_DOWN, GLUT_UP]
    '''
    global mouse
    mouse = [x, y]
    glutPostRedisplay()
    
    


def mouse_active(x, y):
    '''Called when mouse moves while one button is pressed
    '''
    global mouse
    global ancien_mouse
    mouse = [x, y]
    print("--------\n")
    print(camera.position)
    
    camera.position = rotation(camera.position,[0,1,0],-(mouse[0]-ancien_mouse[0])/400)
    camera.position = rotation(camera.position,[0,0,1],-(mouse[1]-ancien_mouse[1])/400)

    ancien_mouse = mouse
    print(camera.position)
    print("\n------------")
    glutPostRedisplay()
    
    
    

def mouse_passive(x, y):
    '''Called when mouse hovers the window
    '''
    global mouse
    mouse =[x, y]
    glutPostRedisplay()


################################################################################
# MAIN

print("Commands:")
print("\tf:\tfullscreen")
print("\tesc:\texit")

glutInit(sys.argv)
glutInitDisplayString(b'double rgba depth')
glutInitWindowSize (800, 600)
glutInitWindowPosition (0, 0)
glutCreateWindow(b'ArcBall')

setupScene("models/Jotaro.obj")

glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_clicks)
glutMotionFunc(mouse_active)
glutPassiveMotionFunc(mouse_passive)
glutMainLoop()
