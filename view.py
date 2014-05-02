
class GameLayout(Widget):
    level=1
    progress=1
   
    
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

    
    EnemyGraphics={
    'lurker':'Graphics/spacemine.png',
    'homer':'Graphics/alienship.png',
    'irris':'Graphics/sillynebula.png',
    'guard':'Graphics/defender.png',
    'bluff':'Graphics/broke_ship.png'
    }
