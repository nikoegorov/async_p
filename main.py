import asyncio
import curses
from os import listdir, path
from random import choice, randint
from time import sleep

from fire_animation import fire
from spaceship_animation import animate_spaceship


async def blink(canvas, row, column, symbol="*"):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(randint(1, 18)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(randint(1, 8)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(randint(1, 3)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(randint(1, 3)):
            await asyncio.sleep(0)


def draw(canvas, spaceshift_animations):
    TIC_TIMEOUT = 0.1

    curses.curs_set(False)
    canvas.border()

    max_height, max_width = canvas.getmaxyx()

    canvas.refresh()
    symbols = "+*.:"

    coroutines = [
        blink(
            canvas=canvas,
            # Top border takes 1 line at top and 2 lines at bottom.
            row=randint(1, max_height - 2),
            # Left border takes 1 line from the left and 2 lines at the right.
            column=randint(1, max_width - 2),
            symbol=choice(symbols),
        )
        for _ in range(100)
    ]

    coroutines.append(
        fire(
            canvas=canvas,
            start_row=int(max_height / 2),
            start_column=int(max_width / 2),
        )
    )

    coroutines.append(
        animate_spaceship(
            canvas=canvas,
            row=int(max_height / 2),
            column=int(max_width / 2),
            animations=spaceshift_animations,
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


def read_file_contents(folder_path: str, filename: str) -> tuple:
    with open(path.join(folder_path, filename)) as r:
        return (filename, r.read())


def list_files_in_folder(folder_path):
    if not path.isdir(folder_path):
        raise IOError(f'Folder "{folder_path}" is missing.')

    return [
        file
        for file in listdir(folder_path)
        if path.isfile(path.join(folder_path, file))
    ]


def load_animations_from_folder(folder_path: str):
    animations = []
    files = list_files_in_folder(folder_path)
    for filename in files:
        animation_in_file = read_file_contents(folder_path, filename)
        animations.append(animation_in_file)

    return sorted(animations)


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
