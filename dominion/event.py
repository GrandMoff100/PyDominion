from enum import Enum


class Event(Enum):
    DRAW_EVENT = 1
    BUY_EVENT = 2
    TRASH_EVENT = 3
    DISCARD_EVENT = 4
    GAIN_EVENT = 5
    ATTACK_EVENT = 6
    REVEAL_EVENT = 7
