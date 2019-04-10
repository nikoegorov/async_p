import curses
from os import path

from time import sleep

from animations_code.background_animation import prepare_blink_coroutines
from animations_code.fire_animation import prepare_fire_coroutine
from animations_code.load_animations_frames import load_animations_from_folder
from animations_code.spaceship_animation import prepare_spaceship_animation
from settings import TIC_TIMEOUT, COMPLEX_ANIMATIONS_FOLDER


def draw(canvas, spaceship_animations):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()

    coroutines = []
    coroutines.extend(prepare_blink_coroutines(canvas))
    coroutines.append(prepare_fire_coroutine(canvas))
    coroutines.append(prepare_spaceship_animation(canvas, spaceship_animations))

    while coroutines:
        for cor in coroutines:
            try:
                _ = cor.send(None)
            except StopIteration:
                coroutines.remove(cor)

        canvas.border()  # Re-draw border to cover fire hit
        canvas.refresh()
        sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    spaceship_animations = load_animations_from_folder(
        path.join(COMPLEX_ANIMATIONS_FOLDER, 'spaceship')
    )
    curses.wrapper(draw, spaceship_animations=spaceship_animations)
    sleep(1)


if __name__ == '__main__':
    main()
