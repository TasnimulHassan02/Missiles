from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width = 1000
height = 700
plane_x, plane_y = 600, 500
plane_angle = 0
plane_speed = 0.3
score = 0
star_x = random.sample(range(50, width-50), 50)
star_y = random.sample(range(50, height-50), 50)
star = [[star_x[35], star_y[35]]]
missile_x = random.sample(range(10, width), 50)
missile_y = random.sample(range(height, height+50), 50)
missile = [[missile_x[35], missile_y[35]]]
missile_speed = 0.2
missile_angle = 0
red_missile = [[300, 900], [700, 1000], [-10, 800]]
red_speed = 0.3
power1_x = random.choice(star_x)
power1_y = random.choice(star_y)
power2_x = random.choice(star_x)
power2_y = random.choice(star_y)
shieldMode = False
boostMode = False
obstacles = [[random.choice(star_x),random.choice(star_y)]]
is_paused = False


################################  DRAWING   ##########################

def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        if dy > 0:
            return 1
        else:
            return 5
    elif dy == 0:
        if dx > 0:
            return 0
        else:
            return 4
    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx > 0 and dy < 0:
            return 7
    else:
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx > 0 and dy < 0:
            return 6

def ConvertMtoZero(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def ConvertZeroToM(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def MidpointLine(x1, y1, x2, y2, zone):
    dx = x2 - x1
    dy = y2 - y1
    E  = 2 * dy
    NE = 2 * (dy - dx)
    d = 2 * dy - dx
    x = x1
    y = y1
    cx, cy = ConvertZeroToM(x, y, zone)
    draw_points(cx, cy)
    while (x <= x2):
        if d <= 0:
            d = d + E
            x = x + 1
        else:
            d = d + NE
            x = x + 1
            y = y + 1
        cx, cy = ConvertZeroToM(x, y, zone)
        draw_points(cx, cy)

def MidpointLineEightway(x1, y1, x2, y2):
    zone = FindZone(x1, y1, x2, y2)
    x1, y1 = ConvertMtoZero(x1, y1, zone)
    x2, y2 = ConvertMtoZero(x2, y2, zone)
    MidpointLine(x1, y1, x2, y2, zone)

def CirclePoints(x, y, cx, cy):
    draw_points( x + cx,  y + cy)
    draw_points( y + cx,  x + cy)
    draw_points( y + cx, -x + cy)
    draw_points( x + cx, -y + cy)
    draw_points( -x + cx, -y + cy)
    draw_points( -y + cx, -x + cy)
    draw_points( -y + cx,  x + cy)
    draw_points( -x + cx,  y + cy)

def MidpointCircle(radius, cx, cy):
    d = 1 - radius
    x = 0
    y = radius
    CirclePoints(x, y, cx, cy)
    while x < y:
        if d < 0:
            d = d + 2*x + 3
            x = x + 1
        else:
            d = d + 2*x - 2*y + 5
            x = x + 1
            y = y - 1
        CirclePoints(x, y, cx, cy)
        
def star_draw(x, y):
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(8)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()
        
    glColor3f(1, 1, 1)
    MidpointLineEightway(x, y+10, x-4, y+3)
    MidpointLineEightway(x-4, y+3, x-10, y+3)
    MidpointLineEightway(x-10, y+3, x-5, y-2)
    MidpointLineEightway(x-5, y-2, x-7, y-10)
    MidpointLineEightway(x-7, y-10, x, y-5)
    MidpointLineEightway(x, y-5, x+7, y-10)
    MidpointLineEightway(x+7, y-10, x+5, y-2)
    MidpointLineEightway(x+5, y-2, x+10, y+3)
    MidpointLineEightway(x+10, y+3, x+4, y+3)
    MidpointLineEightway(x+4, y+3, x, y+10)    
        

def shield_draw(x, y):
    glColor3f(0.11, 0.35, 1)
    MidpointCircle(14, x, y-5)
    glColor3f(0.3, 0.09, 0.02)
    MidpointLineEightway(x-7, y, x+7, y)
    MidpointLineEightway(x-7, y, x-7, y-7)
    MidpointLineEightway(x+7, y, x+7, y-7)
    MidpointLineEightway(x-7, y-7, x, y-15)
    MidpointLineEightway(x+7, y-7, x, y-15)       
        
def obstacle_draw(x, y):
    glColor3f(0.5, 0.1, 0.05)
    glPointSize(50)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()     
    
def thrust_draw(x, y):
    glColor3f(1, 1, 1)
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(220, 0, 0, 1)
    glTranslatef(-x, -y, 0)
    for i in range(-2,2):
        MidpointLineEightway(x+i, y, x+i, y+6)
    for i in range(-2,2):
        glColor3f(0.9, 0.9, 0.9)
        MidpointLineEightway(x+i, y-12, x+i, y-6)
    for i in range(-2,2):
        glColor3f(0.8, 0.8, 0.8)
        MidpointLineEightway(x+i, y-24, x+i, y-18)
    glPopMatrix()

        
def airplane_draw(x, y):
    x = int(x)
    y = int(y)
    global plane_angle
    
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(plane_angle, 0, 0, 1)
    glTranslatef(-x, -y, 0)
    
    glColor3f(0, 0, 0)
    MidpointLineEightway(x, y, x+9, y)
    MidpointLineEightway(x+9, y, x+9, y+2)
    MidpointLineEightway(x+9, y+2, x+1, y)  # pakha
    MidpointLineEightway(x-9, y, x, y)
    MidpointLineEightway(x-9, y, x-9, y+2)
    MidpointLineEightway(x-9, y+2, x-1, y)

    glColor3f(1, 0, 0)
    MidpointLineEightway(x, y, x-8, y-10)     # Front
    MidpointLineEightway(x, y, x+8, y-10)
    MidpointLineEightway(x-8, y-10, x+8, y-10)
    for j in range(y-10, y):
        for i in range(x-8 + (j-(y-10)), x+9 - (j-(y-10))):
            draw_points(i, j)

    MidpointLineEightway(x-8, y-10, x-1, y-60)     # Body
    MidpointLineEightway(x+8, y-10, x+1, y-60)
    MidpointLineEightway(x-8, y-10, x+8, y-10)


    MidpointLineEightway(x+6, y-20, x+20, y-25)
    MidpointLineEightway(x+20, y-30, x+6, y-28)
    MidpointLineEightway(x+20, y-25, x+20, y-30)
    MidpointLineEightway(x+6, y-20, x+7, y-25)
                                                   # main fin
    MidpointLineEightway(x-20, y-25, x-20, y-30)
    MidpointLineEightway(x-6, y-20, x-20, y-25)
    MidpointLineEightway(x-20, y-30, x-6, y-28)
    MidpointLineEightway(x-6, y-20, x-7, y-25)

    MidpointLineEightway(x-2, y-52, x-12, y-57)
    MidpointLineEightway(x+2, y-52, x+12, y-57)
    MidpointLineEightway(x-12, y-57, x-12, y-61)
    MidpointLineEightway(x+12, y-57, x+12, y-61)      # Backside fins
    MidpointLineEightway(x-12, y-61, x-1, y-60)
    MidpointLineEightway(x+12, y-61, x+1, y-60)

    glPopMatrix()
        
def missile_draw(x, y):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(missile_angle, 0, 0, 1)
    glTranslatef(-x, -y, 0)
    
    x = int(x)
    y = int(y)
    glColor3f(1, 1, 0.4)
    MidpointLineEightway(x-4, y, x+4, y)
    MidpointLineEightway(x-4, y-30, x+4, y-30)
    MidpointLineEightway(x-4, y, x-4, y-30)
    MidpointLineEightway(x+4, y-1, x+4, y-30)
    for j in range(y-30, y+1):
        for i in range(x-4, x+5):
            draw_points(i, j)

    glColor3f(0.3, 0.3, 0.3)
    MidpointLineEightway(x-4, y, x-1, y+4)
    MidpointLineEightway(x+4, y, x+1, y+4)
    MidpointLineEightway(x-4, y, x+3, y)
    for j in range(y+1, y+4):
        for i in range(x-4+(j-y), x+5-(j-y)):
            draw_points(i, j)

    MidpointLineEightway(x-4, y-18, x-8, y-21)
    MidpointLineEightway(x-4, y-18, x-4, y-30)
    MidpointLineEightway(x-8, y-21, x-8, y-33)
    MidpointLineEightway(x-8, y-33, x-4, y-30)
    for j in range(y-30, y-19):
        for i in range(x-8, x-3):
            draw_points(i, j)

    MidpointLineEightway(x+4, y-18, x+8, y-21)
    MidpointLineEightway(x+4, y-18, x+4, y-30)
    MidpointLineEightway(x+8, y-21, x+8, y-33)
    MidpointLineEightway(x+8, y-33, x+4, y-30)
    for j in range(y-30, y-19):
        for i in range(x+4, x+9):
            draw_points(i, j)
    glPopMatrix()

def shieldMode_draw(x, y):
    global plane_angle
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(plane_angle, 0, 0, 1)
    glTranslatef(-x, -y, 0)
    glColor3f(0.95, 0.33, 0.10)
    MidpointCircle(38, x, y-30)
    glPopMatrix()
 
def boost_draw(x, y):
    glColor3f(0.12, 0, 0.7)
    MidpointCircle(13, x, y)
    glColor3f(0, 1, 0)
    MidpointLineEightway(x-6, y, x-1, y+6)
    MidpointLineEightway(x+6, y, x, y+6)
    MidpointLineEightway(x-6, y, x+6, y)
    for j in range(y+1, y+6):
        for i in range(x-6+(j-y), x+7-(j-y)):
            draw_points(i, j)
    MidpointLineEightway(x-4, y, x-4, y-6)
    MidpointLineEightway(x, y, x, y-6)
    MidpointLineEightway(x+4, y, x+4, y-6) 
 
 
# def cloud_draw(x, y):
#     glColor3f(0.75, 0.8, 0.8)
#     for i in range(0, 51):
#         MidpointCircle(i, x, y)
#     for i in range(0, 46):
#         MidpointCircle(i, x+40, y+20)
#     for i in range(0, 41):
#         MidpointCircle(i, x, y+40)
#     for i in range(0, 36):
#         MidpointCircle(i, x-60, y)
#     for i in range(0, 36):
#         MidpointCircle(i, x+60, y-5)           
    
# def collision_draw(x,y):
#     #1st blast
#     glColor3f(1, 0, 0)
#     for i in range(0, 15):
#         MidpointCircle(i, x, y)
#     glColor3f(1, 1, 1)
#     for i in range(0, 30):
#         MidpointCircle(i, x, y)
#     #2nd blast
#     glColor3f(1, 0, 0)
#     for j in range(0, 17):
#         MidpointCircle(j, x+11, y+12)
#     glColor3f(1, 1, 1)
#     for i in range(0, 25):
#         MidpointCircle(i, x, y)
#     #3rd blast
#     glColor3f(1, 0, 0)
#     for k in range(0, 19):
#         MidpointCircle(k, x+14, y-13)
#     glColor3f(1, 1, 1)
#     for i in range(0, 29):
#         MidpointCircle(i, x, y)
#     #4th blast
#     glColor3f(1, 0, 0)
#     for l in range(0, 21):
#         MidpointCircle(l, x+25, y-5)
#     glColor3f(1, 1, 1)
#     for i in range(0, 38):
#         MidpointCircle(i, x, y)
        
# def life_count_draw(X,Y):
#     x= X+45
#     y= Y+5
#     glColor3f(0.6, 0.2, 0.8)
#     for i in range(-10, 11):
#         for j in range(-10, 11):
#             if abs(i) + abs(j) <= 12:
#                 draw_points(x + i, y + j)
 

################################  ANIMATION   ##########################       


def animation():
    flying_plane()
    missile_attack()
    red_incoming()


def flying_plane():
    global plane_x, plane_y, plane_angle, plane_speed
    plane_y += plane_speed
    dx = 0
    dy = 0
    
    if plane_angle == 0:
        dx = 0
        dy = 0.2
    if plane_angle == -45:
        dx = 0.3
        dy = 0.0
    if plane_angle == -90:
        dx = 0.4
        dy = -0.3
    if plane_angle == -135:
        dx = 0.2
        dy = -0.6
    if plane_angle == -180:
        dx = 0
        dy = -0.7
    if plane_angle == -225:
        dx = -0.2
        dy = -0.6
    if plane_angle == -270:
        dx = -0.4
        dy = -0.3
    if plane_angle == -315:
        dx = -0.3
        dy = 0
    if plane_angle == -360:
        dx = 0
        dy = 0.3

    if plane_angle == 45:
        dx = -0.3
        dy = 0.2
    if plane_angle == 90:
        dx = -0.4
        dy = -0.3
    if plane_angle == 135:
        dx = -0.2
        dy = -0.6
    if plane_angle == 180:
        dx = 0
        dy = -0.7
    if plane_angle == 225:
        dx = 0.2
        dy = -0.6
    if plane_angle == 270:
        dx = 0.3
        dy = -0.3
    if plane_angle == 315:
        dx = 0.3
        dy = 0.1
    if plane_angle == 360:
        dx = 0
        dy = 0.3
        
    plane_x += dx
    plane_y += dy

    glutPostRedisplay()

def random_star():
    global star, star_x, star_y
    x = random.randint(400,800)
    star.append([x,x])
    for i in range(len(star_x)):
        star.append([star_x[i], star_y[i]])
    
    star_draw(star[0][0], star[0][1])

def collision_detect(plane_x, plane_y, obstacle_x, obstacle_y, threshold=20):
    global score, power1_x, power1_y, shieldMode, obstacles, power2_x, power2_y, red_missile, plane_speed, boostMode
    distance = ((plane_x - obstacle_x) ** 2 + (plane_y - obstacle_y) ** 2) ** 0.5
    if (distance < threshold):
        print('Star Collected')
        score += 1
        star.pop(0)
        print('Score', score)

    distance = ((plane_x - missile[0][0]) ** 2 + (plane_y - missile[0][1]) ** 2) ** 0.5
    if (distance < threshold+5):
        if shieldMode:
            return
        print('Missile Hit')
        print("Goodbye!\nFinal Score:", score)
        glutLeaveMainLoop()
    
    distance = ((plane_x - red_missile[0][0]) ** 2 + (plane_y - red_missile[0][1]) ** 2) ** 0.5
    if (distance < threshold):
        if shieldMode:
            return
        print('IronDome Missile Hit')
        print("Goodbye!\nFinal Score:", score)
        glutLeaveMainLoop()

    distance = ((plane_x - power1_x) ** 2 + (plane_y - power1_y) ** 2) ** 0.5
    if (distance < threshold):
        print('Shield Collected')
        power1_x = -33
        power1_y = -33
        shieldMode = True
    if (score%4) == 0:
        if score != 0:
            shieldMode = False
    
    distance = ((plane_x - power2_x) ** 2 + (plane_y - power2_y) ** 2) ** 0.5
    if (distance < threshold):
        print('Boost Collected')
        power2_x = -33
        power2_y = -33
        boostMode = True
    if (score%4) == 0:
        if score != 0:
            boostMode = False
    
    distance = ((plane_x - obstacles[0][0]) ** 2 + (plane_y - obstacles[0][1]) ** 2) ** 0.5
    if (distance < threshold):
        print('Shield Collected')
        obstacles.pop()
        print('Crashed into obstacle')
        print("Goodbye!\nFinal Score:", score)
        glutLeaveMainLoop()
        

def missile_attack():
    global missile, plane_x, plane_y, missile_speed, missile_angle
    if missile[0][0] < plane_x and missile[0][1] < plane_y:
        missile[0][0] += missile_speed
        missile[0][1] += missile_speed
        missile_angle = -45

    if missile[0][0] > plane_x and missile[0][1] < plane_y:
        missile[0][0] -= missile_speed
        missile[0][1] += missile_speed
        missile_angle = 45

    if missile[0][0] > plane_x and missile[0][1] > plane_y:
        missile[0][0] -= missile_speed
        missile[0][1] -= missile_speed
        missile_angle = 135

    if missile[0][0] < plane_x and missile[0][1] > plane_y:
        missile[0][0] += missile_speed
        missile[0][1] -= missile_speed
        missile_angle = -135
    
    glutPostRedisplay()


def incoming_missile():
    global missile, score
    missile_draw(missile[0][0], missile[0][1])
    

def special_missile(x, y):
    x = int(x)
    y = int(y)
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(220, 0, 0, 1)
    glTranslatef(-x, -y, 0)
    glColor3f(1, 0, 0)
    MidpointLineEightway(x-4, y, x+4, y)
    MidpointLineEightway(x-4, y-30, x+4, y-30)
    MidpointLineEightway(x-4, y, x-4, y-30)
    MidpointLineEightway(x+4, y-1, x+4, y-30)
    for j in range(y-30, y+1):
        for i in range(x-4, x+5):
            draw_points(i, j)

    glColor3f(0.3, 0.3, 0.3)
    MidpointLineEightway(x-4, y, x-1, y+4)
    MidpointLineEightway(x+4, y, x+1, y+4)
    MidpointLineEightway(x-4, y, x+3, y)
    for j in range(y+1, y+4):
        for i in range(x-4+(j-y), x+5-(j-y)):
            draw_points(i, j)

    MidpointLineEightway(x-4, y-18, x-8, y-21)
    MidpointLineEightway(x-4, y-18, x-4, y-30)
    MidpointLineEightway(x-8, y-21, x-8, y-33)
    MidpointLineEightway(x-8, y-33, x-4, y-30)
    for j in range(y-30, y-19):
        for i in range(x-8, x-3):
            draw_points(i, j)

    MidpointLineEightway(x+4, y-18, x+8, y-21)
    MidpointLineEightway(x+4, y-18, x+4, y-30)
    MidpointLineEightway(x+8, y-21, x+8, y-33)
    MidpointLineEightway(x+8, y-33, x+4, y-30)
    for j in range(y-30, y-19):
        for i in range(x+4, x+9):
            draw_points(i, j)
    glPopMatrix()


def red_incoming():
    global red_missile
    for i in range(len(red_missile)):
        red_missile[i][0] += red_speed
        red_missile[i][1] -= red_speed
    glutPostRedisplay()


def red_attack():
    global red_missile, score
    for i in range(len(red_missile)):
        special_missile(red_missile[i][0], red_missile[i][1])
        thrust_draw(red_missile[i][0]-28, red_missile[i][1]+30)
    

def boundary_check():
    global plane_x, plane_y, height, width
    if plane_x < 0 or plane_x > width:
        print("Goodbye!\nFinal Score:", score)
        glutLeaveMainLoop()
    if plane_y < 0 or plane_y > height:
        print("Goodbye!\nFinal Score:", score)
        glutLeaveMainLoop()
    
    
def powerups():
    global score, power1_x, power1_y, plane_x, plane_y, power2_x, power2_y, plane_speed, boostMode
    if (score%3) == 0:
        if score != 0:
            shield_draw(power1_x, power1_y)
    if shieldMode:
        shieldMode_draw(plane_x, plane_y)

    if (score%2) == 0:
        if score != 0:
            boost_draw(power2_x, power2_y)
    if boostMode:
        plane_speed += 0.00002
        

def control():
    glColor3f(0, 0, 0)
    MidpointLineEightway(20, 680, 55, 680)
    MidpointLineEightway(40, 690, 55, 680)
    MidpointLineEightway(40, 670, 55, 680)
    glColor3f(0, 1, 0)
    MidpointLineEightway(500, 670, 500, 690)
    MidpointLineEightway(520, 670, 520, 690)
    glColor3f(1.0, 0, 0)
    MidpointLineEightway(960, 670, 980, 690)
    MidpointLineEightway(980, 670, 960, 690)


def obstacle():
    global obstacles, star_x, star_y, score
    star_x = random.sample(range(50, width-50), 50)
    star_y = random.sample(range(50, height-50), 50)
    for i in range(len(star_x)):
        obstacles.append([star_x[i], star_y[i]])
    if score > 0:
        obstacle_draw(obstacles[0][0], obstacles[0][1])    
    
    
def iterate():
    glViewport(0, 0, 1000, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 700, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    if not is_paused:
        global star_x, star_y, star, score, power1_x, power1_y
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        iterate()
        collision_detect(plane_x, plane_y, star[0][0], star[0][1])
        powerups()
        boundary_check()
        control()
        obstacle()
        red_attack()
        random_star()
        airplane_draw(plane_x, plane_y)
        incoming_missile()
        # life_count_draw(900,650)
        # cloud_draw(500, 500)
        # collision_draw(300,400)
    glutSwapBuffers()       
        


################################  INPUT HANDLING   ##########################



def keyboardListener(key, x, y):
    global plane_x, plane_y, plane_angle, plane_speed, is_paused

    if is_paused:
        return 
    if key == b'a':
        plane_angle += 45
    elif key == b'd':
        plane_angle -= 45
    if abs(plane_angle) == 360:
        plane_angle = 0
    # elif key == b' ':  # Shoot missile
    #     bullets.append((plane_x, plane_y - 30))  # Add a bullet
    # elif key == b'':  # Activate special power
    #     if special_power_collected:
    #         special_power_active = True
    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global is_paused, height
    y = height - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 20 <= x <= 55 and 670 <= y<= 690:  # Play button
            is_paused = False
        elif 500 <= x <= 520 and 670 <= y<= 690:  # Pause button
            is_paused = True
        elif 960 <= x <= 980 and 670 <= y <= 690:  # Close button
            print("Goodbye!\nFinal Score:", score)
            glutLeaveMainLoop()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 700)
glutInitWindowPosition(250,0)
wind = glutCreateWindow(b"Missiles")
glClearColor(0.5,0.8,0.8,1.0)
glutDisplayFunc(showScreen)
glutIdleFunc(animation)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouse_click)
glutMainLoop()