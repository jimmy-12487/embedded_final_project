from enum import Enum, IntEnum

class STATES(Enum):
    INIT = 0
    IDLE = 1
    MOVING = 2
    ATTACK1 = 3
    ATTACK2 = 4
    DEFEND = 5

class DIRECTION(Enum):
    STILL = 0
    LEFT = 1
    RIGHT = 2
    
class GAME_STATE(IntEnum):
    SAY_START = 0
    READY = 1
    PLAYING = 2

class VOICE(IntEnum):
    START = 0
    CHICK = 1
    DINO = 2
    READY = 3

class MOVEMENT(Enum):
    DEFEND = 0
    ATTACK1 = 1
    ATTACK2 = 2