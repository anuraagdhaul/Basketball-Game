# Write your code here :-)
import pygame
import random
import pgzrun
import Games
import subprocess
import sys
from SpeedShot import *
from FastFootwork import *
from Tutorial import *

WIDTH = 960
HEIGHT = 600
counter = False  # keeps track of button click
player = Actor("player_copy", (480, 550))
#ai_player = Actor("player_copy", (400, 550))
ball = Actor("ball")
ball.x = player.x - 6
ball.y = player.y
ballcounter = False
ball_who = 'player'
ballx = 0
bally = 0
gravity = 0.3
button_pressed = False
timer = 90
timer_on = False
games_submenu = False

# Prediction UI
prediction_chance = 0.0
prediction_color = "gray"
prediction_timer = 0


def challengeaction():
    global counter
    counter = True
 
def start_game():
    subprocess.Popen(["pgzrun", "Games.py"])

def start_speedshot():
    subprocess.Popen(["pgzrun", "SpeedShot.py"])



challengebutton = Rect((380, 250), (200, 60))
gamesbutton = Rect((380, 340), (200, 60))
rankingbutton = Rect((380, 430), (200, 60))
pointsbutton = Rect((380, 520), (200, 50))
tutorialbutton = Rect((780, 40), (140, 50))
homebutton = Rect((40, 40), (140, 50))
righthoop = Rect((800, 270), (70, 15))
righthoopbackboard = Rect((800, 290), (70, 40))
speedshotscore = 0


speedshotbutton = Rect((170, 220), (250, 140))
fastfootworkbutton = Rect((540, 220), (250, 140))
dogbutton = Rect((360, 420), (250, 140))

def draw():
    global counter, speedshotscore, button_pressed
    screen.clear()
    screen.fill((249, 246, 232))
    screen.blit(images.court2, (0, 180))



    # -------------- Buttons --------------
    if counter == False:
        # -------- Header ----------

        screen.draw.text("Welcome to the Basketball Game!", center=(WIDTH // 2, 130), color="black", fontsize=40,)

        screen.draw.text("Continue your journey:", center=(WIDTH // 2, 170), color="black", fontsize=30)

        # Challenge button
        screen.draw.filled_rect(challengebutton, "#fdd76e")
        screen.draw.text("Challenges", center=challengebutton.center, color="black", fontsize=28)

        # Games button
        screen.draw.filled_rect(gamesbutton, "#a5cdff")
        screen.draw.text("Games", center=gamesbutton.center, color="black", fontsize=28)

        # Ranking button
        screen.draw.filled_rect(rankingbutton, "#d7c9e9")
        screen.draw.text("Ranking", center=rankingbutton.center, color="black", fontsize=28)

        # Points button
        screen.draw.filled_rect(pointsbutton, "#b7e3a0")
        screen.draw.text("Points", center=pointsbutton.center, color="black", fontsize=28)

        # Tutorial button
        screen.draw.filled_rect(tutorialbutton, "#baf3f7")
        screen.draw.text("Tutorial", center=tutorialbutton.center, color="black", fontsize = 28)

        # Player
        original = images.player_copy  # no .png
        resized = pygame.transform.scale(original, (75, 180))
        screen.blit(resized, (650, 250))


    if  counter == True:
        screen.draw.filled_rect(speedshotbutton, "#990F02")
        screen.draw.text("Speed Shot\n\nMake 30 baskets in 90 seconds", center=speedshotbutton.center, color="white")
        #screen.draw.text(, center = (200, 150), fontsize = 30, color="white")

        # Home button
        screen.draw.filled_rect(homebutton, "#baf3f7")
        screen.draw.text("Home", center=homebutton.center, color="black", fontsize = 28)

        screen.draw.filled_rect(fastfootworkbutton, "#960019")
        screen.draw.text("Fast Footwork", center=fastfootworkbutton.center, color="white")

        screen.draw.filled_rect(dogbutton, "#960019")
        screen.draw.text("D.O.G", center=dogbutton.center, color="white")

        screen.draw.text("Choose a challenge and try to earn some points!", center=(WIDTH // 2, 130), color="black", fontsize=40)

        if timer == 0:
            counter = True


    if counter == "Speed Shot":
        speedshotdraw(screen)

    if counter == "Fast Footwork":
        fastfootworkdraw(screen)

        # Draw prediction bar if timer active
        if prediction_timer > 0:
            bar_width = 300
            bar_height = 20
            bar_x = WIDTH // 2 - bar_width // 2
            bar_y = 100
            fill_width = int(bar_width * prediction_chance)
            screen.draw.text("Shot Accuracy", center=(WIDTH // 2, bar_y - 25), fontsize=30, color="black")
            screen.draw.filled_rect(Rect((bar_x, bar_y), (bar_width, bar_height)), "gray")
            screen.draw.filled_rect(Rect((bar_x, bar_y), (fill_width, bar_height)), prediction_color)
            screen.draw.rect(Rect((bar_x, bar_y), (bar_width, bar_height)), "black")

    if counter == "Home":
        counter = False
    
    if counter == "Tutorial":
        print_tutorial(screen, images)

# for all collisions
def on_mouse_down(pos):
    global counter, button_pressed, timer_on, games_submenu
    if challengebutton.collidepoint(pos):
        challengeaction()
        #games_submenu = True
        return
    if speedshotbutton.collidepoint(pos) and counter == True:
        counter = "Speed Shot"
        timer_on = True
        start_speedshot()
        sys.exit()
    if gamesbutton.collidepoint(pos):
        counter = "Games"
        start_game()
        sys.exit()
    if homebutton.collidepoint(pos):
        counter = "Home"
    if fastfootworkbutton.collidepoint(pos):
        counter = "Fast Footwork"
    if tutorialbutton.collidepoint(pos):
        counter = "Tutorial"

def on_key_down(key):
    global ballcounter, prediction_chance, prediction_color, prediction_timer
    global ballx
    global bally
    if key == keys.SPACE and ballcounter == False:
        ballx = random.uniform(6, 9)
        bally = random.uniform(-10, -13)
        ballcounter = True

         # Predict shot success based on simple angle
        

def resetball():
    global ballcounter
    ballcounter = False
    ball.x = player.x - 6
    ball.y = player.y

def decreasetimer():
    global timer
    timer -= 1

def startspeedshot():
    clock.schedule_interval(decreasetimer, 1.0)

#should always be last
def update():
    global counter, ballx, bally, speedshotscore, timer_on
    if counter == "Speed Shot" or counter == "Games":
        if timer_on == True:
            startspeedshot()
            timer_on = False
        updatespeedshot(keyboard, screen)
pgzrun.go()