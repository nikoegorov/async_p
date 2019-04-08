import curses

from time import sleep

from animations_code.background_animation import prepare_blink_coroutines
from animations_code.fire_animation import prepare_fire_coroutine
from animations_code.spaceship_animation import prepare_spaceship_animation
from constants import TIC_TIMEOUT


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()

    coroutines = []
    coroutines.extend(prepare_blink_coroutines(canvas))
    coroutines.append(prepare_fire_coroutine(canvas))
    coroutines.append(prepare_spaceship_animation(canvas))

    while True:
        if len(coroutines) == 0:
            break

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
    curses.wrapper(draw)
    sleep(1)


if __name__ == '__main__':
    main()
