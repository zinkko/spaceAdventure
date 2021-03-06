import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from math import hypot
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
#from kivy.uix.togglebutton import ToggleButton
#from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
#from kivy.uix.switch import Switch
#from kivy.uix.textinput import TextInput
from random import random
#from kivy.core.window import Window


'''Problems to be fixed:
-randoms go to the corner to the same place in the beginning of every game
-popup restart button doesn't work

  !!!!!!!!!!!!!!!!!!!!!
  !!!!!!!!!!!!!!!!!!!!!
  !!!!!          !!!!!!
  !!!!! REFACTOR !!!!!!
  !!!!!          !!!!!!
  !!!!!!!!!!!!!!!!!!!!!
  !!!!!!!!!!!!!!!!!!!!!

New aspects to be implemented:
--random pickup item
-restricting number of bluff's which don't attack
--good graphics :P
-flexible speed configuration
--maps extending beyound the window 
--custom start/goal -zones
-menu

Possible new elements

-blocks 
-bluffmaker-gun 
-guns 
-preselected routes 
'''  

class GameLayout(Widget):
    level=1
    progress=1
   
    #def __init__(self,**kwargs):
    #    super(GameLayout,self).__init__(**kwargs)
    
    start = ObjectProperty(None)
    gamezone = ObjectProperty(None)
    goal=ObjectProperty(None)
        
    k=0 
                  
    transition=ObjectProperty(None)  
    
    popup_layout=BoxLayout(orientation='vertical',spacing=10,padding=10)
    label=Label(text='Level Cleared!',size_hint=(1,0.6),font_size=50)
    button=Button(text='Next Level',size_hint=(1,0.2))
    restart_button=Button(text='Restart',size_hint=(1,0.2))
    
    popup_layout.add_widget(label)
    popup_layout.add_widget(button)
    popup_layout.add_widget(restart_button)
    
    transition=Popup(title='Congratulations!',
    content=popup_layout,
    size_hint=(0.8,0.8))
    button.bind(on_press=transition.dismiss)                    

    loss=ObjectProperty(None)
    
    new_layout=BoxLayout(orientation='vertical',spacing=10,padding=10)
    btn=Button(text='Start again!',size_hint=(1,0.2))
    txt=Label(text='All your ships have been destroyed.\n highest level reached: level %d' 
    %(progress),size_hint=(1,0.8))

    new_layout.add_widget(txt)
    new_layout.add_widget(btn)

    loss=Popup(title='Game Over',
    content=new_layout,
    size_hint=(0.8,0.8))
    btn.bind(on_press=loss.dismiss)
    
            
    def reset(self):
        self.start.hero.pos=375.0,5.0
        self.start.hero.speed=Vector(0,0)
        self.start.hero.velocity=3
        p1=self.start.pickup1
        p2=self.start.pickup2
        p1.pos=p1.reset_pos
        p2.pos=p2.reset_pos
        for j in self.baddies:
            j.pos=j.reset_pos 

    
    EnemyGraphics={
    'lurker':'Graphics/spacemine.png',
    'homer':'Graphics/alienship.png',
    'irris':'Graphics/sillynebula.png',
    'guard':'Graphics/defender.png',
    'bluff':'Graphics/broke_ship.png'
    }
    level1={'enemies':['homer','irris','irris'],'map':'Graphics/space.png',
    'positions':[(100,480),(400,300),(500,300)],'items':['boost','shield']}
    level2={'enemies':['guard','lurker','guard'],'map':'Graphics/space.png', 
    'positions':[(200,480),(300,300),(500,480)],'items':['empty','one_up']}
    level3={'enemies':['homer','homer','homer'],'map':'Graphics/space.png', 
    'positions':[(200,300),(400,300),(600,300)],'items':['boost','one_up']}
    level4={'enemies':['bluff','lurker','irris'],'map':'Graphics/space.png', 
    'positions':[(200,300),(400,300),(600,300)],'items':['boost','empty']} 
    level5={'enemies':['homer','lurker','homer'],'map':'Graphics/space.png',
    'positions':[(200,300),(400,300),(600,300)],'items':['boost','shield']} 
    level6={'enemies':['irris','guard','homer','irris'],'map':'Graphics/Sunrise.png', 
    'positions':[(200,300),(400,300),(600,300),(200,450)],'items':['boost','shield']} 
    level7={'enemies':['homer','homer','guard','guard'],'map':'Graphics/Sunrise.png',
    'positions':[(200,300),(400,300),(620,450),(180,450)],'items':['empty','one_up']}
    level8={'enemies':['lurker','irris','irris','lurker'],'map':'Graphics/Sunrise.png',
    'positions':[(50,400),(400,300),(600,300),(650,400)],'items':['boost','boost']}
    level9={'enemies':['homer','homer','bluff','bluff'],'map':'Graphics/Sunrise.png',
    'positions':[(350,500),(450,500),(90,400),(620,400)],'items':['boost','shield']}
    level10={'enemies':['lurker','homer','lurker','homer'],'map':'Graphics/Sunrise.png',
    'positions':[(200,300),(400,300),(600,300),(200,450)],'items':['empty','one_up']}
    level11={'enemies':['irris','irris','irris','irris','irris'],'map':'Graphics/supernova.png', 
    'positions':[(200,300),(400,300),(600,300),(200,450),(600,450)],'items':['boost','one_up']} 
    level12={'enemies':['guard','guard','guard','guard','guard'],'map':'Graphics/supernova.png',
    'positions':[(130,480),(260,480),(390,480),(520,480),(650,480)],'items':['boost','one_up']} 
    level13={'enemies':['bluff','bluff','bluff','guard','guard'],'map':'Graphics/supernova.png',
    'positions':[(200,300),(400,300),(600,300),(200,450),(600,450)],'items':['boost','empty']}
    level14={'enemies':['homer','homer','homer','homer','homer'],'map':'Graphics/supernova.png',
    'positions':[(200,300),(400,300),(600,300),(200,450),(600,450)],'items':['boost','empty']} 
    level15={'enemies':['homer','homer','homer','homer','lurker'],'map':'Graphics/supernova.png',
    'positions':[(160,300),(320,300),(480,300),(640,300),(400,450)],'items':['boost','empty']}
    
    Levels=[level1, level2, level3, level4, level5, level6, level7,level8, level9, level10, level11, 
    level12, level13, level14, level15]

    def set_graphics(self):
        for i in range(len(self.baddies)):
            level=self.Levels[self.level-1]
            positions=level['positions']
            enemy=self.baddies[i]
            enemy.placement=positions[i]
            enemy.graphics_file=self.EnemyGraphics[enemy.name]


    def list_baddies(self):

        try:
            level=self.Levels[self.level-1]
        except IndexError:
            level=self.Levels[-1]
            
        self.baddies=[] #-------------------------------------------------
        
        
        self.baddies.append(self.gamezone.enemy1)       # LE brute-force...
        self.baddies.append(self.gamezone.enemy2)
        self.baddies.append(self.gamezone.enemy3)

        if len(level['enemies'])==4:
            self.baddies.append(self.gamezone.enemy4)
            self.gamezone.enemy5.pos=-50,-50
        elif len(level['enemies'])==5:
            self.baddies.append(self.gamezone.enemy4)
            self.baddies.append(self.gamezone.enemy5)
        else:
            self.gamezone.enemy4.pos=-50,-50
            self.gamezone.enemy5.pos=-50,-50 #----------------------------

        print self.baddies
        
    def configure_level(self):
    
        level=self.Levels[self.level-1]

        self.list_baddies()
        
        item_list=level['items']
        p1=self.start.pickup1
        p2=self.start.pickup2
        
        p1.name=item_list[0]
        p2.name=item_list[1]

        p1.pict=p1.file_list[p1.name]
        p2.pict=p2.file_list[p2.name]
        
        l = self.start.lifebar
        
        l.graphics_file=l.files[l.lives-1]
        
        
             
        for i in range(0,len(self.baddies)):            
            names=level['enemies']
            self.baddies[i].name=names[i]
            
        self.gamezone.pict=level['map']

        
    def ItemAction(self,item,n):
            hero=self.start.hero
            lifebar=self.start.lifebar
            u=Vector(*item.center) ; v=Vector(*hero.center) 

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
            
            action={'boost':speed_boost,'one_up':plus_life,'shield':shield_up,'empty':empty}
            
            if v.distance(u)<40 and item.y < self.goal.y:
                action[item.name]()
                item.pos=(750-(n*50),550)
      
   
    ########
    # UPDATE
    ########
    
    def update(self, *args):        
         
        def RndHeading():
            rnd_x=random()*self.gamezone.width
            rnd_y=random()*self.gamezone.height
            heading=rnd_x,rnd_y
            return heading
            
        def set_patrol():
                pointA=self.goal.x,self.goal.y-60
                pointB=self.goal.right-50,self.goal.y-60
                return pointA,pointB

        l = self.start.lifebar
        self.start.hero.move()


        
        self.ItemAction(self.start.pickup1,0)
        self.ItemAction(self.start.pickup2,1)
        
        a=self.start.hero.x
        b=self.start.hero.y

        AI={
        'lurker':(a,Window.height/2),
        'homer':(a,b),
        'irris':RndHeading,
        'guard':set_patrol(),
        'bluff':(a,b)
        }            

        default_speed={
        'lurker':2.5,
        'homer':2.9,
        'irris':4,
        'guard':4,
        'bluff':5
        }
            
        
        if self.gamezone.collide_widget(self.start.hero):
            self.gamezone.text=''
            
            for i in self.baddies:
                if i.name=='irris':               
                    v=Vector(*i.rnd_heading); u=Vector(*i.pos)
                    
                    if i.counter%60==0 or u.distance(v)<25:
                        heading_giver=AI[i.name]
                        i.rnd_heading=heading_giver() 
                        i.counter=0 
                        

                    i.counter+=1 
                    heading=i.rnd_heading


                # Unnecessary brute-force!! 
                ###########################
                   
                elif i.name=='guard':
                    a1,b1=AI[i.name]
                    v=Vector(*i.pos); va=Vector(*a1); vb=Vector(*b1)
                                      
                    if v.distance(va)<25:
                        self.k=1
                    elif v.distance(vb)<25:
                        self.k=0
                    else:
                        pass
                    
                    if self.k==0:
                        heading=a1
                    elif self.k==1:
                        heading=b1
                    else:
                        pass
                       
                
                else:
                    heading=AI[i.name]
                                    
                if i.name!='bluff':
   
                    i.move(heading)
                                        

                elif Vector(*i.pos).distance(Vector(a,b))<200 and i.attack<0.7:
                    i.move(heading)
                else:
                    pass

                    
        
        for i in self.baddies:          # if baddies collide
            for j in self.baddies:
                if i!=j:
                    u=Vector(*i.pos)
                    v=Vector(*j.pos)
                    if u.distance(v)<50:
                        i.pos=2*(u-v)/hypot(*(u-v))+i.pos
                        j.pos=-2*(u-v)/hypot(*(u-v))+j.pos
                              

        for i in self.baddies:
            i.speed=default_speed[i.name] 
            hero=self.start.hero
            x1,y1=i.pos; x2,y2=hero.pos
            
            if hypot(x1-x2,y1-y2)<50 and hero.shield_up==False: # if player collides with enemy
            
                l.lives-=1
                
                self.list_baddies()
                    
                if l.lives==0:
                    self.loss.open()
                    l.lives=5
                    self.level=1
                    self.configure_level()
                    self.set_graphics()               
                    self.reset()
                    l.graphics_file=l.files[l.lives-1]
                else:
                  
                    l.graphics_file=l.files[l.lives-1]
                    
                
                    self.reset()
                    i.attack=random()

            elif hypot(x1-x2,y1-y2)<50 and hero.shield_up==True: 
                i.pos=(-100,-100)
                self.baddies.remove(i)
                hero.shield_up=False
                hero.graphic='Graphics/starship.png'
                
            elif self.start.hero.y>self.gamezone.top:  # if player reaches goal
            
                self.level+=1
                
                if self.level>self.progress:
                    self.progress=self.level
                    self.txt.text='All your ships have been destroyed.\n Highest level reached: level %d' %(self.progress)
                
                if self.level>len(self.Levels):
                    self.gamezone.text='You Won!'
                    self.start.hero.graphic='Graphics/starship_green.png'

                else:                    
                    self.gamezone.text='Level ' + str(self.level)
                    self.configure_level()
                    self.set_graphics()               
                    self.reset()
                    self.transition.open()
                    
            else:
                pass

                
######################        
# Fields on the screen
######################

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
    name='boost'
    pict=StringProperty('')
    file_list={'boost':'Graphics/canister.png',
    'shield':'Graphics/shield.png',
    'one_up':'Graphics/heart.png', #heart.png :)
    'empty':'Graphics/canister.png'}
    
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
    
    x1=NumericProperty(0)
    y1=NumericProperty(0)
    reset_pos=ReferenceListProperty(x1,y1)
    heading = 0,0
    speed=Vector(0,0)
    shield_up=False
    velocity=3
    graphic=StringProperty('Graphics/starship.png')
    
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
        p=Vector(*self.pos)
        h=Vector(*self.heading)

        if p.distance(h)>2: 
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
            

#####################
# Registering and App
#####################

Factory.register("GameLayout",GameLayout)
Factory.register("StartZone",StartZone)
Factory.register("GoalZone",GoalZone)
Factory.register("Hero",Hero)
Factory.register("Enemy",Enemy)
Factory.register("GameZone",GameZone)
Factory.register("Lifecounter",lifecounter)
Factory.register("PickupItem",PickupItem)

class GameApp(App):

    
    def build(self):
        layout=GameLayout()
        layout.configure_level()
        layout.set_graphics()

        Clock.schedule_interval(layout.update, 1.0/60.0)
        return layout


if __name__ in ('__android__','__main__'):
    GameApp().run()
