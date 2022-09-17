import pygame as pg
from numpy import sin, cos, e, pi, sqrt, arctan2

class Graph:
  def __init__(self, eq, x_min, y_min, x_max, y_max):
    self.eq = eq
    self.x_min = x_min
    self.y_min = y_min
    self.x_max = x_max
    self.y_max = y_max

  def xc_to_c(self, x):
    return win_size[0]*(x-self.x_min)/(self.x_max-self.x_min)
  
  def yc_to_c(self, y):
    return win_size[1]*(y-self.y_max)/(self.y_min-self.y_max)

  def c_to_c(self, x, y):
    return (int(self.xc_to_c(x)), int(self.yc_to_c(y)))

  def draw_axes(self, color):
    pg.draw.line(win, color, (0, self.yc_to_c(0)), (win_size[0], self.yc_to_c(0)))
    pg.draw.line(win, color, (self.xc_to_c(0), 0), (self.xc_to_c(0), win_size[1]))

  def draw_graph(self):
    spacing = 100
    try:
      for i in range(spacing*self.x_min, spacing*(self.x_max-self.x_min)):
        x = i/spacing+pi/(10*spacing)
        try:
          pg.draw.circle(win, (0,0,255), self.c_to_c(x, eval(self.eq)), 1)
        except:
          continue
    except:
      None

  def draw(self):
    self.draw_axes()
    self.draw_graph()

class Differential(Graph):
  def __init__(self, eq, x_min, y_min, x_max, y_max):
    super().__init__(eq, x_min, y_min, x_max, y_max)

  def draw_graph(self, color):
    spacing = 50
    d = (self.x_max - self.x_min)/200
    for x in range(spacing):
      x = x/spacing*(self.x_max-self.x_min)+self.x_min
      for y in range(spacing):
        y = y/spacing*(self.y_max-self.y_min)+self.y_min
        try:
          dx = d*cos(arctan2(eval(self.eq), 1))
          dy = d*sin(arctan2(eval(self.eq), 1))
        except:
          dx = 0
          dy = d
        try:
          pg.draw.line(win, color, super().c_to_c(x-dx, y-dy), super().c_to_c(x+dx, y+dy))
        except:
          pass

  def draw(self, a_color, d_color):
    super().draw_axes(a_color)
    self.draw_graph(d_color)

class Particle:
  def __init__(self, P, V, f):
    self.x = P[0]
    self.y = P[1]
    self.vx = V[0]
    self.vy = V[1]
    self.t = 0.5
    self.d = 0.1
    self.f = f

  def move(self):
    self.x = self.x+(self.vx*self.t)
    self.y = self.y+(self.vy*self.t)
    x = self.x
    y = self.y
    print(self.vx, self.vy)
    try:
      self.vx, self.vy = self.evaluate_closer()
      
    except:
        self.vx = 0
        self.vy = self.d
    
    self.draw()

  def draw(self):
    pg.draw.circle(win, (255,0,255), f.c_to_c(self.x, self.y), 1)

  def evaluate_closer(self):
    x = self.x
    y = self.y
    v = (self.d*cos(arctan2(eval(f.eq))), self.d*sin(arctan2(eval(f.eq))))
    if self.closer(self.vx, cos):# or self.closer(self.vy, sin):
        return v
    else:
        return -v[0], -v[1]

  def closer(self, v, func):
    x = self.x
    y = self.y
    return abs(v - self.d*func(arctan(eval(f.eq)))) < abs(v + self.d*func(arctan(eval(f.eq))))
    
pg.init()

win_size = (800,800)
win=pg.display.set_mode(win_size, pg.RESIZABLE)
pg.display.set_caption("Game")
bg_color = (0,0,0)
a_color = (100,100,100)
d_color = (255,100,100)
win.fill(bg_color)
run = True
f = Differential('sin(x*y)', -100, -100, 100, 100)
#p = Particle((5, 0), (0, 0), f)
f.draw(a_color, d_color)
pg.display.update()
while run:
  pg.time.delay(10)
  for i in pg.event.get():
    if i.type == pg.QUIT:
      run=False
            
    elif i.type == pg.VIDEORESIZE:
      win_size = i.size
      win=pg.display.set_mode(win_size, pg.RESIZABLE)
      win.fill(bg_color)
            
    k = pg.key.get_pressed()
    #p.move()
    f.draw(a_color, d_color)
        
    if k[pg.K_ESCAPE]:
      run=False

    pg.display.update()

pg.quit()
