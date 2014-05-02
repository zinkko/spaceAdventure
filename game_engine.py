class GameEngine(object):
      
    def __init__(self, layout):
        if not isinstance(layout,GameLayout):
            raise ValueError
        self.layout = layout
            
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

