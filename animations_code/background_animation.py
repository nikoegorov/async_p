import asyncio
import curses
from random import choice, randint

from curses_tools import discover_active_area


async def blink(canvas, row, column, symbol='*'):
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


def prepare_blink_coroutines(
    canvas, amount_of_stars: int = 100, stars_symbols='+*.:'
) -> list:
    active_area = discover_active_area(canvas)

    return [
        blink(
            canvas=canvas,
            # We don't want to place stars at borderline, so 1 row/column cap
            row=randint(
                active_area['border_limit_top'], active_area['border_limit_bottom'] - 1
            ),
            column=randint(
                active_area['border_limit_left'], active_area['border_limit_right'] - 1
            ),
            symbol=choice(stars_symbols),
        )
        for _ in range(amount_of_stars)
    ]
