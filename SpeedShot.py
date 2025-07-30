def logic_for_speedshot(player, ball, righthoop, state, screen, homebutton):
    player.draw()
    ball.draw()
    screen.draw.filled_rect(righthoop, (0, 0, 0))
    screen.draw.text("Score: " + str(state['speedshotscore']), center=(state['WIDTH'] // 2, 400), color="black", fontsize=40)
    screen.draw.text("Timer: " + str(state['timer']), center = (state['WIDTH'] // 2, 400), color="black", fontsize=40)
    screen.draw.filled_rect(homebutton, "#baf3f7")
    screen.draw.text("Home", center=homebutton.center, color="black", fontsize = 28)