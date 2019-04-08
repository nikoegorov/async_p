from os import path

from animations_code.load_animations_frames import load_animations_from_folder

# Keyboard codes
SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258

# Time (tick) of each display refresh
TIC_TIMEOUT = 0.1

COMPLEX_ANIMATIONS_FOLDER = 'complex_animations'
SPACESHIP_ANIMATIONS = load_animations_from_folder(
    path.join(COMPLEX_ANIMATIONS_FOLDER, 'spaceship')
)
