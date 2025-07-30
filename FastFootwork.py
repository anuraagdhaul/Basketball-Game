import random

def start_fastfootwork(state):
    state['timer'] = 90
    state['fastfootwork_score'] = 0
    radius = state['fastfootwork_radius']
    min_x = 100 + radius
    max_x = 860 - radius
    min_y = 406 + radius
    max_y = state['HEIGHT'] - radius
    state['fastfootwork_circle'] = (random.randint(min_x, max_x), random.randint(min_y, max_y))

def draw_fastfootwork(screen, player, state, homebutton):
    x, y = state['fastfootwork_circle']
    radius = state['fastfootwork_radius']
    # Draw shadow
    screen.draw.circle((x, y + 5), radius, (120, 120, 120))
    # Draw thick blue rim
    for i in range(4):
        screen.draw.circle((x, y), radius - i, (30, 144, 255))
    # Net effect
    net_height = 12
    net_color = (220, 220, 220)
    for i in range(-2, 3):
        screen.draw.line((x + i*4, y + radius), (x + i*2, y + radius + net_height), net_color)
    screen.draw.line((x - radius//2, y + radius + net_height//2),
                     (x + radius//2, y + radius + net_height//2), net_color)
    player.draw()
    screen.draw.text(f"Score: {state['fastfootwork_score']}", center=(state['WIDTH'] // 2, 130), color="black", fontsize=40)
    screen.draw.text(f"Timer: {state['timer']}", center=(state['WIDTH'] // 2, 170), color="black", fontsize=40)
    screen.draw.filled_rect(homebutton, "#baf3f7")
    screen.draw.text("Home", center=homebutton.center, color="black", fontsize=28)

def logic_for_fastfootwork(player, state):
    radius = state['fastfootwork_radius']
    min_x = 100 + radius
    max_x = 860 - radius
    min_y = 406 + radius
    max_y = state['HEIGHT'] - radius
    x, y = state['fastfootwork_circle']
    dx = player.x - x
    dy = player.y - y
    dist = (dx**2 + dy**2) ** 0.5
    if dist < radius + 40:
        state['fastfootwork_score'] += 1
        state['points'] += 2
        state['fastfootwork_circle'] = (random.randint(min_x, max_x), random.randint(min_y, max_y))

