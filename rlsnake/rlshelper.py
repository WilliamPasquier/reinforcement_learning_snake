from enum import Enum

class Settings(Enum):
    '''
    Application settings
    Can toggle features
    '''
    PLOT_DATA = False
    SAVE_MODEL = True 
    MODEL_PATH = './model'
    DISPLAY_INFO = False
    DISPLAY_SENSOR = False