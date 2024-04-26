# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:38:58 2024

@author: marve
"""
import pygame, simpleGE, random
""" Save Gary from the fire 
"""

class Fire(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
    
        self.setImage("fire.png")
        self.setSize(35, 35)
        self.minSpeed = 3
        self.maxSpeed = 4
        self.reset()
        
    def reset(self):
            #move to the top of screen 
            self.y = 10
            
            #x is random 0 - screen width 
            self.x = random.randint(0, self.screenWidth)
            
            #dy is random minSpeed to maxSpeed 
            self.dy = random.randint(self.minSpeed, self.maxSpeed)
            
    def checkBounds(self):
            if self.bottom > self.screenHeight: 
                self.reset()
                

                
class GaryFood(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("gary_food.png")
        self.setSize(50, 50)
        self.position = (520, 330)
    
        
class Gary(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("gary.png")
        self.setSize(50, 50)
        self.position = (320, 400)
        self.moveSpeed = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT): 
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
    
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        
    
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time: 10"
        self.center = (500, 30)

   
    

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("spongebac.jpeg")
        #self.sndFire = pygame.mixer.Sound("Spongebob.mp3")  # Ensure this path is correct
        self.sndFire = simpleGE.Sound("sound.mp3")
        self.sndFire.play()
        
        self.timer = simpleGE.Timer()
        self.timer.start()
        
        
        self.timerScore = simpleGE.Timer()
        self.timerScore.start()
        self.score = 0
        
        self.lblTime =LblTime()
        self.lblScore = LblScore()
        

        self.Gary = Gary(self)
        self.Fire = []
        self.GaryFood = GaryFood(self)
        
        
        for i in range(10):
            self.Fire.append(Fire(self))
            
            self.lblScore = LblScore()
            self.lblTime = LblTime()
        
            self.sprites = [self.Gary,
                            self.GaryFood,
                            self.Fire,
                            self.lblScore, 
                            self.lblTime]
            
                        
        
    def process(self):
        if self.timerScore.getElapsedTime() >= 2:
            self.score += 3
            #self.maxSpeed += 1
            self.timerScore.start()
        self.lblScore.text = f"Score: {self.score}"
        
        if self.Gary.collidesWith(self.GaryFood):
            print("Collision with GaryFood detected!")
            #self.sndFire.play()  
            self.GaryFood.reset()
            #self.lblScore.text = "Game Passed"
            self.stop()  # Handling after collision
        
        for Fire in self.Fire:
            if self.Gary.collidesWith(Fire):
                print("yes")
                Fire.reset() 
                self.stop()
                #self.score += 1
                
         
        self.lblTime.text = f"Time: {self.timer.getElapsedTime():.2f}"
            
       # if self.timer.getTimeLeft() < 0: 
          # print(f"Final Score: {self.score}")
           #self.stop()
                   
class Instructions(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("spongebac.jpeg")
        
        self.response = "Play"
        
        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = [
        "You are a gary trying to escape the fire destroying",
        "the bikini bottom and also the annoying sound",
        "Move with the left and right arrow keys",
        "Your scores increases based on how long you",
        "spend on the game",
        "Have fun!"]
        
        self.instructions.center = (320, 240)
        self.instructions.size = (500, 250)
        
        self.prevScore = score
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.lblScore.center = (320, 400)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (up)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)
        
        self.sprites = [self.instructions,
                        self.lblScore,
                        self.btnQuit,
                        self.btnPlay]
    def process(self):
        #buttons
           if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
           if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()

        #arrow keys
           if self.isKeyPressed(pygame.K_UP):
            self.response = "Play"
            self.stop()
           if self.isKeyPressed(pygame.K_DOWN):
            self.response = "Quit"
            self.stop()

def main():
    
    keepGoing = True
    score = 0
    while keepGoing:
    
        instructions = Instructions(score)
        instructions.start()
                
        if instructions.response == "Play":    
            game = Game()
            game.start()
            score = game.score
        else:
            keepGoing = False
                 
                    
                     
if __name__ =="__main__":
    main()
                 
    
    