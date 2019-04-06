import asyncio
from itertools import cycle
from typing import List

from curses_tools import draw_frame, get_frame_size, read_controls


async def animate_spaceship(canvas, start_row: int, start_column: int, animations: List[str]):
    animations_cycle = cycle(animations)

    row_shift = 0
    column_shift = 0

    while True:
        rows_direction, columns_direction, _ = read_controls(canvas)
        row_shift += rows_direction
        column_shift += columns_direction

        filename, frame = next(animations_cycle)
        frame_height, frame_width  = get_frame_size(frame)

        spaceship_center_row = start_row - int(frame_height / 2) + row_shift
        spaceship_center_column = start_column - int(frame_width / 2) + column_shift


        draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame)
        canvas.refresh()
        for i in range(2):
            await asyncio.sleep(0)
        draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame, negative=True)
        canvas.refresh()


