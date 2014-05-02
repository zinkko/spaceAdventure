import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from random import random
from math import hypot
from entities import *
from view import GameLayout
from game_engine import GameEngine

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
        layout= GameLayout()
        logic = GameEngine(layout)
        
        Clock.schedule_interval(logic.update, 1.0/60.0)
        return layout

if __name__ in ('__android__','__main__'):
    GameApp().run()
