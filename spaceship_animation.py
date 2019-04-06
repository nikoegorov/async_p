import asyncio
from itertools import cycle
from typing import List

from curses_tools import draw_frame


async def animate_spaceship(canvas, row, column, animations: List[str]):
    animations_cycle = cycle(animations)
    while True:
        filename, frame = next(animations_cycle)
        draw_frame(canvas, row, column, frame)
        canvas.refresh()
        for i in range(5):
            await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        canvas.refresh()
