import kivy
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty
from kivy.vector import Vector

class StartZone(Widget):
    hero = ObjectProperty(None)
    lifebar = ObjectProperty(None)
    pickup1 = ObjectProperty(None)
    pickup2 = ObjectProperty(None)
    
class GoalZone(Widget):
    pass

class GameZone(Widget):

    #def __init__(self,**kwargs):
      #  super(GameZone, self).__init__(**kwargs)
    pict=StringProperty('Graphics/space.png')
    level=str(GameLayout().level)

    
    enemy1=ObjectProperty(None)
    enemy2=ObjectProperty(None)
    enemy3=ObjectProperty(None)
    enemy4=ObjectProperty(None)
    enemy5=ObjectProperty(None)

    layout=GameLayout()
    level=layout.Levels[layout.level-1]
    number=len(level['enemies'])
    
    text=StringProperty('')
    
##########
# Entities
##########

class PickupItem(Widget):
    #name='boost'
    #pict=StringProperty('')
    
    file_list={'boost':'Graphics/canister.png',
    'shield':'Graphics/shield.png',
    'one_up':'Graphics/heart.png', #heart.png :)
    'empty':'Graphics/canister.png'}
    
    functions = {'boost':speed_boost,
    'shield':shield_up,
    'one_up':plus_life,
    'empty':empty}
    
    def __init__(self,**kwargs):
        super(PickupItem,self).__init__(**kwargs)
        self.name = 'empty'
        #if name not in file_list:
        #    self.name = 'empty'
        self.pict = StringProperty(self.file_list[name])
    
    def item_action(self):
        self.functions[self.name]()
    
    def speed_boost():
        hero.velocity=4

    def plus_life():
        if lifebar.lives < 8:
            lifebar.lives+=1
            lifebar.graphics_file=lifebar.files[lifebar.lives-1]
        else:
            pass 


    def shield_up():
        hero.shield_up=True
        hero.graphic='Graphics/starship_shield.png'

    def empty():
        pass

class lifecounter(Widget):

    lives=NumericProperty(5)
    graphics_file=StringProperty('')
    files=['Graphics/hangar0.png',
    'Graphics/hangar1.png',
    'Graphics/hangar2.png',
    'Graphics/hangar3.png',
    'Graphics/hangar4.png',
    'Graphics/hangar5.png',
    'Graphics/hangar6.png',
    'Graphics/hangar7.png']
    
class Hero(Widget):
    
    def __init__(self,**kwargs):
        super(Hero,self).__init__(**kwargs)
        self.x1=NumericProperty(0)
        self.y1=NumericProperty(0)
        self.reset_pos=ReferenceListProperty(x1,y1)
        self.heading = 0,0
        self.speed=Vector(0,0)
        self.shield_up=False
        self.velocity=3
        self.graphic=StringProperty('Graphics/starship.png')
    
    def on_touch_down(self,touch):
        a=touch.x-self.width/2 ; b=touch.y
        if a<0:
            a=0
        elif a>(Window.width-50):
            a=Window.width-50
        elif b>Window.height-50:
            b=Window.height-50
        else:
            pass
        self.heading=a,b
        v=Vector(a,b)
        u=Vector(self.pos)
        d=u.distance(v)
        new_vector=v-u

        try:
            new_vector *= (self.velocity/d)
        except ZeroDivisionError:
            new_vector= 0,0

        self.speed[0]=new_vector[0]
        self.speed[1]=new_vector[1]     
     
    def move(self): 
        position=Vector(*self.pos)
        heading=Vector(*self.heading)

        if position.distance(heading) > 2: 
            self.pos = self.speed + self.pos
        else:
            pass

        
class Enemy(Widget):  
    rnd_heading=375,5
    X=NumericProperty(0)
    Y=NumericProperty(0)
    placement=ReferenceListProperty(X,Y)
    attack=random()
    graphics_file=StringProperty('')
    name='homer'
    reset_x=NumericProperty(0)
    reset_y=NumericProperty(0)
    reset_pos=ReferenceListProperty(reset_x,reset_y)
    speed=3
    start=StartZone
    counter=0
  
    def move(self,heading):
        v=Vector(*heading)
        u=Vector(self.pos)
        d=u.distance(v)
        speed_vector=v-u
        try:
            speed_vector *= (self.speed/d)
        except ZeroDivisionError:
            speed_vector=Vector(0,0)
        self.pos = speed_vector + self.pos
