import asyncio
from collections import OrderedDict, deque
from random import choice, randint

import math

from curses_tools import discover_active_area, draw_frame, get_frame_size



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




def fill_orbit_with_garbage(canvas, garbage_frames: OrderedDict):
    return [
        prepare_garbage_coroutine(canvas, garbage_frames)
        for _ in range(len(garbage_frames))
    ]

def is_overlapping(garbage_instances: deque, candidate_height, candidate_width, candidate_column):
    for queue_element in garbage_instances:
        height, width, delay, column = queue_element
        if candidate_height >= delay or candidate_height >= height:
            if candidate_column in range(column, column + width):
                return True
            elif column in range(candidate_column, candidate_column + candidate_width):
                return True
        # else:

        # if all([
        #     candidate_height > delay,
        #     candidate_column in range(column, column + width),
        # ]):
        #     return True

        # if all([
        #     height >= candidate_height,
        #     delay in range(candidate_height, height + delay),
        #     candidate_column in range(column, column + width),
        # ]):
        #     return True
        # else:
        #     continue
        #

async def prepare_garbage_coroutine(canvas, garbage_frames: OrderedDict):
    garbage_queue = deque(maxlen=len(garbage_frames) * 2)
    while True:
        active_area = discover_active_area(canvas)
        garbage_column = randint(
            active_area['border_limit_left'],
            active_area['border_limit_right']
        )
        garbage_chosen = choice(list(garbage_frames.values()))
        frame_height, frame_width = get_frame_size(garbage_chosen)
        delay = frame_height * 7 - randint(frame_height , frame_height * 2)

        if is_overlapping(garbage_queue, frame_height, frame_width, garbage_column):
            continue
        else:
            garbage_queue.append((frame_height, frame_width, delay, garbage_column))


        for _ in range(0, delay):
            await asyncio.sleep(0)

        if garbage_column + frame_width >= active_area['border_limit_right']:
            garbage_column = int(garbage_column - frame_width)

        # print(garbage_queue)

        await fly_garbage(
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
