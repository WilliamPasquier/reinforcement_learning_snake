from enum import Enum

class Network(Enum):
    INPUT = 11
    HIDDEN = 256
    OUTPUT = 3

class Memory(Enum):
    MAX_MEMORY = 100_000
    BATCH_SIZE = 1000
    LEARNING_RATE = 0.001
