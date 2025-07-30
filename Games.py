import pgzrun
import random
import sys
import subprocess
from pgzero.builtins import Actor, Rect, keyboard

WIDTH = 960
HEIGHT = 600

# Players
player1 = Actor("player", (300, 500))
ai_player = Actor("player_red", (600, 500))  # Changed to a different color sprite and closer position

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
righthoopbackboard = Rect((830, 230), (73, 35))

# Scores and timer
score_p1 = 0
score_p2 = 0
timer = 90


# Prediction UI
prediction_chance = 0.0
prediction_color = "gray"
prediction_timer = 0

# Game State
game_state = "home"

homebutton = Rect((40, 40), (140, 50))  # Add this near the top with other buttons

def startspeedshot():
    clock.schedule_interval(decrease_timer, 1.0)

def decrease_timer():
    global timer
    if timer > 0:
        timer -= 1

timer_on = True

def reset_ball(a):
    global ball_in_motion, ballx, bally
    #if ball_owner == 'player1':
       # ball.x = player1.x - 6
        #ball.y = player1.y
   # else:
        #ball.x = ai_player.x - 6
        #ball.y = ai_player.y
    ball.x = a.x
    ball.y = a.y
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
    #screen.draw.filled_rect(left_hoop, (0, 0, 0))
    #screen.draw.filled_rect(right_hoop, (0, 0, 0))
    #screen.draw.filled_rect(righthoopbackboard, (0,0,0))

    # Draw scores and timer
    screen.draw.text(f"P1 Score: {score_p1}", midtop=(200, 10), fontsize=30, color="black")
    screen.draw.text(f"AI Score: {score_p2}", midtop=(760, 10), fontsize=30, color="black")
    screen.draw.text(f"Timer: {timer}", center=(WIDTH//2, 40), fontsize=40, color="black")

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

    if timer == 0:
        if score_p1>score_p2:
            screen.draw.text("Player Wins!", center=(WIDTH//2, HEIGHT//2-40), fontsize=60, color="green")
        elif score_p1==score_p2:
            screen.draw.text("Draw!", center=(WIDTH//2, HEIGHT//2-40), fontsize=60, color="orange")
        else:
            screen.draw.text("AI Wins!", center=(WIDTH//2, HEIGHT//2-40), fontsize=60, color="red")
        screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

    # Draw Home button
    screen.draw.filled_rect(homebutton, "#baf3f7")
    screen.draw.text("Home", center=homebutton.center, color="black", fontsize=28)

def update():
    global ballx, bally, score_p1, score_p2, ball_owner, ball_in_motion, timer_on, prediction_timer
    if timer_on == True:
        startspeedshot()
        timer_on = False

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

    distance = ai_player.distance_to(player1)

    if ball.colliderect(righthoopbackboard):
        ballx = -ballx * 0.8
        ball.x += ballx
    # AI behavior
    if not ball_in_motion:
        if ball_owner == 'ai':
        # Move towards hoop if AI has the ball
            dx = left_hoop.centerx - ai_player.x
            dy = left_hoop.centery - ai_player.y
            distance_to_hoop = (dx**2 + dy**2) ** 0.5
            #if ai_player.x == 122.0 or ai_player.y == 390:
                #ai_player.x = random.random()
                #ai_player.y = random.random()
            if distance_to_hoop > 220:
                if abs(dx) > 5:
                    ai_player.x += 3 if dx > 0 else -3
                if abs(dy) > 5:
                    ai_player.y += 3 if dy > 0 else -3
            else:
                if random.random() < 0.02:
                    shoot_ai()
            dx_ai = player1.x - ai_player.x
            dy_ai = player1.y - ai_player.y
            distance_to_player = (dx_ai**2 + dy_ai**2) ** 0.5
            if distance_to_player < 60:
                if ai_player.x < player1.x:
                    ai_player.x -= 3
                elif ai_player.x > player1.x:
                    ai_player.x += 3
                if ai_player.y < player1.y:
                    ai_player.y -= 3
                elif ai_player.y > player1.y:
                    ai_player.y += 3
        else:
            # AI chases player1 if doesn't have the ball
            dx2 = right_hoop.centerx - player1.x
            dy2 = right_hoop.centery - player1.y
            distance_to_hoop = (dx2**2 + dy2**2) ** 0.5
            if distance_to_hoop != 0:
                ndx = dx2 / distance_to_hoop
                ndy = dy2 / distance_to_hoop
            else:
                ndx = 0
                ndy = 0
            offset = 70
            targetx = player1.x + ndx*offset
            targety = player1.y + ndy*offset

            if abs(ai_player.x - targetx) > 2:
                ai_player.x += 3 if ai_player.x < targetx else -3
            if abs(ai_player.y - targety) > 2:
                ai_player.y += 3 if ai_player.y < targety else -3

            #if ai_player.x < targetx:
                #ai_player.x += 3
            #elif ai_player.x > targetx:
                #ai_player.x -= 3
            #if ai_player.y < targety:
                #ai_player.y += 3
            #elif ai_player.y > targety:
                #ai_player.y -= 3

    # Steal ball if close enough
    if not ball_in_motion and ball_owner == 'player1' and distance < 30:
        ball_owner = 'ai'

    # Player steal back from AI
    if not ball_in_motion and ball_owner == 'ai' and distance < 30 and keyboard.LSHIFT:
        ball_owner = 'player1'

    # AI shooting logic
    if not ball_in_motion and ball_owner == 'ai':
        if random.random() < 0.02:
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
            ball.x = player1.x - 6
            ball.y = player1.y
            reset_ball(player1)
            ball_owner = 'player1'
        elif ball.colliderect(right_hoop) and ball_owner == 'player1':
            score_p1 += 1
            ball.x = ai_player.x - 6
            ball.y = ai_player.y
            reset_ball(ai_player)
            ball_owner = 'ai'
        elif ball.y > HEIGHT or ball.x < 0 or ball.x > WIDTH:
            if ball_owner == 'player1':
                reset_ball(ai_player)
                ball_owner = 'ai'
            else:
                reset_ball(player1)
                ball_owner = 'player1'


def on_key_down(key):
    global ball_in_motion, ballx, bally, ball_owner, prediction_chance, prediction_color, prediction_timer
    if key == keys.SPACE and not ball_in_motion and ball_owner == 'player1':
        ballx = random.uniform(6, 9)
        bally = random.uniform(-10, -13)
        ball_in_motion = True
    # Predict shot success based on simple angle
        distance_to_hoop = ((player1.x - right_hoop.centerx)**2 + (player1.y - right_hoop.centery)**2) ** 0.5
        prediction_chance = max(0, min(1, 1 - (distance_to_hoop / 600)))
        if prediction_chance > 0.75:
            prediction_color = "green"
        elif prediction_chance > 0.4:
            prediction_color = "yellow"
        else:
            prediction_color = "red"
        prediction_timer = 60 

def shoot_ai():
    global ball_in_motion, ballx, bally, ball_owner
    if not ball_in_motion:
        ballx = random.uniform(-9, -6)
        bally = random.uniform(-10, -13)
        ball_in_motion = True

def on_mouse_down(pos):
    if homebutton.collidepoint(pos):
        # Relaunch Main.py and close this window
        subprocess.Popen(["pgzrun", "Main.py"])
        sys.exit()
    # ...add any other mouse handling here if needed...
