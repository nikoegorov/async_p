import curses
from os import path
from random import choice, randint
from time import sleep

from animations_code.background_animation import blink
from animations_code.fire_animation import fire
from animations_code.load_animations_frames import load_animations_from_folder
from animations_code.spaceship_animation import animate_spaceship


TIC_TIMEOUT = 0.01
COMPLEX_ANIMATIONS_FOLDER = 'complex_animations'
SPACESHIP_ANIMATIONS_FOLDER = 'spaceship'
SPACESHIP_ANIMATIONS = load_animations_from_folder(
        path.join(COMPLEX_ANIMATIONS_FOLDER, SPACESHIP_ANIMATIONS_FOLDER)
    )



def discover_active_area(canvas) -> dict:
    max_height, max_width = canvas.getmaxyx()

    return {
        'border_limit_top': 1,
        'border_limit_left': 1,
        'border_limit_right': max_width - 1,
        'border_limit_bottom': max_height - 1,
        'window_center_row': int(max_height / 2),
        'window_center_column': int(max_width / 2),
    }


def prepare_blink_coroutines(
    canvas,
    amount_of_stars: int=100,
    stars_symbols="+*.:"
) -> list:
    active_area = discover_active_area(canvas)

    return [
        blink(
            canvas=canvas,
            # We don't want to place stars at borderline, so 1 row/column cap
            row=randint(
                active_area['border_limit_top'],
                active_area['border_limit_bottom'] - 1
            ),
            column=randint(
                active_area['border_limit_left'],
                active_area['border_limit_right'] - 1
            ),
            symbol=choice(stars_symbols),
        )
        for _ in range(amount_of_stars)
    ]


def prepare_fire_coroutine(canvas):
    active_area = discover_active_area(canvas)
    return fire(
            canvas=canvas,
            start_row=active_area['window_center_row'],
            start_column=active_area['window_center_column'],
        )


def prepare_spaceship_animation(canvas, spaceship_animations=SPACESHIP_ANIMATIONS):
    active_area = discover_active_area(canvas)

    return animate_spaceship(
        canvas=canvas,
        start_row=active_area['window_center_row'],
        start_column=active_area['window_center_column'],
        border_limit_top=active_area['border_limit_top'],
        border_limit_bottom=active_area['border_limit_bottom'],
        border_limit_left=active_area['border_limit_left'],
        border_limit_right=active_area['border_limit_right'],
        animations=spaceship_animations,
    )


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

        canvas.border()  # Re-draw border to cover fire hits
        canvas.refresh()
        sleep(TIC_TIMEOUT)


def main():


    curses.update_lines_cols()
    curses.wrapper(draw)
    sleep(1)


if __name__ == "__main__":
    main()
