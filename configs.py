# game environment configs
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = (255, 255, 255)
ROLE_NUMBER = 2
WALL_OFFSET = 100
FONT_SIZE = 150
DAMAGE_TICKS_PER_FRAME = 20

# chicken configs

CHICKEN_WIDTH = 300
CHICKEN_HEIGHT = 300

CHICKEN_RUSH_WIDTH = 300
CHICKEN_RUSH_HEIGHT = 180

CHICKEN_EGG_WIDTH = 150
CHICKEN_EGG_HEIGHT = 200

CHICKEN_INIT_POSITION = {
    'LEFT': {
        'X': WALL_OFFSET,
        'Y': WINDOW_HEIGHT - CHICKEN_HEIGHT - WALL_OFFSET
    },
    'RIGHT': {
        'X': WINDOW_WIDTH - CHICKEN_WIDTH - WALL_OFFSET,
        'Y': WINDOW_HEIGHT - CHICKEN_WIDTH - WALL_OFFSET
    }
}

# dinosaur configs

DINO_WIDTH = 450
DINO_HEIGHT = 450

DINO_INIT_POSITION = {
    'LEFT': {
        'X': WALL_OFFSET,
        'Y': WINDOW_HEIGHT - DINO_HEIGHT - WALL_OFFSET
    },
    'RIGHT': {
        'X': WINDOW_WIDTH - DINO_WIDTH - WALL_OFFSET,
        'Y': WINDOW_HEIGHT - DINO_HEIGHT - WALL_OFFSET
    }
}

DINO_SCRATCH_WIDTH = 300
DINO_SCRATCH_HEIGHT = 180

DINO_FIRE_WIDTH = 600
DINO_FIRE_HEIGHT = 360

# ready scene
AVAIABLE_ICON_SIZE = 150

# playing scene
DEFEND_WIDTH = 300
DEFEND_HEIGHT = 500

TICKS_PER_FRAME = 20 # ticks to go next state
TICKS_PER_MOVEMENT = 2
MOVEMENT_SPEED = 5
RETREAT_SPEED_OFFSET = 5


HEALTH_BAR_ICON_SIZE = 160
HEALTH_BAR_HIEGHT = 80
HEALTH_BAR_WIDTH = 600

HEALTH_BAR_OFFSET = 55

HEALTH_BAR_POSITION = {
    'LEFT': {
        'X': HEALTH_BAR_ICON_SIZE - HEALTH_BAR_OFFSET,
        'Y': 0
    },
    'RIGHT': {
        'X': WINDOW_WIDTH - HEALTH_BAR_ICON_SIZE - HEALTH_BAR_WIDTH + HEALTH_BAR_OFFSET,
        'Y': 0
    }
}

HEALTH_BAR_ICON_POSITION = {
    'LEFT': {
        'X': 0,
        'Y': 0,
    },
    'RIGHT': {
        'X': WINDOW_WIDTH - HEALTH_BAR_ICON_SIZE,
        'Y': 0
    }
}