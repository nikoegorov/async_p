import asyncio
from collections import OrderedDict
from random import choice, randint

from curses_tools import discover_active_area, draw_frame, get_frame_size


def prepare_garbage_coroutine(canvas, garbage_frames: OrderedDict):
    active_area = discover_active_area(canvas)
    garbage_column = randint(
        active_area['border_limit_left'],
        active_area['border_limit_right']
    )
    garbage_chosen = choice(list(garbage_frames.values()))
    frame_height, frame_width = get_frame_size(garbage_chosen)
    if garbage_column + frame_width >= active_area['border_limit_right']:
        garbage_column = int(garbage_column - frame_width)

    return fly_garbage(
        canvas=canvas,
        column=garbage_column,
        garbage_frame=garbage_chosen,
    )

async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
