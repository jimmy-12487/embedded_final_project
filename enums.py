from enum import Enum, IntEnum

class STATES(Enum):
    INIT = 0
    IDLE = 1
    MOVING = 2
    ATTACK = 3
    DEFEND = 4
    FORWARD = 5
    RETREAT = 6
    DIE = 7

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

class ATTACK_MOVEMENT(Enum):
    NONE = 0
    DEFEND = 1
    ATTACK1 = 2
    ATTACK2 = 3