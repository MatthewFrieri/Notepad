from math import *
import pygame as pg
import sys
import tkinter as tk
from tkinter import filedialog
pg.init()

# ~~~~~~~~~~~~~~~ Window setup ~~~~~~~~~~~~~~~ 
winW, winH = 700, 1000
WIN = pg.display.set_mode((winW, winH))
pg.display.set_caption("Notepad")
FPS = 1100
clock = pg.time.Clock()

canvas = pg.Surface((700, 1000))
lineWIN = None
BLACK = (0, 0, 0)

# Tkinter setup
root = tk.Tk()
root.withdraw()

# ~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~

def triangleArea(a, b, c):
    return abs(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))/2  

# ~~~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~~~

# Text
saveSmallFont = pg.font.SysFont('Calibri Bold', 30)
saveSmallSurface = saveSmallFont.render("Save", True, BLACK)
saveBigFont = pg.font.SysFont('Calibri Bold', 40)
saveBigSurface = saveBigFont.render("Save", True, BLACK)

loadSmallFont = pg.font.SysFont('Calibri Bold', 30)
loadSmallSurface = loadSmallFont.render("Load", True, BLACK)
loadBigFont = pg.font.SysFont('Calibri Bold', 40)
loadBigSurface = loadBigFont.render("Load", True, BLACK)

class Button:
    def __init__(self, x, y, w, h, color, style="color", rad=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.hover = False
        self.style = style
        self.rad = rad

    def draw(self):
        x, y = pg.mouse.get_pos()
        
        if self.style == "circle":
            popRad = 15
            # Already hovering
            if self.hover:
                if dist((x, y), (self.x, self.y)) <= self.rad + popRad:
                    pg.draw.circle(WIN, self.color, (self.x, self.y), self.rad + popRad)
                    pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad + popRad, 4)
                    
                else: 
                    self.hover = False
                    pg.draw.circle(WIN, self.color, (self.x, self.y), self.rad)
                    pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad, 4)

            # Not already hovering
            else:
                if dist((x, y), (self.x, self.y)) <= self.rad:
                    self.hover = True
                    pg.draw.circle(WIN, self.color, (self.x, self.y), self.rad + popRad)
                    pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad + popRad, 4)

                else: 
                    pg.draw.circle(WIN, self.color, (self.x, self.y), self.rad)
                    pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad, 4)

        elif self.style == "triangle":
            popRad = 15
            v1 = self.x, self.y - self.rad
            v2 = self.x - self.rad * sin(radians(60)), self.y + self.rad * cos(radians(60))
            v3 = self.x + self.rad * sin(radians(60)), self.y + self.rad * cos(radians(60))
            v1pop = self.x, self.y - (self.rad + popRad)
            v2pop = self.x - (self.rad + popRad) * sin(radians(60)), self.y + (self.rad + popRad)* cos(radians(60))
            v3pop = self.x + (self.rad + popRad) * sin(radians(60)), self.y + (self.rad + popRad)* cos(radians(60))

            # Already hovering
            if self.hover:
                if round(triangleArea(v1pop, v2pop, v3pop), 5) == round(triangleArea(v1pop, v2pop, (x, y)) + triangleArea(v1pop, (x, y), v3pop) + triangleArea((x, y), v2pop, v3pop), 5):
                    pg.draw.polygon(WIN, self.color, [v1pop, v2pop, v3pop])
                    pg.draw.polygon(WIN, BLACK, [v1pop, v2pop, v3pop], 4)
                    
                else: 
                    self.hover = False
                    pg.draw.polygon(WIN, self.color, [v1, v2, v3])
                    pg.draw.polygon(WIN, BLACK, [v1, v2, v3], 4)

            # Not already hovering
            else:
                if round(triangleArea(v1, v2, v3), 5) == round(triangleArea(v1, v2, (x, y)) + triangleArea(v1, (x, y), v3) + triangleArea((x, y), v2, v3), 5):
                    self.hover = True
                    pg.draw.polygon(WIN, self.color, [v1pop, v2pop, v3pop])
                    pg.draw.polygon(WIN, BLACK, [v1pop, v2pop, v3pop], 4)

                else: 
                    pg.draw.polygon(WIN, self.color, [v1, v2, v3])
                    pg.draw.polygon(WIN, BLACK, [v1, v2, v3], 4)

        elif self.style == "clear":
            popRad = 10
            # Already hovering
            if self.hover:
                if self.x - popRad <= x <= self.x + self.w + popRad and self.y - popRad <= y <= self.y + self.h + popRad:
                    pg.draw.rect(WIN, self.color, (self.x - popRad, self.y - popRad, self.w + popRad*2, self.h + popRad*2), 6, 2)
                    pg.draw.line(WIN, self.color, (self.x - popRad + 5, self.y - popRad + 5), (self.x + self.w + popRad - 5, self.y + self. h + popRad - 5), 8)

                else: 
                    self.hover = False
                    pg.draw.rect(WIN, self.color, (self.x, self.y, self.w, self.h), 4, 2)
                    pg.draw.line(WIN, self.color, (self.x + 3, self.y + 3), (self.x + self.w - 5, self.y + self.h - 5), 6)
            # Not already hovering
            else:
                if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
                    self.hover = True
                    pg.draw.rect(WIN, self.color, (self.x - popRad, self.y - popRad, self.w + popRad*2, self.h + popRad*2), 6, 2)
                    pg.draw.line(WIN, self.color, (self.x - popRad + 5, self.y - popRad + 5), (self.x + self.w + popRad - 5, self.y + self. h + popRad - 5), 8)

                else: 
                    pg.draw.rect(WIN, self.color, (self.x, self.y, self.w, self.h), 4, 2)
                    pg.draw.line(WIN, self.color, (self.x + 3, self.y + 3), (self.x + self.w - 5, self.y + self.h - 5), 6)



        # Squares
        else:
            if self.style == "color":
                popRad = 20
            else:
                popRad = 10



            # Already hovering
            if self.hover:
                if self.x - popRad <= x <= self.x + self.w + popRad and self.y - popRad <= y <= self.y + self.h + popRad:
                    pg.draw.rect(WIN, self.color, (self.x - popRad, self.y - popRad, self.w + popRad*2, self.h + popRad*2))
                    pg.draw.rect(WIN, BLACK, (self.x - popRad, self.y - popRad, self.w + popRad*2, self.h + popRad*2), 4, 2)
                    if self.style == "save":
                        WIN.blit(saveBigSurface, (self.x + self.w//2 - 33, self.y + self.h//2 - 13))
                    elif self.style == "load":
                        WIN.blit(loadBigSurface, (self.x + self.w//2 - 33, self.y + self.h//2 - 13))
                              


                else: 
                    self.hover = False
                    pg.draw.rect(WIN, self.color, (self.x, self.y, self.w, self.h))
                    pg.draw.rect(WIN, BLACK, (self.x, self.y, self.w, self.h), 4, 2)
                    if self.style == "save":
                        WIN.blit(saveSmallSurface, (self.x + self.w//2 - 23, self.y + self.h//2 - 10))
                    elif self.style == "load":
                        WIN.blit(loadSmallSurface, (self.x + self.w//2 - 23, self.y + self.h//2 - 10))
                    
            # Not already hovering
            else:
                if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
                    self.hover = True
                    pg.draw.rect(WIN, self.color, (self.x - popRad, self.y - popRad, self.w + popRad*2, self.h + popRad*2))
                    pg.draw.rect(WIN, BLACK, (self.x - popRad, self.y - popRad, self.w + popRad*2, self.h + popRad*2), 4, 2)
                    if self.style == "save":
                        WIN.blit(saveBigSurface, (self.x + self.w//2 - 33, self.y + self.h//2 - 13))
                    elif self.style == "load":
                        WIN.blit(loadBigSurface, (self.x + self.w//2 - 33, self.y + self.h//2 - 13))
                    
                else: 
                    pg.draw.rect(WIN, self.color, (self.x, self.y, self.w, self.h))
                    pg.draw.rect(WIN, BLACK, (self.x, self.y, self.w, self.h), 4, 2)
                    if self.style == "save":
                        WIN.blit(saveSmallSurface, (self.x + self.w//2 - 23, self.y + self.h//2 - 10))
                    elif self.style == "load":
                        WIN.blit(loadSmallSurface, (self.x + self.w//2 - 23, self.y + self.h//2 - 10))
                            
black = Button(37, 20, 40, 40, (0, 0, 0))
white = Button(37, 85, 40, 40, (255, 255, 255))
gray = Button(102, 20, 40, 40, (127, 127, 127))
grayL = Button(102, 85, 40, 40, (195, 195, 195))
burgundy = Button(167, 20, 40, 40, (136, 0, 21))
brown = Button(167, 85, 40, 40, (185, 122, 87))
red = Button(232, 20, 40, 40, (237, 28, 36))
pink = Button(232, 85, 40, 40, (255, 174, 201))
orange = Button(297, 20, 40, 40, (255, 127, 39))
yellowD = Button(297, 85, 40, 40, (255, 201, 14))
yellow = Button(362, 20, 40, 40, (255, 242, 0))
yellowL = Button(362, 85, 40, 40, (239, 228, 176))
green = Button(427, 20, 40, 40, (34, 177, 76))
greenL = Button(427, 85, 40, 40, (181, 230, 29))
blue = Button(492, 20, 40, 40, (0, 162, 232))
blueL = Button(492, 85, 40, 40, (153, 217, 234))
blueD = Button(557, 20, 40, 40, (63, 72, 204))
cyan = Button(557, 85, 40, 40, (112, 146, 190))
purple = Button(622, 20, 40, 40, (163, 73, 164))
mauve = Button(622, 85, 40, 40, (200, 191, 231))
circle = Button(109, 170, None, None, BLACK, rad=20, style="circle")
square = Button(159, 150, 40, 40, BLACK, style="square")
triangle = Button(251, 175, None, None, BLACK, rad=25, style="triangle")
line = Button(302, 160, 60, 20, BLACK, style="line")
clear = Button(392, 150, 40, 40, (255, 0, 0), style="clear")
save = Button(462, 150, 60, 40, (255, 233, 162), style="save")
load = Button(552, 150, 60, 40, (255, 233, 162), style="load")
inLine = False
buttons = [black, white, gray, grayL, burgundy, brown, red, pink, orange, yellowD, yellow, yellowL, green, greenL, blue, blueL, blueD, cyan, purple, mauve, circle, square, triangle, line, clear, save, load]

class Pen:
    def __init__(self, color, rad):
        self.color = color
        self.rad = rad
        self.style = "circle"
        self.x = 0
        self.y = 0
        self.down = False

    def draw(self):
        if self.style == "circle":
            pg.draw.circle(canvas, pen.color, (pen.x, pen.y), pen.rad)
        elif self.style == "square":
            pg.draw.rect(canvas, pen.color, (pen.x-pen.rad, pen.y-pen.rad, pen.rad*2, pen.rad*2))
        elif self.style == "triangle":
            v1 = self.x, self.y - self.rad
            v2 = self.x - self.rad * sin(radians(60)), self.y + self.rad * cos(radians(60))
            v3 = self.x + self.rad * sin(radians(60)), self.y + self.rad * cos(radians(60))
            pg.draw.polygon(canvas, self.color, [v1, v2, v3])
        elif self.style == "line":
            global lineWIN
            lineWIN = pg.Surface.copy(canvas)
            pg.draw.line(lineWIN, self.color, start, (pen.x, pen.y), self.rad)

pen = Pen((0, 0, 0), 7)

class Slider():
    def __init__(self, x, y, rad, val):
        self.x = x
        self.y = y
        self.rad = rad
        self.val = val
        self.color = BLACK
        self.inSlide = False
        self.hover = False
    
    def draw(self):
        x, y = pg.mouse.get_pos()
        popRad = 10
        # Already hovering
        if self.hover or self.inSlide:
            if not dist((x, y), (self.x, self.y)) <= self.rad + popRad:
                self.hover = False
            pg.draw.circle(WIN, self.color, (self.x, self.y), self.rad + popRad)
            pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad + popRad, 4)

        # Not already hovering
        else:
            if dist((x, y), (self.x, self.y)) <= self.rad:
                self.hover = True
                pg.draw.circle(WIN, self.color, (self.x, self.y), self.rad + popRad)
                pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad + popRad, 4)

            else: 
                pg.draw.circle(WIN, self.color, (self.x, self.y), self.rad)
                pg.draw.circle(WIN, BLACK, (self.x, self.y), self.rad, 4)

        # Text
        myfont = pg.font.SysFont('Calibri Bold', 70)
        textsurface = myfont.render(str(self.val), True, BLACK)
        w, h = myfont.size(str(self.val))

        WIN.blit(textsurface, (635 - (w/2), 220))
slider = Slider(230, 245, 20, 4)


# ~~~~~~~~~~~~~~~ MAIN LOOP ~~~~~~~~~~~~~~~

WIN.fill((255, 255, 255))
canvas.fill((255, 255, 255))
while True:
    clock.tick(FPS)
    pen.x, pen.y = pg.mouse.get_pos()
    for event in pg.event.get():
        # Mouse down
        pressed = pg.mouse.get_pressed()

        if event.type == pg.MOUSEBUTTONDOWN and pressed[0]:
            if pen.style == "line" and pen.y >= winH - winW:
                start = pen.x, pen.y
                inLine = True

            if pen.y > winH-winW:
                pen.down = True
            for button in buttons:
                if button.hover:
                    if button.style == "color":
                        pen.color = button.color
                        circle.color = button.color
                        square.color = button.color
                        triangle.color = button.color
                        line.color = button.color
                        slider.color = button.color
                    elif button.style == "clear":
                        canvas.fill((255, 255, 255))
                        if lineWIN:
                            lineWIN.fill((255, 255, 255))
                    elif button.style == "load":
                        # Override canvas
                        filePath = filedialog.askopenfilename()
                        if filePath:
                            loaded = pg.image.load(filePath)
                            loaded = pg.transform.scale(loaded, (700, 700))
                            canvas.blit(loaded, (0, 300))
                    elif button.style == "save":
                        # Save screenshot
                        filePath = filedialog.asksaveasfilename(defaultextension="png", filetypes=[("PNG File", ".png"), ("JPEG File", ".jpeg")])
                        if filePath:
                            img = pg.Surface((700, 700))
                            img.blit(canvas, (0, 0), (0, 300, 700, 700))
                            pg.image.save(img, filePath)                    
                    else:
                        pen.style = button.style
                    break
            if slider.hover:
                slider.inSlide = True

        # Mouse up
        elif event.type == pg.MOUSEBUTTONUP and not pressed[0]:
            pen.down = False
            slider.inSlide = False
            if inLine and lineWIN:
                canvas = pg.Surface.copy(lineWIN)
                inLine = False
        
        # Check quit
        elif event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()

    # Within canvas
    if pen.y > winH-winW and pen.down:
        pen.draw()

    # Move slider
    if slider.inSlide:   
        if pg.mouse.get_pressed()[0]:
            x, y = pg.mouse.get_pos()
            if x < 86:
                slider.x = 57
                slider.val = 1
                pen.rad = 1
            elif x < 144:
                slider.x = 115
                slider.val = 2
                pen.rad = 2
            elif x < 201:
                slider.x = 173
                slider.val = 3
                pen.rad = 4
            elif x < 259:
                slider.x = 230
                slider.val = 4
                pen.rad = 7
            elif x < 317:
                slider.x = 288
                slider.val = 5
                pen.rad = 12
            elif x < 375:
                slider.x = 346
                slider.val = 6
                pen.rad = 18
            elif x < 432:
                slider.x = 404
                slider.val = 7
                pen.rad = 25
            elif x < 490:
                slider.x = 461
                slider.val = 8
                pen.rad = 35
            elif x < 548:
                slider.x = 519
                slider.val = 9
                pen.rad = 45
            else:
                slider.x = 577
                slider.val = 10
                pen.rad = 70
            
    # ~~~ DRAW BUTTONS ~~~
    pg.draw.rect(WIN, (255, 255, 255), (0, 0, winW, winH-winW))
    pg.draw.line(WIN, BLACK, (57, 245), (577, 245), 5)
    # Slider Increments
    pg.draw.line(WIN, BLACK, (57, 238), (57, 252), 3)
    pg.draw.line(WIN, BLACK, (115, 238), (115, 252), 3)
    pg.draw.line(WIN, BLACK, (173, 238), (173, 252), 3)
    pg.draw.line(WIN, BLACK, (230, 238), (230, 252), 3)
    pg.draw.line(WIN, BLACK, (288, 238), (288, 252), 3)
    pg.draw.line(WIN, BLACK, (346, 238), (346, 252), 3)
    pg.draw.line(WIN, BLACK, (404, 238), (404, 252), 3)
    pg.draw.line(WIN, BLACK, (461, 238), (461, 252), 3)
    pg.draw.line(WIN, BLACK, (519, 238), (519, 252), 3)
    pg.draw.line(WIN, BLACK, (577, 238), (577, 252), 3)


    for button in buttons:
        button.draw()
    slider.draw()

    if inLine and lineWIN:
        WIN.blit(lineWIN, (0, 300), (0, 300, 700, 700))
    else:
        WIN.blit(canvas, (0, 300), (0, 300, 700, 700))

    pg.display.update()
