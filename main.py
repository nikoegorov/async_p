import asyncio
import curses
from random import choice, randint, random
from time import sleep

from fire_animation import fire


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


def draw(canvas):
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
            start_row=int(max_height/2),
            start_column=int(max_width/2),
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

        canvas.border()   # Re-draw border to cover fire hits
        canvas.refresh()
        sleep(TIC_TIMEOUT)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)
    sleep(1)


if __name__ == "__main__":
    main()
