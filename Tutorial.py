import pgzrun
from pgzero.builtins import Rect  # <-- Add this line

WIDTH = 960
HEIGHT = 600

show_popup = False

counter = False


    # to adjust size, go to image, go to tools, and manually resize image

def print_tutorial(screen, images):
    homebutton = Rect((40, 40), (140, 50))
    screen.clear()
    screen.fill((249, 246, 232))

    screen.draw.text("Tutorial", center=(WIDTH//2, 80), fontsize=40, color="black")
    screen.draw.text("To control the blue player in any of the sections, \n \n use the Arrow Keys.", center = (350, 183), fontsize = 30, color = "black")
    screen.blit(images.arrowkeys2, (650,85))
    screen.draw.text("To shoot the ball, press the space bar. In the Games section, to steal the ball from \n \n the bot, press the shift button.", center=(460, 320), fontsize = 30, color = "black")
    screen.blit(images.spacebar, (350, 377))
    screen.blit(images.shiftkey2, (500, 360))
    screen.draw.text("Make sure to complete as many challenges and win as many game as you can. \n \n This will give you a higher points score and increase your ranking.", center = (467, 520), fontsize = 30, color = "black")

    # Draw Home button
    screen.draw.filled_rect(homebutton, "#baf3f7")
    screen.draw.text("Home", center=homebutton.center, color="black", fontsize=28)

def on_key_down(key):
    global show_popup
    if key == keys.SPACE:
        show_popup = True
    #if homebutton.collidepoint(pos):
       # counter = False

def on_mouse_down(pos):
    global show_popup
    if show_popup:
        show_popup = False

pgzrun.go()