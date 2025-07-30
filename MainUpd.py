# Write your code here :-)
# AI Player Basketball Game in Pygame Zero with Ball Stealing and Smarter AI
import pygame
import random
from pgzero.builtins import Actor, Rect, keyboard

WIDTH = 960
HEIGHT = 600

# Players
player1 = Actor("player_copy", (300, 500))
ai_player = Actor("player_red", (660, 500))  # Changed to a different color sprite

# Ball setup
ball = Actor("ball")
ball.x = player1.x - 6
ball.y = player1.y
ball_in_motion = False
ball_owner = 'player1'
ballx = 0
bally = 0
gravity = 0.3

# Hoops
left_hoop = Rect((90, 270), (70, 15))
right_hoop = Rect((800, 270), (70, 15))

# Scores and timer
score_p1 = 0
score_p2 = 0
timer = 90

# Game State
game_state = "home"

# Start timer
clock.schedule_interval(lambda: decrease_timer(), 1.0)

def decrease_timer():
    global timer
    if timer > 0:
        timer -= 1

def reset_ball():
    global ball_in_motion, ballx, bally
    if ball_owner == 'player1':
        ball.x = player1.x - 6
        ball.y = player1.y
    else:
        ball.x = ai_player.x - 6
        ball.y = ai_player.y
    ball_in_motion = False
    ballx = 0
    bally = 0

def draw():
    screen.clear()
    screen.fill((249, 246, 232))
    screen.blit("court2", (0, 180))

    # Draw players and ball
    player1.draw()
    ai_player.draw()
    ball.draw()

    # Draw hoops
    screen.draw.filled_rect(left_hoop, (0, 0, 0))
    screen.draw.filled_rect(right_hoop, (0, 0, 0))

    # Draw scores and timer
    screen.draw.text(f"P1 Score: {score_p1}", midtop=(200, 10), fontsize=30, color="black")
    screen.draw.text(f"AI Score: {score_p2}", midtop=(760, 10), fontsize=30, color="black")
    screen.draw.text(f"Timer: {timer}", center=(WIDTH//2, 40), fontsize=40, color="black")

    if timer == 0:
        screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

def update():
    global ballx, bally, score_p1, score_p2, ball_owner, ball_in_motion

    if timer <= 0:
        return

    # Player 1 movement (arrow keys)
    if keyboard.left:
        player1.x -= 4
    if keyboard.right:
        player1.x += 4
    if keyboard.up:
        player1.y -= 4
    if keyboard.down:
        player1.y += 4

    # AI follows player1 but keeps distance
    distance = ai_player.distance_to(player1)
    if distance > 100:
        if ai_player.x < player1.x:
            ai_player.x += 2
        elif ai_player.x > player1.x:
            ai_player.x -= 2
        if ai_player.y < player1.y:
            ai_player.y += 2
        elif ai_player.y > player1.y:
            ai_player.y -= 2

    # Steal ball if close enough
    if not ball_in_motion and ball_owner == 'player1' and distance < 50:
        ball_owner = 'ai'

    # Player steal back from AI
    if not ball_in_motion and ball_owner == 'ai' and distance < 50 and keyboard.LSHIFT:
        ball_owner = 'player1'

    # AI shooting logic
    if not ball_in_motion and ball_owner == 'ai':
        if random.random() < 0.01:
            shoot_ai()

    # Keep players within bounds
    for p in [player1, ai_player]:
        if p.left < 100: p.left = 100
        if p.right > 860: p.right = 860
        if p.bottom < 406: p.bottom = 406
        if p.bottom > HEIGHT: p.bottom = HEIGHT

    # Ball motion
    if not ball_in_motion:
        if ball_owner == 'player1':
            ball.x = player1.x - 6
            ball.y = player1.y
        else:
            ball.x = ai_player.x - 6
            ball.y = ai_player.y
    else:
        ball.x += ballx
        ball.y += bally
        bally += gravity

        if ball.colliderect(left_hoop) and ball_owner == 'ai':
            score_p2 += 1
            reset_ball()
        elif ball.colliderect(right_hoop) and ball_owner == 'player1':
            score_p1 += 1
            reset_ball()
        elif ball.y > HEIGHT or ball.x < 0 or ball.x > WIDTH:
            reset_ball()

def on_key_down(key):
    global ball_in_motion, ballx, bally, ball_owner
    if key == keys.RETURN and not ball_in_motion and ball_owner == 'player1':
        ballx = random.uniform(6, 9)
        bally = random.uniform(-10, -13)
        ball_in_motion = True

def shoot_ai():
    global ball_in_motion, ballx, bally, ball_owner
    if not ball_in_motion:
        ballx = random.uniform(-9, -6)
        bally = random.uniform(-10, -13)
        ball_in_motion = True
