from pathlib import Path

# basic settings
FPS = 60
SCREEN_SIZE = (1280, 720)

# path settings
BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = Path.joinpath(BASE_PATH, 'Assets')
PARTICLES_PATH = Path.joinpath(ASSETS_PATH, 'Particles')
PLAYER_PATH = Path.joinpath(ASSETS_PATH, 'Characters', 'Player')
PLAYER_MASK_DUDE_PATH = Path.joinpath(PLAYER_PATH, 'MaskDude')
PLAYER_VIRTUAL_GUY_PATH = Path.joinpath(PLAYER_PATH, 'VirtualGuy')
PLAYER_ANIMATION_PATH = Path.joinpath(PLAYER_PATH, 'animations')
PLAYER_PARTICLES_PATH = Path.joinpath(PARTICLES_PATH, 'PlayerParticles')


# level setting
LEVEL_MAP = [
    '                            ',
    '                            ',
    '                            ',
    '       XXXX           XX    ',
    '   P                        ',
    'XXXXX         XX         XX ',
    ' XXXX       XX              ',
    ' XX    X  XXXX    XX  XX    ',
    '       X  XXXX    XX  XXX   ',
    '    XXXX  XXXXXX  XX  XXXX  ',
    'XXXXXXXX  XXXXXX  XX  XXXX  ',
]

TILE_SIZE = 64

# colors
BG_COLOR = '#060C17'
PLAYER_COLOR = '#C4F7FF'
TILE_COLOR = '#94D7F2'

# camera settings
CAMERA_BORDERS = {'left': 100, 'right': 200, 'top': 100, 'bottom': 150}
