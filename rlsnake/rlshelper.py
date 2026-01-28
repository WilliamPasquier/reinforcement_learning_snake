from enum import Enum

class Settings(Enum):
    '''
    Application settings
    Can toggle features
    '''
    PLOT_DATA = False
    SAVE_MODEL = False 
    MODEL_PATH = './model'
    DISPLAY_INFO = True
    DISPLAY_SENSOR = False