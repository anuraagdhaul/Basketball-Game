# Write your code here :-)
import pygame
import random
import pgzrun
#from MainG import 

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


def challengeaction():
    global counter
    counter = True


challengebutton = Rect((130, 250), (200, 60))
customizebutton = Rect((130, 390), (200, 60))
gamesbutton = Rect((360, 250), (200, 60))
rankingbutton = Rect((360, 455), (200, 45))
pointsbutton = Rect((360, 390), (200, 50))
accountbutton = Rect((780, 40), (140, 50))
tutorialbutton = Rect((40, 40), (140, 50))
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

        # Customize button
        screen.draw.filled_rect(customizebutton, "#fdb8b2")
        screen.draw.text("Customize", center=customizebutton.center, color="black", fontsize=28)

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
        original = images.player_copy  # no .png
        resized = pygame.transform.scale(original, (75, 180))
        screen.blit(resized, (650, 250))


    if  counter == True:
        screen.draw.filled_rect(speedshotbutton, "#990F02")
        screen.draw.text("Speed Shot\n\nMake 30 baskets in 90 seconds", center=speedshotbutton.center, color="white")
        #screen.draw.text(, center = (200, 150), fontsize = 30, color="white")


        screen.draw.filled_rect(fastfootworkbutton, "#960019")
        screen.draw.text("Fast Footwork", center=fastfootworkbutton.center, color="white")

        screen.draw.filled_rect(dogbutton, "#960019")
        screen.draw.text("D.O.G", center=dogbutton.center, color="white")

        screen.draw.text("Choose a challenge and try to earn some points!", center=(WIDTH // 2, 130), color="black", fontsize=40)

        if timer == 0:
            counter = True


    if counter == "Speed Shot":
        player.draw()
        ball.draw()
        screen.draw.filled_rect(righthoop, (0, 0, 0))
        screen.draw.text("Score: " + str(speedshotscore), center=(WIDTH // 2, 130), color="black", fontsize=40)
        screen.draw.text("Timer: " + str(timer), center = (WIDTH // 2, 170), color="black", fontsize=40)

   
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
    if gamesbutton.collidepoint(pos):
        counter = "Games"


def on_key_down(key):
    global ballcounter
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

pgzrun.go()