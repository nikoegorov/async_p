import curses
from os import path
from random import choice, randint
from time import sleep

from animations_code.background_animation import blink
from animations_code.fire_animation import fire
from animations_code.load_animations_frames import load_animations_from_folder
from animations_code.spaceship_animation import animate_spaceship


TIC_TIMEOUT = 0.1


def draw(canvas, spaceship_animations):

    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()

    max_height, max_width = canvas.getmaxyx()
    canvas.addstr(20, 2, "Your terminal is %dx%d in size." % (max_width, max_height))

    border_limit_top = 1
    border_limit_left = 1
    border_limit_right = max_width - 2
    border_limit_bottom = max_height - 2

    window_center_row = int(border_limit_bottom / 2)
    window_center_column = int(border_limit_right / 2)

    canvas.refresh()
    stars_symbols = "+*.:"

    coroutines = [
        blink(
            canvas=canvas,
            # Border takes 1 line at top and 2 lines at bottom.
            row=randint(1, border_limit_bottom),
            # Border takes 1 line from the left and 2 lines at the right.
            column=randint(1, border_limit_right),
            symbol=choice(stars_symbols),
        )
        for _ in range(100)
    ]

    coroutines.append(
        fire(
            canvas=canvas,
            start_row=window_center_row,
            start_column=window_center_column,
        )
    )

    coroutines.append(
        animate_spaceship(
            canvas=canvas,
            start_row=window_center_row,
            start_column=window_center_column,
            border_limit_rows_top=border_limit_top,
            border_limit_rows_bottom=border_limit_bottom,
            border_limit_columns_left=border_limit_left,
            border_limit_columns_right=border_limit_right,
            animations=spaceship_animations,
        )
    )

    while True:
        if len(coroutines) == 0:
            break

        for cor in coroutines:
            try:
                _ = cor.send(None)
            except StopIteration:
                coroutines.remove(cor)

        canvas.border()  # Re-draw border to cover fire hits
        canvas.refresh()
        sleep(TIC_TIMEOUT)


def main():

    complex_animations_folder = 'complex_animations'
    spaceship_animations_folder = 'spaceship'
    spaceship_animations = load_animations_from_folder(
        path.join(complex_animations_folder, spaceship_animations_folder)
    )

    curses.update_lines_cols()
    curses.wrapper(draw, spaceship_animations)
    sleep(1)


if __name__ == "__main__":
    main()
