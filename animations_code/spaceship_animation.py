import asyncio
from typing import List

from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls


async def animate_spaceship(
    canvas,
    start_row: int,
    start_column: int,
    border_limit_rows_top: int,
    border_limit_rows_bottom: int,
    border_limit_columns_left: int,
    border_limit_columns_right: int,
    animations: List[str]
):
    animations_cycle = cycle(animations)

    row_shift = 0
    column_shift = 0

    while True:
        rows_direction, columns_direction, _ = read_controls(canvas)

        filename, frame = next(animations_cycle)
        frame_height, frame_width = get_frame_size(frame)

        shift_frame_rows_to_center = -int(frame_height / 2)
        shift_frame_columns_to_center = -int(frame_width / 2)

        current_position_row = start_row + row_shift
        current_position_column = start_column + column_shift

        desired_position_top_row = current_position_row + rows_direction
        desired_position_left_column = current_position_column + columns_direction

        desired_frame_top_row = desired_position_top_row + shift_frame_rows_to_center
        desired_frame_bottom_row = desired_position_top_row - shift_frame_rows_to_center

        desired_frame_left_column = desired_position_left_column + shift_frame_columns_to_center
        desired_frame_right_column = desired_position_left_column - shift_frame_columns_to_center

        if desired_frame_top_row < border_limit_rows_top:
            rows_direction = 0

        if desired_frame_bottom_row > border_limit_rows_bottom:
            rows_direction = 0

        if desired_frame_left_column < border_limit_columns_left:
            columns_direction = 0

        if desired_frame_right_column > border_limit_columns_right:
            columns_direction = 0

        row_shift += rows_direction
        column_shift += columns_direction

        spaceship_center_row = start_row + row_shift + shift_frame_rows_to_center
        spaceship_center_column = start_column + column_shift + shift_frame_columns_to_center

        draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame)
        canvas.refresh()
        for i in range(2):
            await asyncio.sleep(0)
        draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame,
                   negative=True)
        canvas.refresh()
