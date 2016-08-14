import pygame, sys, random, math, time
from pygame.locals import *

pygame.init()
width = 700
height = 700
#load font, prepare values
font = pygame.font.Font(None, 40)
fg = 0,0,0
bg = 5, 5, 5
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

def rotate_3d_points(points, angle_x, angle_y, angle_z):
    new_points = []
    for point in points:
        x = point[0]
        y = point[1]
        z = point[2]
        new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
        y = new_y
        # isn't math fun, kids? 
        z = new_z
        new_x = x * math.cos(angle_y) - z * math.sin(angle_y)
        new_z = x * math.sin(angle_y) + z * math.cos(angle_y)
        x = new_x
        z = new_z
        new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
        new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
        x = new_x
        y = new_y
        new_points.append([x, y, z])
    return new_points

def do_line_demo(surface, counter):
    color = (0, 0, 0) # black
    cube_points = [ [-1, -1, 1], [-1, 1, 1], [1, 1, 1], [1, -1, 1], [-1, -1, -1], [-1, 1, -1], [1, 1, -1],[1, -1, -1] ]                    
    connections = [ (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7) ]
                
    t = counter * 2 * 3.14159 / 60 # this angle is 1 rotation per second
        
    # rotate about x axis every 2 seconds 
    # rotate about y axis every 4 seconds 
    # rotate about z axis every 6 seconds 
    points = rotate_3d_points(cube_points, t / 2, t / 4, t / 6)
    flattened_points = []
    for point in points:
        flattened_points.append((point[0] * (1 + 1.0 / (point[2] + 3)), point[1] * (1 + 1.0 / (point[2] + 3))))
        for con in connections:
            p1 = flattened_points[con[0]]
            p2 = flattened_points[con[1]]
            x1 = p1[0] * 60 + 200
            y1 = p1[1] * 60 + 150
            x2 = p2[0] * 60 + 200
            y2 = p2[1] * 60 + 150
                
            # This is the only line that really matters 
            pygame.draw.line(surface, color, (x1, y1), (x2, y2), 4)


class RotatingCube:
    "Moving finish line, to get a lap, you have to lap the finish line"

    def __init__(self, title):
      self.count = 1
      self.title = title

    def move(self):
      self.count+=1
      do_line_demo(DISPLAYSURF,self.count)
        


class Animation:
   'Animation by Melanie and Lizzie'

   def changebehaviour(self):
      self.stepsize = random.randrange(-5,10)
      self.lateralvariationfrequency = random.randrange(5,15)/10.0;
      self.lateralvariationamplitude = random.randrange(15,30)

   def __init__(self, filename, title, titlecolor, x, y):
      self.image = pygame.transform.scale(pygame.image.load(filename),(150,150))
      self.x = x
      self.y = y
      self.direction = 'right'
      self.title = title
      self.titlecolor = titlecolor
      self.laps = 0
      self.lateralvariation = 0;
      self.xoffset = 0
      self.yoffset = 0
      self.count = 0
      # Set up a list of all of the racers locations over every 3 laps of the race
      self.points = [(x,y)]
      Animation.changebehaviour(self)
          
   def move(self):      
    self.count+=1
    if (self.count%360 == 0):
        Animation.changebehaviour(self)

    if (abs(self.stepsize)<=1) :
        "Spin in a circle if small stepsize"
        self.xoffset = (self.count%360)/135*self.lateralvariationamplitude*math.sin((3.141592653589793238462643383950288*2*self.lateralvariationfrequency*self.count)/FPS)
        self.yoffset = (self.count%360)/135*self.lateralvariationamplitude*math.cos((3.141592653589793238462643383950288*2*self.lateralvariationfrequency*self.count)/FPS)
    else:
        self.lateralvariation = self.lateralvariationamplitude*math.sin((3.141592653589793238462643383950288*2*self.lateralvariationfrequency*self.count)/FPS)        
        if self.direction == 'right':
            self.x += self.stepsize
            self.yoffset = self.lateralvariation
            self.xoffset = 0
            if self.x > width - self.image.get_width() :
                self.direction = 'down'
        elif self.direction == 'down':
            self.y += self.stepsize
            self.yoffset = 0
            self.xoffset = self.lateralvariation
            if self.y > height - self.image.get_height():
                self.direction = 'left'
        elif self.direction == 'left':
            self.x -= self.stepsize
            self.xoffset = 0
            self.yoffset = self.lateralvariation
            if self.x < 10:
                self.direction = 'up'
        elif self.direction == 'up':
            self.y -= self.stepsize 
            self.yoffset = 0
            self.xoffset = self.lateralvariation
            self.laps +=1
            # Reset points after 3 laps
            # if self.laps > 2:
            # self.points = [ self.points[-1]]
            if self.y < 10:
                self.direction = 'right'
    #no AA, no transparancy, normal
    ren = font.render(self.title, 1, self.titlecolor)
    DISPLAYSURF.blit(self.image, (self.x+self.xoffset, self.y+self.yoffset))
    # 
    DISPLAYSURF.blit(ren, (self.x+self.xoffset+(self.image.get_width()-ren.get_width())/2, self.y+self.yoffset+self.image.get_height()))
    # Find middle of image
    # Insert point into points array
    self.points.append((self.x+self.xoffset+self.image.get_width()/2, self.y+self.yoffset+self.image.get_height()/2))
    
    # Draw points on screen
    pygame.draw.lines(DISPLAYSURF, self.titlecolor, 0, self.points, 2)
    
   

  

# set up the window
DISPLAYSURF = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption('Animation')

def team(race,image,color,names):
    for name in names:
        race.append(Animation(image,name,color,10,10))

WHITE = (12, 34, 56)

racers = []


#racers.append(RotatingCube('Cube'))
team(racers,'pi.PNG',(235,254,40),['3.1415926','5358979','323846264','338327950288'])
team(racers,'rat.png',(80,255,200),['Toopy','Latte','Pinball','Snickers'])
team(racers,'unicorn.png',(255, 0, 255),['Parker','Teddy Best','Positive Teddy'])



while True: # the main game loop
    DISPLAYSURF.fill(WHITE)

    for racer in racers:
        racer.move()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)


   
      
