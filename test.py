# Write your code here :-)


WIDTH = 960
HEIGHT = 720
counter = False
def challengeaction ():
    global counter
    counter = True

challengebutton = Rect((150,120),(200,50))
def draw ():
    global counter
    screen.clear()
    screen.fill((200,200,255))
    screen.blit(images.court2, (0,300))
    screen.draw.filled_rect(challengebutton, "white")
    screen.draw.text("Challenges",center = challengebutton.center, color = "black")
    if counter:
        screen.draw.text("Welcome to Number Count!", center=(WIDTH/2, 150), fontsize=50, color=(255, 255,255))



def on_mouse_down(pos):
    if challengebutton.collidepoint (pos):
        challengeaction()

def update():
    pass
