from enum import Enum, IntEnum

class STATES(Enum):
    INIT = 0
    IDLE = 1
    MOVING = 2
    ATTACK = 3
    DEFENDING = 4
    FORWARD = 5
    RETREAT = 6
    DIE = 7
    DONE = -1
    
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
    DEFEND = 4
    ATTACK1 = 5
    ATTACK2 = 6

class ATTACK_MOVEMENT(Enum):
    NONE = 0
    DEFENDING = 1
    ATTACK1 = 2 # fire
    ATTACK2 = 3 # rush
    
class INTERACTION_RESPONSE(Enum):
    NONE = 0
    FORWARD_NOT_COLLIDE = 1
    FORWARD_AND_COLLIDE = 2
    ATTACK1 = 3
    ATTACK2 = 4
    RETREAT_NOT_GO_BACK = 5
    RETREAT_AND_GO_BACK = 6
    DEFEND = 7