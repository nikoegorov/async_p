import asyncio
from itertools import cycle
from typing import List

from curses_tools import draw_frame, get_frame_size


async def animate_spaceship(canvas, row: int, column: int, animations: List[str]):
    animations_cycle = cycle(animations)

    while True:
        filename, frame = next(animations_cycle)
        frame_height, frame_width  = get_frame_size(frame)

        spaceship_center_row = row - int(frame_height / 2)
        spaceship_center_column = column - int(frame_width / 2)

        draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame)
        canvas.refresh()
        for i in range(5):
            await asyncio.sleep(0)
        draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame, negative=True)
        canvas.refresh()
