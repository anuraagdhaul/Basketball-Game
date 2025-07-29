import pygame
import random
import pgzrun
import Games
import subprocess
import sys
from pgzero.builtins import Actor, Rect

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
righthoop = Rect((800, 270), (70, 15))
righthoopbackboard = Rect((800, 290), (70, 40))
speedshotscore = 0
ball_owner = 'player'
ball_in_motion = False

# Prediction UI
prediction_chance = 0.0
prediction_color = "gray"
prediction_timer = 0

def on_key_down(key):
    global ball_in_motion, ballx, bally, ball_owner, prediction_chance, prediction_color, prediction_timer
    if key == keys.RETURN and not ball_in_motion and ball_owner == 'player':
        ballx = random.uniform(6, 9)
        bally = random.uniform(-10, -13)
        ball_in_motion = True
    # Predict shot success based on simple angle
        distance_to_hoop = ((player.x - right_hoop.centerx)**2 + (player.y - right_hoop.centery)**2) ** 0.5
        prediction_chance = max(0, min(1, 1 - (distance_to_hoop / 600)))
        if prediction_chance > 0.75:
            prediction_color = "green"
        elif prediction_chance > 0.4:
            prediction_color = "yellow"
        else:
            prediction_color = "red"
        prediction_timer = 60

def speedshotdraw(screen):
    player.draw()
    ball.draw()
    screen.draw.filled_rect(righthoop, (0, 0, 0))
    screen.draw.text("Score: " + str(speedshotscore), center=(WIDTH // 2, 130), color="black", fontsize=40)
    screen.draw.text("Timer: " + str(timer), center = (WIDTH // 2, 170), color="black", fontsize=40)

def on_key_down(key):
    global ballcounter, prediction_chance, prediction_color, prediction_timer
    global ballx
    global bally
    if key == keys.SPACE and ballcounter == False:
        ballx = random.uniform(6, 9)
        bally = random.uniform(-10, -13)
        ballcounter = True

def resetball():
    global ballcounter
    ballcounter = False
    ball.x = player.x - 6
    ball.y = player.y

def updatespeedshot(keyboard, screen):
        global counter, ballx, bally, speedshotscore, timer_on
        if keyboard.up:
            player.y -= 3
        if keyboard.down:
            player.y += 3
        if keyboard.left:
            player.x -= 3
        if keyboard.right:
            player.x += 3
        if ballcounter == False:
            ball.x = player.x - 6
            ball.y = player.y
        if ballcounter == True:
            ball.x += ballx
            ball.y += bally
            bally += gravity
            if ball.colliderect(righthoop):
                speedshotscore += 1
                resetball()
            if ball.y > HEIGHT or ball.x > WIDTH:
                resetball()

        if player.bottom < 406:
            player.bottom = 406
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
        if player.left < 100:
            player.left = 100
        if player.right > 860:
            player.right = 860

        if not ball_in_motion:
            if ball_owner == 'player':
                ball.x = player.x - 6
                ball.y = player.y
            else:
                ball.x = ai_player.x - 6
                ball.y = ai_player.y
        else:
            ball.x += ballx
            ball.y += bally
            bally += gravity