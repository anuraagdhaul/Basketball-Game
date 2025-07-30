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
button_pressed = False
timer = 90
timer_on = False
games_submenu = False
righthoop = Rect((800, 270), (70, 15))
righthoopbackboard = Rect((800, 290), (70, 40))
speedshotscore = 0

# Hoop challenge setup
hoop_radius = 30
initial_hoops = 3
hoop_pos = []
visited_hoops = []
score = 0
message = ""
message_timer = 0

def reset_hoops(count):
    global hoop_pos, visited_hoops
    hoop_pos = [
        (random.randint(hoop_radius, WIDTH - hoop_radius),
         random.randint(hoop_radius, HEIGHT - hoop_radius))
        for _ in range(count)
    ]
    visited_hoops = [False] * count

reset_hoops(initial_hoops)

def fastfootworkdraw(screen):
    player.draw() 
    screen.draw.filled_rect(righthoop, (0, 0, 0))
    # Draw hoops
    for i, (x, y) in enumerate(hoop_pos):
        color = "green" if visited_hoops[i] else "red"
        screen.draw.circle((x, y), hoop_radius, color=color)
    screen.draw.text("Score: " + str(speedshotscore), center=(WIDTH // 2, 130), color="black", fontsize=40)
    screen.draw.text("Timer: " + str(timer), center = (WIDTH // 2, 170), color="black", fontsize=40)

def on_key_down(key):
    print("hi")

def updatefastfootwork(keyboard, screen):
        global counter, speedshotscore, timer_on
        if keyboard.up:
            player.y -= 3
        if keyboard.down:
            player.y += 3
        if keyboard.left:
            player.x -= 3
        if keyboard.right:
            player.x += 3

        if player.bottom < 406:
            player.bottom = 406
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
        if player.left < 100:
            player.left = 100
        if player.right > 860:
            player.right = 860


