import pygame
import random
import pgzrun
import subprocess
import sys
from Tutorial import print_tutorial

WIDTH = 960
HEIGHT = 600
counter = False  # keeps track of button click
player = Actor("player", (480, 550))


# Hoops
left_hoop = Rect((90, 270), (70, 15))
right_hoop = Rect((800, 270), (70, 15))
righthoopbackboard = Rect((830, 230), (73, 35))

fastfootwork_score = 0
fastfootwork_circle = None  # (x, y)
fastfootwork_radius = 20  # Radius of the circle

# Ball setup
ball = Actor("ball")
ball.x = player.x - 6
ball.y = player.y
ballcounter = False
ball_who = 'player'
ballx = 0
bally = 0
gravity = 0.3

# Prediction UI
prediction_chance = 0.0
prediction_color = "gray"
prediction_timer = 0

button_pressed = False
timer = 90
timer_on = False
games_submenu = False

points = 0
points_log = []


def challengeaction():
    global counter
    counter = True


challengebutton = Rect((380, 250), (200, 60))
gamesbutton = Rect((380, 340), (200, 60))
rankingbutton = Rect((380, 430), (200, 60))
pointsbutton = Rect((380, 520), (200, 50))
tutorialbutton = Rect((780, 40), (140, 50))
homebutton = Rect((40, 40), (140, 50))
tryaginbutton = Rect((780, 40), (140, 50))
accountbutton = Rect((780, 40), (140, 50))
righthoop = Rect((800, 270), (70, 15))
speedshotscore = 0



speedshotbutton = Rect((170, 220), (250, 140))
fastfootworkbutton = Rect((540, 220), (250, 140))
dogbutton = Rect((360, 420), (250, 140))

def start_fastfootwork():
    global timer, fastfootwork_score, fastfootwork_circle
    reset_game_state()
    timer = 90
    fastfootwork_score = 0
    # Player boundaries: left=100, right=860, top=406, bottom=HEIGHT
    min_x = 100 + fastfootwork_radius
    max_x = 860 - fastfootwork_radius
    min_y = 406 + fastfootwork_radius
    max_y = HEIGHT - fastfootwork_radius
    fastfootwork_circle = (random.randint(min_x, max_x), random.randint(min_y, max_y))
    startspeedshot()  # reuse timer logic

def draw_fastfootwork():
    global fastfootwork_circle, fastfootwork_score
    # Draw the circle
    if fastfootwork_circle:
        screen.draw.filled_circle(fastfootwork_circle, fastfootwork_radius, "blue")
    # Draw player and UI
    player.draw()
    screen.draw.text(f"Score: {fastfootwork_score}", center=(WIDTH // 2, 130), color="black", fontsize=40)
    screen.draw.text(f"Timer: {timer}", center=(WIDTH // 2, 170), color="black", fontsize=40)
    # Home button
    screen.draw.filled_rect(homebutton, "#baf3f7")
    screen.draw.text("Home", center=homebutton.center, color="black", fontsize=28)

def logicForFastFootwork():
    global fastfootwork_circle, fastfootwork_score, points
    min_x = 100 + fastfootwork_radius
    max_x = 860 - fastfootwork_radius
    min_y = 406 + fastfootwork_radius
    max_y = HEIGHT - fastfootwork_radius
    if fastfootwork_circle:
        dx = player.x - fastfootwork_circle[0]
        dy = player.y - fastfootwork_circle[1]
        dist = (dx**2 + dy**2) ** 0.5
        if dist < fastfootwork_radius + 40:
            fastfootwork_score += 1
            points += 2
            fastfootwork_circle = (random.randint(min_x, max_x), random.randint(min_y, max_y))


def reset_game_state():
    global timer, speedshotscore, ballcounter, ballx, bally, prediction_chance, prediction_color, prediction_timer, timer_on
    timer = 90
    speedshotscore = 0
    ballcounter = False
    ballx = 0
    bally = 0
    prediction_chance = 0.0
    prediction_color = "gray"
    prediction_timer = 0
    timer_on = False

state = {
    'WIDTH': WIDTH,
    'HEIGHT': HEIGHT,
    'timer': timer,
    'fastfootwork_score': fastfootwork_score,
    'fastfootwork_circle': fastfootwork_circle,
    'fastfootwork_radius': fastfootwork_radius,
    'points': points,
    'speedshotscore': speedshotscore,
}

def draw():
    global counter, speedshotscore, button_pressed, timer_on, points, points_log
    screen.clear()
    screen.fill((249, 246, 232))
    screen.blit(images.court2, (0, 180))

    if counter == "Tutorial":
        print_tutorial(screen, images)
        return

    if counter == "Points Log":
        screen.draw.text("Points Log", center=(WIDTH//2, 60), color="black", fontsize=48)
        y = 120
        for entry in points_log[-10:][::-1]:  # Show last 10 entries, newest first
            screen.draw.text(entry, topleft=(100, y), color="black", fontsize=32)
            y += 40
        # Back button
        screen.draw.filled_rect(homebutton, "#baf3f7")
        screen.draw.text("Back", center=homebutton.center, color="black", fontsize=28)
        return

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

        # Account button
        screen.draw.filled_rect(accountbutton, "#baf3f7")
        screen.draw.text("Account", center=accountbutton.center, color="black", fontsize = 28)

        # Tutorial button
        screen.draw.filled_rect(tutorialbutton, "#baf3f7")
        screen.draw.text("Tutorial", center=tutorialbutton.center, color="black", fontsize = 28)

        # Player
        original = images.player  # no .png
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

    if counter == "Speed Shot":
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
            #counter = True
            timer_on = False
            screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2-40), fontsize=60, color="red")
            if(speedshotscore>=30):
                screen.draw.text("Well done!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="green")
                screen.draw.text("You’ve completed the challenge.", center=(WIDTH//2, HEIGHT//2+40), fontsize=60, color="green")
                if not hasattr(draw, "speed_shot_logged"):
                    points += 40
                    points_log.append("Speed Shot: 40")
                    draw.speed_shot_logged = True
            else:
                screen.draw.text("Challenge Failed.", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
                # Draw Try Again button
                screen.draw.filled_rect(tryaginbutton, "#baf3f7")
                screen.draw.text("Try Again", center=tryaginbutton.center, color="black", fontsize=28)
        logicForSpeedShot()

    if counter == "Fast Footwork":
        if timer == 0:
            screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2-40), fontsize=60, color="red")
            screen.draw.text(f"Score: {fastfootwork_score}", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="black")
            # Log points only once at the end
            if not hasattr(draw, "fastfootwork_logged"):
                if fastfootwork_score > 0:
                    points_log.append(f"Fast Footwork: {fastfootwork_score * 2}")
                draw.fastfootwork_logged = True
            # Home button
            screen.draw.filled_rect(homebutton, "#baf3f7")
            screen.draw.text("Home", center=homebutton.center, color="black", fontsize=28)
        else:
            # Reset the log flag when challenge is running
            if hasattr(draw, "fastfootwork_logged"):
                del draw.fastfootwork_logged
            draw_fastfootwork()
            logicForFastFootwork()

    if counter == "Home":
        reset_game_state()
        counter = False
    
    if counter == "Try Again":
        reset_game_state()
        counter = "Speed Shot"


   
# for all collisions
def on_mouse_down(pos):
    global counter, button_pressed, timer_on, games_submenu
    if challengebutton.collidepoint(pos):
        challengeaction()
        return
    if speedshotbutton.collidepoint(pos) and counter == True:
        counter = "Speed Shot"
        reset_game_state()
        startspeedshot()
    if fastfootworkbutton.collidepoint(pos) and counter == True:
        counter = "Fast Footwork"
        start_fastfootwork()
    if gamesbutton.collidepoint(pos):
        counter = "Games"
        subprocess.Popen(["pgzrun", "Games.py"])  # launch MainG
        sys.exit()  # close Main2 window
    if homebutton.collidepoint(pos):
        counter = "Home"
    if tryaginbutton.collidepoint(pos) and counter == "Speed Shot" and timer == 0:
        reset_game_state()
        counter = "Speed Shot"
        startspeedshot()
    if pointsbutton.collidepoint(pos) and counter == False:
        counter = "Points Log"
    if homebutton.collidepoint(pos) and counter == "Points Log":
        counter = False
    if tutorialbutton.collidepoint(pos) and counter == False:
        counter = "Tutorial"
        return
    if homebutton.collidepoint(pos) and counter == "Tutorial":
        counter = False
        return

def on_key_down(key):
    global ballcounter
    global ballx
    global bally, prediction_chance, prediction_color, prediction_timer
    if key == keys.SPACE and ballcounter == False:
        ballx = random.uniform(6, 9)
        bally = random.uniform(-10, -13)
        ballcounter = True
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

def resetball():
    global ballcounter
    ballcounter = False
    ball.x = player.x - 6
    ball.y = player.y

def decreasetimer():
    global timer
    if timer > 0:
        timer -= 1

def startspeedshot():
    clock.unschedule(decreasetimer)  # Stop any previous timer
    clock.schedule_interval(decreasetimer, 1.0)

def logicForSpeedShot():
    global counter, speedshotscore, button_pressed,timer_on
    player.draw()
    ball.draw()
    screen.draw.filled_rect(righthoop, (0, 0, 0))
    screen.draw.text("Score: " + str(speedshotscore), center=(WIDTH // 2, 130), color="black", fontsize=40)
    screen.draw.text("Timer: " + str(timer), center = (WIDTH // 2, 170), color="black", fontsize=40)
    # Home button
    screen.draw.filled_rect(homebutton, "#baf3f7")
    screen.draw.text("Home", center=homebutton.center, color="black", fontsize = 28) 

#should always be last
def update():
    global counter, ballx, bally, speedshotscore, timer_on
    if counter == "Speed Shot" or counter == "Games":
        if keyboard.up:
            player.y -= 3
        if keyboard.down:
            player.y += 3
        if keyboard.left:
            player.x -= 3
        if keyboard.right:
            player.x += 3
        # Keep player in bounds (same as Fast Footwork)
        if player.bottom < 406:
            player.bottom = 406
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
        if player.left < 100:
            player.left = 100
        if player.right > 860:
            player.right = 860
        if ball.colliderect(righthoopbackboard):
            ballx = -ballx * 0.8
            ball.x += ballx
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
    if counter == "Fast Footwork":
        # Player movement only
        if keyboard.up:
            player.y -= 3
        if keyboard.down:
            player.y += 3
        if keyboard.left:
            player.x -= 3
        if keyboard.right:
            player.x += 3

        # Keep player in bounds
        if player.bottom < 406:
            player.bottom = 406
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT
        if player.left < 100:
            player.left = 100
        if player.right > 860:
            player.right = 860

pgzrun.go()